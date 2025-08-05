import json
import sqlite3
from typing import AsyncGenerator

import bitarray
from fastapi import Request
from fastapi.responses import StreamingResponse

from tft_dps.lib.constants import MAX_IDS_PER_SIMULATE, PACKED_ID_BIT_ESTIMATE
from tft_dps.lib.db import TftDb
from tft_dps.lib.simulator.sim_state import SimResult
from tft_dps.lib.utils.network_utils import (
    decompress_gzip,
    unpack_sim_id,
    unpack_sim_id_array,
)
from tft_dps.lib.web.app_worker import AppWorkerContext
from tft_dps.lib.web.job_worker import SimulateAllRequest, SimulateRequest
from tft_dps.lib.web.worker_manager import dbid_from_request

APP_WORKER_CONTEXT: AppWorkerContext


async def handle_simulate(req: Request):
    body = await req.body()

    # Decode request
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

    # Convert to SimulateRequest
    sim_requests: list[SimulateRequest] = []
    for r in raw_requests:
        id_unit = APP_WORKER_CONTEXT.unit_info_by_index[r["unit"]]["info"]["id"]
        items = [
            APP_WORKER_CONTEXT.item_info_by_index[itemId]["id"]
            for itemId in r["items"]
            if itemId > 0
        ]
        traits = APP_WORKER_CONTEXT.unit_info[id_unit]["info"]["traits"]
        sim_req = SimulateRequest(
            type="simulate_request",
            id_unit=id_unit,
            stars=r["stars"],
            items=items,
            traits={trait: tier for trait, tier in zip(traits, r["traits"])},
        )

        sim_requests.append(sim_req)

    # Chunk and process
    return StreamingResponse(_stream(period, sim_requests))


async def _stream(period: float, reqs: list[SimulateRequest]):
    db = TftDb().connect()

    async for chunk in _handle_simulate_chunk(db, period, reqs):
        yield json.dumps([x["total"] for x in chunk]).encode()


async def _handle_simulate_chunk(
    db: sqlite3.Connection,
    period: float,
    reqs: list[SimulateRequest],
) -> "AsyncGenerator[list[dict]]":
    """
    Yielding a large number of responses is slow for some reason
    (~250ms per chunk on localhost / chrome, independent of chunk size)

    But large fixed-size chunks can take a long time depending on
    how many requests are in db vs how many need to be generated

    So as a compromise, buffer until we hit G generations and yield that buffer
    so with R requests, if all are cached, client sees a stream with single chunk of size R
    if none are cached, client sees stream of (R/G) chunks of size G
    """

    max_generations_per_batch = 100

    buffer: list[dict | None] = []
    idx_from_worker = []

    async def _generate():
        nonlocal buffer, idx_from_worker

        async with APP_WORKER_CONTEXT.queue_lock:
            APP_WORKER_CONTEXT.req_queue.put(
                SimulateAllRequest(
                    type="simulate_all_request",
                    requests=[reqs[req_idx] for req_idx, _ in idx_from_worker],
                )
            )

            sims_from_workers: list[SimResult] = APP_WORKER_CONTEXT.resp_queue.get()
            for idx_sim, res in zip(idx_from_worker, sims_from_workers):
                buffer[idx_sim] = dict(
                    total=_calc_dps(res, period),
                )

            idx_from_worker = []

    for req_idx, req in enumerate(reqs):
        buffer_idx = len(buffer)

        # Select from db, scheduling any missing for workers
        dps = _select_dps(db, req, period)
        buffer.append(dps)
        if not dps:
            idx_from_worker.append((req_idx, buffer_idx))

        # Collect worker results
        if len(idx_from_worker) >= max_generations_per_batch:
            await _generate()

            # Flush
            yield buffer  # type: ignore
            buffer = []

    if idx_from_worker:
        await _generate()

    if buffer:
        yield buffer  # type: ignore


def _select_dps(db: sqlite3.Connection, req: SimulateRequest, t: float) -> dict | None:
    id = dbid_from_request(req)

    does_exist = bool(db.execute("SELECT 1 FROM combo WHERE id = ?", [id]).fetchone())
    if not does_exist:
        return None

    total = db.execute(
        """
        SELECT AVG(
            mult * physical +
            mult * magical +
            mult * true
        ) avg
        FROM dps
        WHERE
            id_combo = ?
            AND t <= ?
        """,
        [id, t],
    ).fetchone()["avg"]

    return dict(total=total)


def _calc_dps(res: SimResult, period: float):
    total_damage = 0

    for x in [
        *res["attacks"],
        *res["casts"],
        *res["misc_damage"],
    ]:
        if x["t"] > period:
            break

        total_damage += x["mult"] * (
            x["physical_damage"] + x["magical_damage"] + x["true_damage"]
        )

    return total_damage / period
