import asyncio
import multiprocessing as mp
from typing import Literal, TypedDict

from loguru import logger

from tft_dps.lib.simulator.sim_runner import SimRunner
from tft_dps.lib.simulator.sim_state import SimResult


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
    while True:
        if job_queue.qsize() == 0:
            await asyncio.sleep(0.25)
            continue

        job: SimulateJob = job_queue.get()
        req = job["req"]
        resp = await runner.run(
            unit_id=req["id_unit"],
            stars=req["stars"],
            items=req["items"],
            traits=req["traits"],
        )
        result_queue.put(
            SimulateJobResult(
                type="simulate_job_result",
                batch=job["batch"],
                resp=resp,
            )
        )
