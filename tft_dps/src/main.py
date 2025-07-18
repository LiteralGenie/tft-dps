"""
dps(T) = total_auto_dmg + total_spell_dmg

total_auto_dmg(T) = auto_count(T) * auto_dmg(T)

total_spell_dmg(T) = cast_count(T) * cast_dmg(T)

cast_count(T) = mana_regen(T) + auto_count(T) * auto_mana

auto_count(T) = [simulated]
"""

import json
from pathlib import Path

from lib.cache import NativeFileCache, fetch_cached_json
from lib.resolver import (
    fetch_cdragon_map22,
    fetch_cdragon_patch_status,
    fetch_cdragon_strings,
    fetch_cdragon_unit,
    get_units,
)
from lol_resolver.tft.generator import get_unit_ids

# log_http_requests()

VERSION = "pbe"


# def main():
#     alias = "tft-units"
#     urls = ["data/maps/shipping/map22/map22.bin.json"]
#     return gen_handler("pbe", ["en_us"], alias, urls, generate_version_units, False)


def main():
    cache = NativeFileCache("/tmp/tft_dps")

    patch_status = fetch_cdragon_patch_status(VERSION)
    if "done" not in patch_status:
        raise Exception(patch_status)

    map22 = fetch_cached_json(
        lambda: fetch_cdragon_map22(VERSION),
        cache,
        "map22",
    )

    unit_ids: list[str] = get_unit_ids(map22)
    raw_units = {
        id: fetch_cached_json(
            lambda: fetch_cdragon_unit(VERSION, id),
            cache,
            f"unit_{id.split('/')[-1]}",
        )
        for id in unit_ids
    }

    strings = fetch_cached_json(
        lambda: fetch_cdragon_strings(VERSION, "en_us"), cache, "strings"
    )["entries"]

    units = get_units(VERSION, map22, raw_units, strings)
    Path("/tmp/units").write_text(json.dumps(units, indent=2))


main()
