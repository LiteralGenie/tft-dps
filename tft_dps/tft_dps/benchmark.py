import asyncio
import json
import time
from pathlib import Path

from tft_dps.lib.cache import NativeFileCache
from tft_dps.lib.paths import CD_DIR
from tft_dps.lib.simulator.sim_runner import SimRunner

"""
workers <-> worker_manager <-> web_servers

mgr <-> web_servers
    shared request queue
    per-server response queue

mgr <-> workers
    shared job queue
    shared result queue
"""

# log_http_requests()


async def main():
    print("Initializing simulator ...")
    cache = NativeFileCache(CD_DIR)
    runner = await SimRunner.ainit(cache)

    #

    Path("/tmp/units").write_text(json.dumps(runner.units, indent=2))
    Path("/tmp/items").write_text(json.dumps(runner.items, indent=2))
    Path("/tmp/traits").write_text(json.dumps(runner.traits, indent=2))

    #

    n = 100
    ti = time.time()
    for idx in range(n):
        result = await runner.run(
            "Characters/TFT15_Gnar",
            3,
            [
                "TFT_Item_ArchangelsStaff",
                "TFT_Item_ArchangelsStaff",
                "TFT_Item_ArchangelsStaff",
            ],
            dict(
                TFT15_Luchador=1,
                TFT15_Sniper=1,
            ),
        )
    el = time.time() - ti
    print(f"{(el / n)*1000:.0f}ms")


if __name__ == "__main__":
    asyncio.run(main())
