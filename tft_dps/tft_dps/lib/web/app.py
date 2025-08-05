from dataclasses import dataclass

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from tft_dps.lib.simulator.sim_state import SimResult
from tft_dps.lib.web.app_worker import AppWorkerContext
from tft_dps.lib.web.handlers.handle_simulate import handle_simulate
from tft_dps.lib.web.job_worker import SimulateRequest
from tft_dps.lib.web.worker_manager import SimulateAllRequest

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
async def simulate(req: Request):
    return await handle_simulate(req)


@dataclass
class SimulateDetailsDto:
    id_unit: str
    period: int
    stars: int
    items: list[str]
    traits: dict[str, int]


@app.post("/simulate/details")
async def simulate_details(dto: SimulateDetailsDto):
    APP_WORKER_CONTEXT.req_queue.put(
        SimulateAllRequest(
            type="simulate_all_request",
            requests=[
                SimulateRequest(
                    type="simulate_request",
                    id_unit=dto.id_unit,
                    stars=dto.stars,
                    items=dto.items,
                    traits=dto.traits,
                )
            ],
        )
    )

    sims: list[SimResult] = APP_WORKER_CONTEXT.resp_queue.get()
    return sims[0]


@app.get("/info/units")
async def get_unit_info():
    return APP_WORKER_CONTEXT.unit_info


@app.get("/info/items")
async def get_item_info():
    return APP_WORKER_CONTEXT.item_info


@app.get("/info/traits")
async def get_trait_info():
    return APP_WORKER_CONTEXT.trait_info
