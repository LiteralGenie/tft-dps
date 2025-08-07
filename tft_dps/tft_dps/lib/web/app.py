from dataclasses import dataclass

from bitarray.util import int2ba
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from tft_dps.lib.constants import PACKED_ID_BITS
from tft_dps.lib.utils.network_utils import sim_id_to_sim_request
from tft_dps.lib.web.app_worker import AppWorkerContext
from tft_dps.lib.web.handlers.handle_simulate import handle_simulate
from tft_dps.lib.web.handlers.handle_simulate_details import handle_simulate_details
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
    import os

    return os.getpid()
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
async def simulate_details_by_dto(dto: "SimulateDetailsDto"):
    req = SimulateRequest(
        type="simulate_request",
        id_unit=dto.id_unit,
        stars=dto.stars,
        items=dto.items,
        traits=dto.traits,
    )

    return await handle_simulate_details(req)


@app.post("/simulate/details/{id}")
async def simulate_details_by_id(id: int):
    req = sim_id_to_sim_request(
        int2ba(id, endian="big", length=PACKED_ID_BITS),
        APP_WORKER_CONTEXT,
    )
    return await handle_simulate_details(req)


@app.get("/info/units")
async def get_unit_info():
    return APP_WORKER_CONTEXT.unit_info


@app.get("/info/items")
async def get_item_info():
    return APP_WORKER_CONTEXT.item_info


@app.get("/info/traits")
async def get_trait_info():
    return APP_WORKER_CONTEXT.trait_info
    return APP_WORKER_CONTEXT.trait_info
