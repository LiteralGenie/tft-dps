import asyncio

from tft_dps.lib.web.worker_manager import WorkerManager

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


# async def main():
#     cache = NativeFileCache("/tmp/tft_dps")
#     runner = await SimRunner.ainit(cache)

#     #

#     units: dict = {}
#     for id in CHAMPION_UNITS:
#         base_stats = runner.unit_proc.get_base_stats(id)
#         info = runner.unit_proc.get_unit(id, runner.unit_proc.get_base_stats(id))
#         spell_vars = runner.unit_proc.calc_spell_vars_for_level(id, 3, base_stats)
#         if info:
#             units[info["id"]] = dict(
#                 base_stats=base_stats,
#                 spell_vars=spell_vars,
#                 info=info,
#             )
#     Path("/tmp/units").write_text(json.dumps(units, indent=2))

#     Path("/tmp/items").write_text(json.dumps(runner.items, indent=2))

#     Path("/tmp/traits").write_text(json.dumps(runner.traits, indent=2))

#     #
#     n = 20

#     ti = time.time()
#     for idx in range(n):
#         result = await runner.run("Characters/TFT15_Gnar")
#     el = time.time() - ti
#     print(f"{(el / n)*1000:.0f}ms")

#     # total = calc_total_damage(result)
#     # for pt in total:
#     #     print(f"{pt['t']},{pt['physical']},{pt['magical']}")


async def main():
    WorkerManager.init(4, 8)


if __name__ == "__main__":
    asyncio.run(main())
