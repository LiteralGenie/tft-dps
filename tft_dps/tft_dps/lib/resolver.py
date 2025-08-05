import json

import requests

from tft_dps.lol_resolver.tft.traits import TFTTraitsProcessor

from ..lol_resolver.tft.generator import (
    filter_unit_props,
    get_set_items,
    get_set_traits,
    get_trait_units,
    get_unit_ids,
)
from ..lol_resolver.tft.items import TFTItemsProcessor
from ..lol_resolver.tft.units import TFTUnitsProcessor
from .cache import Cache, fetch_cached


# tft > generator.py > generate_version_items()
async def fetch_cached_and_get_traits(cache: Cache, version: str):
    map22 = await fetch_cached(
        lambda: fetch_cdragon_map22(version),
        cache,
        "map22",
    )

    strings = (
        await fetch_cached(
            lambda: fetch_cdragon_strings(version, "en_us"), cache, "strings"
        )
    )["entries"]

    unit_ids: list[str] = get_unit_ids(map22)
    raw_units = {
        id: await fetch_cached(
            lambda: fetch_cdragon_unit(version, id),
            cache,
            f"unit_{id.split('/')[-1]}",
        )
        for id in unit_ids
    }
    trait_units = get_trait_units(map22, raw_units)

    unit_props = filter_unit_props(map22)

    trait_list = get_set_traits(map22)

    proc = TFTTraitsProcessor(
        version,
        "en_us",
        map22,
        trait_list,
        trait_units,
        unit_props,
        strings,
    )

    return proc.get_traits()


async def fetch_cached_and_init_unit_processor(cache: Cache, version: str):
    map22 = await fetch_cached(
        lambda: fetch_cdragon_map22(version),
        cache,
        "map22",
    )

    unit_ids: list[str] = get_unit_ids(map22)
    raw_units = {
        id: await fetch_cached(
            lambda: fetch_cdragon_unit(version, id),
            cache,
            f"unit_{id.split('/')[-1]}",
        )
        for id in unit_ids
    }

    strings = (
        await fetch_cached(
            lambda: fetch_cdragon_strings(version, "en_us"), cache, "strings"
        )
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
async def fetch_cached_and_get_items(cache: Cache, version: str):
    map22 = await fetch_cached(
        lambda: fetch_cdragon_map22(version),
        cache,
        "map22",
    )

    strings = (
        await fetch_cached(
            lambda: fetch_cdragon_strings(version, "en_us"), cache, "strings"
        )
    )["entries"]

    unit_props = filter_unit_props(map22)

    raw_items = get_set_items(map22)

    proc = TFTItemsProcessor(
        version,
        "en_us",
        map22,
        raw_items,
        unit_props,
        strings,
    )

    return proc.get_items()


async def fetch_cdragon(version: str, path: str):
    url = f"https://raw.communitydragon.org/{version}/game/{path}"
    resp = requests.get(url)
    resp.raise_for_status()
    return json.loads(resp.text)


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
async def fetch_cdragon_map22(version: str):
    return await fetch_cdragon(version, "data/maps/shipping/map22/map22.bin.json")


# utils.py > gen_handler()
async def fetch_cdragon_patch_status(version: str):
    version_modified = "live" if version == "latest" else version

    url = f"https://raw.communitydragon.org/status.{version_modified}.txt"
    resp = requests.get(url)
    resp.raise_for_status()

    return resp.text


# tft > generator.py > download_unit()
async def fetch_cdragon_unit(version: str, unit_id: str) -> dict:
    try:
        return await fetch_cdragon(version, f"{unit_id.lower()}.cdtb.bin.json")
    except Exception:
        return {}


async def fetch_cdragon_version(version: str) -> dict:
    url = f"https://raw.communitydragon.org/{version}/content-metadata.json"
    resp = requests.get(url)
    resp.raise_for_status()
    return json.loads(resp.text)


async def fetch_cdragon_version_cached(cache: Cache, version: str) -> dict:
    return await fetch_cached(
        lambda: fetch_cdragon_version(version),
        cache,
        "content-metadata",
    )
