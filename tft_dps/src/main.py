import json
from pathlib import Path

from lib.cache import NativeFileCache
from lib.calc_ctx import CalcCtx, CalcCtxStats
from lib.constants import CHAMPION_UNITS
from lib.resolver import (
    fetch_cached_and_get_items,
    fetch_cached_and_init_unit_processor,
)
from lib.simulator.plot import calc_total_damage
from lib.simulator.simulate import simulate
from lib.simulator.units.aatrox import AatroxQuirks

# log_http_requests()

VERSION = "pbe"


def main():
    cache = NativeFileCache("/tmp/tft_dps")

    unit_proc = fetch_cached_and_init_unit_processor(cache, VERSION)
    units: dict = {}
    for id in CHAMPION_UNITS:
        base_stats = unit_proc.get_base_stats(id)
        info = unit_proc.get_unit(id, unit_proc.get_base_stats(id))
        spell_vars = unit_proc.calc_spell_vars_for_level(id, 1, base_stats)
        if info:
            units[info["id"]] = dict(
                base_stats=base_stats,
                spell_vars=spell_vars,
                info=info,
            )

    Path("/tmp/units").write_text(json.dumps(units, indent=2))

    items = fetch_cached_and_get_items(cache, VERSION)
    Path("/tmp/items").write_text(json.dumps(items, indent=2))

    #

    ctx = CalcCtx(
        unit_id="Characters/TFT15_Aatrox",
        T=20,
        item_info=items,
        unit_proc=unit_proc,
        item_inventory=dict(),
        stats=CalcCtxStats.from_unit("Characters/TFT15_Aatrox", 1, unit_proc),
        unit_quirks=AatroxQuirks(),
    )
    result = simulate(ctx)

    total = calc_total_damage(result)
    for pt in total:
        print(f"{pt['t']},{pt['physical']},{pt['magical']}")


main()
