import requests
from lib.cache import Cache, fetch_cached_json
from lol_resolver.tft.generator import filter_unit_props, get_set_items, get_unit_ids
from lol_resolver.tft.items import TFTItemsProcessor
from lol_resolver.tft.units import TFTUnitsProcessor


def fetch_cached_and_init_unit_processor(cache: Cache, version: str):
    map22 = fetch_cached_json(
        lambda: fetch_cdragon_map22(version),
        cache,
        "map22",
    )

    unit_ids: list[str] = get_unit_ids(map22)
    raw_units = {
        id: fetch_cached_json(
            lambda: fetch_cdragon_unit(version, id),
            cache,
            f"unit_{id.split('/')[-1]}",
        )
        for id in unit_ids
    }

    strings = fetch_cached_json(
        lambda: fetch_cdragon_strings(version, "en_us"), cache, "strings"
    )["entries"]

    proc = init_unit_processor(version, map22, raw_units, strings)
    return proc


# tft > generator.py > generate_version_units()
def init_unit_processor(version: str, map22, unit_list: dict, strings: dict):
    unit_props = filter_unit_props(map22)

    processor = TFTUnitsProcessor(
        version,
        "en_us",
        map22,
        unit_list,
        unit_props,
        strings,
    )

    return processor


# tft > generator.py > generate_version_items()
def fetch_cached_and_get_items(cache: Cache, version: str):
    map22 = fetch_cached_json(
        lambda: fetch_cdragon_map22(version),
        cache,
        "map22",
    )

    strings = fetch_cached_json(
        lambda: fetch_cdragon_strings(version, "en_us"), cache, "strings"
    )["entries"]

    unit_props = filter_unit_props(map22)

    items = get_set_items(map22)

    proc = TFTItemsProcessor(
        version,
        "en_us",
        map22,
        items,
        unit_props,
        strings,
    )

    return proc.get_items()


def fetch_cdragon(version: str, path: str):
    url = f"https://raw.communitydragon.org/{version}/game/{path}"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.text


# utils.py > cd_get_strings_file()
def fetch_cdragon_strings(version: str, language: str):
    candidates = [
        f"{language}/data/menu/en_us/tft.stringtable.json",
        f"{language}/data/menu/en_us/main.stringtable.json",
        f"data/menu/main_{language}.stringtable.json",
        f"data/menu/fontconfig_{language}.txt.json",
    ]

    for path in candidates:
        try:
            return fetch_cdragon(version, path)
        except Exception:
            continue

    raise Exception()


# tft > generator.py > get_tftmap_file()
def fetch_cdragon_map22(version: str):
    return fetch_cdragon(version, "data/maps/shipping/map22/map22.bin.json")


# utils.py > gen_handler()
def fetch_cdragon_patch_status(version: str):
    version_modified = "live" if version == "latest" else version

    url = f"https://raw.communitydragon.org/status.{version_modified}.txt"
    resp = requests.get(url)
    resp.raise_for_status()

    return resp.text


# tft > generator.py > download_unit()
def fetch_cdragon_unit(version: str, unit_id: str):
    try:
        return fetch_cdragon(version, f"{unit_id.lower()}.cdtb.bin.json")
    except requests.HTTPError:
        return "{}"
