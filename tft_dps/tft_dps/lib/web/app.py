from dataclasses import dataclass

import bitarray
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from tft_dps.lib.constants import MAX_IDS_PER_SIMULATE, PACKED_ID_BIT_ESTIMATE
from tft_dps.lib.simulator.sim_state import SimResult
from tft_dps.lib.utils.network_utils import (
    decompress_gzip,
    unpack_sim_id,
    unpack_sim_id_array,
)
from tft_dps.lib.web.app_worker import AppWorkerContext
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
    body = await req.body()

    data = decompress_gzip(
        body,
        max_bytes=(MAX_IDS_PER_SIMULATE * PACKED_ID_BIT_ESTIMATE) // 8,
    )
    unpacked = unpack_sim_id_array(data)
    ids: list[bitarray.bitarray] = unpacked["ids"]
    period: float = unpacked["period"]

    raw_requests = [
        unpack_sim_id(id, APP_WORKER_CONTEXT.trait_bits_by_unit_index) for id in ids
    ]

    requests = []
    for r in raw_requests:
        id_unit = APP_WORKER_CONTEXT.unit_info_by_index[r["unit"]]["info"]["id"]
        items = [
            APP_WORKER_CONTEXT.item_info_by_index[itemId]["id"]
            for itemId in r["items"]
            if itemId > 0
        ]
        traits = APP_WORKER_CONTEXT.unit_info[id_unit]["info"]["traits"]
        requests.append(
            SimulateRequest(
                type="simulate_request",
                id_unit=id_unit,
                stars=r["stars"],
                items=items,
                traits={trait: tier for trait, tier in zip(traits, r["traits"])},
            )
        )

    APP_WORKER_CONTEXT.req_queue.put(
        SimulateAllRequest(type="simulate_all_request", requests=requests)
    )

    sims: list[SimResult] = APP_WORKER_CONTEXT.resp_queue.get()

    result = []
    for sim in sims:
        total_damage = 0

        for key in ["attacks", "casts", "misc_damage"]:
            for x in sim[key]:
                if x["t"] > period:
                    break

                total_damage += (
                    x["physical_damage"] + x["magical_damage"] + x["true_damage"]
                )

        result.append(total_damage / period)

    return result


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
