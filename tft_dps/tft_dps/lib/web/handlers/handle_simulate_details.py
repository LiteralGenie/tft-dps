import json

from tft_dps.lib.db import TftDb
from tft_dps.lib.simulator.sim_state import SimDamage, SimResult, SimStats
from tft_dps.lib.utils.db_utils import dbid_from_request
from tft_dps.lib.web.app_worker import AppWorkerContext
from tft_dps.lib.web.job_worker import SimulateAllRequest, SimulateRequest

APP_WORKER_CONTEXT: AppWorkerContext


async def handle_simulate_details(req: SimulateRequest):
    sim = _select_sim_result(req)
    if not sim:
        async with APP_WORKER_CONTEXT.queue_lock:
            APP_WORKER_CONTEXT.req_queue.put(
                SimulateAllRequest(
                    type="simulate_all_request",
                    requests=[req],
                )
            )

            res: list[SimResult] = APP_WORKER_CONTEXT.resp_queue.get()
            sim = res[0]

    return sim


def _select_sim_result(req: SimulateRequest) -> SimResult | None:
    id = dbid_from_request(req)

    db = TftDb()

    does_exist = bool(
        db.connect().execute("SELECT 1 FROM combo WHERE id = ?", [id]).fetchone()
    )
    if not does_exist:
        return

    dps_query = db.connect().execute(
        """
        SELECT
            type, t, mult, physical, magical, true
        FROM dps
        WHERE id_combo = ?
        ORDER by t ASC
        """,
        [id],
    )
    dps_rows = list(dps_query.fetchall())

    stats_query = db.connect().execute(
        """
        SELECT data
        FROM stats
        WHERE id_combo = ?
        """,
        [id],
    )
    stats = json.loads(stats_query.fetchone()["data"])

    result = SimResult(
        attacks=[
            SimDamage(
                t=r["t"],
                mult=r["mult"],
                physical_damage=r["physical"],
                magical_damage=r["magical"],
                true_damage=r["true"],
            )
            for r in dps_rows
            if r["type"] == "auto"
        ],
        casts=[
            SimDamage(
                t=r["t"],
                mult=r["mult"],
                physical_damage=r["physical"],
                magical_damage=r["magical"],
                true_damage=r["true"],
            )
            for r in dps_rows
            if r["type"] == "cast"
        ],
        misc_damage=[
            SimDamage(
                t=r["t"],
                mult=r["mult"],
                physical_damage=r["physical"],
                magical_damage=r["magical"],
                true_damage=r["true"],
            )
            for r in dps_rows
            if r["type"] == "misc"
        ],
        initial_stats=SimStats(**stats["initial_stats"]),
        final_stats=SimStats(**stats["final_stats"]),
    )
    return result
