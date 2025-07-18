import requests
from lol_resolver.tft.generator import filter_unit_props
from lol_resolver.tft.units import TFTUnitsProcessor


# tft > generator.py > generate_version_units()
def get_units(version: str, map22, unit_list: dict, strings: dict):
    unit_props = filter_unit_props(map22)

    processor = TFTUnitsProcessor(
        version,
        "en_us",
        map22,
        unit_list,
        unit_props,
        strings,
    )

    return processor.success_return


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
