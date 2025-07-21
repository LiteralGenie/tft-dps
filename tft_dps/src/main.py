import json
from pathlib import Path

from lib.cache import NativeFileCache
from lib.resolver import (
    fetch_cached_and_get_items,
    fetch_cached_and_init_unit_processor,
)

# log_http_requests()

VERSION = "pbe"


# def main():
#     alias = "tft-units"
#     urls = ["data/maps/shipping/map22/map22.bin.json"]
#     return gen_handler("pbe", ["en_us"], alias, urls, generate_version_units, False)


def main():
    cache = NativeFileCache("/tmp/tft_dps")

    proc = fetch_cached_and_init_unit_processor(cache, VERSION)
    units = {k: proc.get_unit(k) for k in proc.unit_list}
    Path("/tmp/units").write_text(json.dumps(units, indent=2))

    items = fetch_cached_and_get_items(cache, VERSION)
    Path("/tmp/items").write_text(json.dumps(items, indent=2))


main()
