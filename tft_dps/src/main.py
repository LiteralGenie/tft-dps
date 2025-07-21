import json
from pathlib import Path

from lib.cache import NativeFileCache
from lib.calc_ctx import CalcCtx, CalcCtxStats
from lib.resolver import (
    fetch_cached_and_get_items,
    fetch_cached_and_init_unit_processor,
)
from lib.simulator.simulate import simulate

# log_http_requests()

VERSION = "pbe"


# def main():
#     alias = "tft-units"
#     urls = ["data/maps/shipping/map22/map22.bin.json"]
#     return gen_handler("pbe", ["en_us"], alias, urls, generate_version_units, False)


def main():
    cache = NativeFileCache("/tmp/tft_dps")

    unit_proc = fetch_cached_and_init_unit_processor(cache, VERSION)
    units: dict = {}
    for k in unit_proc.unit_list:
        info = unit_proc.get_unit(k)
        if info:
            units[info["id"]] = info

    Path("/tmp/units").write_text(json.dumps(units, indent=2))

    items = fetch_cached_and_get_items(cache, VERSION)
    Path("/tmp/items").write_text(json.dumps(items, indent=2))

    #

    ctx = CalcCtx(
        unit_id="TFT15_Aatrox",
        T=20,
        item_info=items,
        unit_proc=unit_proc,
        item_inventory=dict(),
        stats=CalcCtxStats.from_unit(1, units["TFT15_Aatrox"]),
    )
    result = simulate(ctx)
    # print(result)


main()
