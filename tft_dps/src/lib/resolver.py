from lol_resolver.tft.generator import generate_version_units
from lol_resolver.utils import gen_handler


def get_units():
    alias = "tft-units"
    urls = ["data/maps/shipping/map22/map22.bin.json"]
    return gen_handler("pbe", ["en_us"], alias, urls, generate_version_units, False)
