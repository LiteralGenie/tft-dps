from tft_dps.lib.cache import Cache
from tft_dps.lib.constants import CHAMPION_UNITS, VERSION
from tft_dps.lib.resolver import fetch_cached_and_init_unit_processor


async def get_all_units(cache: Cache):
    unit_proc = await fetch_cached_and_init_unit_processor(cache, VERSION)

    units: dict = {}
    for id in CHAMPION_UNITS:
        base_stats = unit_proc.get_base_stats(id)
        info = unit_proc.get_unit(id, unit_proc.get_base_stats(id))
        spell_vars = unit_proc.calc_spell_vars_for_level(id, 3, base_stats)
        if info:
            units[info["id"]] = dict(
                base_stats=base_stats,
                spell_vars=spell_vars,
                info=info,
            )

    return units
