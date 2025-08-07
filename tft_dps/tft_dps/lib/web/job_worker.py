import asyncio
import multiprocessing as mp
import time
from typing import Literal, TypedDict

import loguru
from loguru import logger

from tft_dps.lib.paths import LOG_DIR
from tft_dps.lib.simulator.sim_runner import SimRunner
from tft_dps.lib.simulator.sim_state import SimResult

loguru.logger.add(
    LOG_DIR / "worker_performance.log",
    filter=lambda record: record["extra"].get("name") == "worker_performance",
    rotation="10 MB",
    retention=2,
)
PERF_LOGGER = loguru.logger.bind(name="worker_performance")


class SimulateAllRequest(TypedDict):
    type: Literal["simulate_all_request"]
    requests: list["SimulateRequest"]


class SimulateRequest(TypedDict):
    type: Literal["simulate_request"]
    id_unit: str
    stars: int
    items: list[str]
    traits: dict[str, int]


class SimulateJob(TypedDict):
    type: Literal["simulate_job"]
    batch: "BatchInfo"
    req: SimulateRequest


class SimulateJobResult(TypedDict):
    type: Literal["simulate_job_result"]
    batch: "BatchInfo"
    resp: SimResult


class BatchInfo(TypedDict):
    id: str
    idx: int
    total: int


@logger.catch(reraise=True)
def run_job_worker(*args, **kwargs):
    asyncio.run(_run_job_worker(*args, **kwargs))


async def _run_job_worker(
    runner: SimRunner,
    job_queue: mp.Queue,
    result_queue: mp.Queue,
):
    times = []

    while True:
        if job_queue.qsize() == 0:
            await asyncio.sleep(0.25)
            continue

        start = time.time()

        job: SimulateJob = job_queue.get()
        req = job["req"]
        resp = await runner.run(
            unit_id=req["id_unit"],
            stars=req["stars"],
            items=req["items"],
            traits=req["traits"],
        )

        times = _append_perf_log(times, time.time() - start)

        result_queue.put(
            SimulateJobResult(
                type="simulate_job_result",
                batch=job["batch"],
                resp=resp,
            )
        )


def _append_perf_log(times: list[float], new_time: float, n=1000):
    times.append(new_time)
    if len(times) < n:
        return times

    avg = sum(times) / len(times)
    msg = f"{len(times)} sims in {avg*1000:.0f}ms per sim"
    PERF_LOGGER.info(msg)

    return []
