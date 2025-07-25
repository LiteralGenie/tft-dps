from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from tft_dps.lib.web.app_worker import AppWorkerContext
from tft_dps.lib.web.job_worker import SimulateRequest

__all__ = ["app"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


APP_WORKER_CONTEXT: AppWorkerContext


@app.get("/ping")
async def ping():
    return "pong"


@app.post("/simulate")
async def simulate(data: SimulateRequest):
    APP_WORKER_CONTEXT.req_queue.put(data)
    result = APP_WORKER_CONTEXT.resp_queue.get()
    return result


@app.get("/info/units")
async def get_unit_info():
    return APP_WORKER_CONTEXT.unit_info


@app.get("/info/items")
async def get_item_info():
    return APP_WORKER_CONTEXT.item_info


@app.get("/info/traits")
async def get_trait_info():
    return APP_WORKER_CONTEXT.trait_info
