import json
from pathlib import Path

from tft_dps.lib.cache import NativeFileCache
from tft_dps.lib.calc_ctx import CalcCtx, CalcCtxStats
from tft_dps.lib.resolver import (
    fetch_cached_and_get_items,
    fetch_cached_and_init_unit_processor,
)
from tft_dps.lib.simulator.plot import calc_total_damage
from tft_dps.lib.simulator.simulate import simulate
from tft_dps.lib.simulator.unit_quirks import GarenQuirks

# log_http_requests()

VERSION = "pbe"


def main():
    cache = NativeFileCache("/tmp/tft_dps")

    unit_proc = fetch_cached_and_init_unit_processor(cache, VERSION)
    # units: dict = {}
    # for id in CHAMPION_UNITS:
    #     base_stats = unit_proc.get_base_stats(id)
    #     info = unit_proc.get_unit(id, unit_proc.get_base_stats(id))
    #     spell_vars = unit_proc.calc_spell_vars_for_level(id, 3, base_stats)
    #     if info:
    #         units[info["id"]] = dict(
    #             base_stats=base_stats,
    #             spell_vars=spell_vars,
    #             info=info,
    #         )
    # Path("/tmp/units").write_text(json.dumps(units, indent=2))

    items = fetch_cached_and_get_items(cache, VERSION)
    Path("/tmp/items").write_text(json.dumps(items, indent=2))

    #

    ctx = CalcCtx(
        unit_id="Characters/TFT15_Garen",
        T=20,
        item_info=items,
        unit_proc=unit_proc,
        item_inventory=dict(),
        stats=CalcCtxStats.from_unit("Characters/TFT15_Garen", 3, unit_proc),
        unit_quirks=GarenQuirks(),
        flags=dict(),
    )
    result = simulate(ctx)

    total = calc_total_damage(result)
    for pt in total:
        print(f"{pt['t']},{pt['physical']},{pt['magical']}")


if __name__ == "__main__":
    main()
