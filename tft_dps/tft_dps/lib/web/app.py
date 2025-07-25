from fastapi import FastAPI

from tft_dps.lib.web.app_worker import AppWorkerContext
from tft_dps.lib.web.job_worker import SimulateRequest

__all__ = ["app"]

app = FastAPI()

APP_WORKER_CONTEXT: AppWorkerContext


@app.get("/ping")
async def ping():
    return "pong"


@app.post("/simulate")
async def simulate(data: dict):
    APP_WORKER_CONTEXT.req_queue.put(
        SimulateRequest(
            type="simulate",
            **data,
        )
    )
    result = APP_WORKER_CONTEXT.resp_queue.get()
    return result
