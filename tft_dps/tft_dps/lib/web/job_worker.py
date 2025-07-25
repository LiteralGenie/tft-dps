import asyncio
import multiprocessing as mp
from typing import Literal, TypedDict

from tft_dps.lib.simulator.sim_runner import SimRunner


class SimulateRequest(TypedDict):
    type: Literal["simulate"]
    id: str




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

        job = job_queue.get()
        req: SimulateRequest = job["req"]
        resp = (await runner.run(req["id"])).as_dict()
        result_queue.put(
            dict(
                **job,
                resp=resp,
            )
        )
