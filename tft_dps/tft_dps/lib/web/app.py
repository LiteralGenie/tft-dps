from collections import Counter

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from tft_dps.lib.constants import MAX_IDS_PER_SIMULATE, PACKED_ID_BIT_ESTIMATE
from tft_dps.lib.utils.network_utils import (
    decodePackedId,
    decodePackedIdArray,
    decompress_gzip,
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
    packed_ids = decodePackedIdArray(data)
    raw_requests = [
        decodePackedId(id, APP_WORKER_CONTEXT.max_trait_bits_by_unit)
        for id in packed_ids
    ]

    requests = []
    for r in raw_requests:
        id_unit = APP_WORKER_CONTEXT.unit_info_by_index[r["unit"]]["info"]["id"]
        items = dict(
            Counter(
                [
                    APP_WORKER_CONTEXT.item_info_by_index[item]["id"]
                    for item in r["items"]
                ]
            ).items()
        )
        traits = APP_WORKER_CONTEXT.unit_info[id_unit]["traits"]
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
