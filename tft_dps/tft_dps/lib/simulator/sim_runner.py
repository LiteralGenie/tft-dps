from tft_dps.lib.cache import Cache
from tft_dps.lib.calc_ctx import CalcCtx, CalcCtxStats
from tft_dps.lib.constants import VERSION
from tft_dps.lib.resolver import (
    fetch_cached_and_get_items,
    fetch_cached_and_get_traits,
    fetch_cached_and_init_unit_processor,
)
from tft_dps.lib.simulator.simulate import simulate
from tft_dps.lib.simulator.unit_quirks import GarenQuirks
from tft_dps.lol_resolver.tft.units import TFTUnitsProcessor


class SimRunner:
    def __init__(
        self,
        cache: Cache,
        unit_proc: TFTUnitsProcessor,
        items: dict,
        traits: dict,
    ) -> None:
        self.cache = cache
        self.unit_proc = unit_proc
        self.items = items
        self.traits = traits

    @classmethod
    async def ainit(cls, cache: Cache):
        unit_proc = await fetch_cached_and_init_unit_processor(cache, VERSION)
        items = await fetch_cached_and_get_items(cache, VERSION)
        traits = await fetch_cached_and_get_traits(cache, VERSION)
        return cls(cache, unit_proc, items, traits)

    async def run(
        self,
        unit_id: str,
        stars: int,
        items: dict[str, int],
        traits: dict[str, int],
    ):
        ctx = CalcCtx(
            T=30,
            unit_id=unit_id,
            unit_quirks=GarenQuirks(),
            unit_proc=self.unit_proc,
            base_stats=CalcCtxStats.from_unit(unit_id, stars, self.unit_proc),
            item_inventory=items,
            trait_inventory=traits,
            #
            item_info=self.items,
            trait_info=self.traits,
            flags=dict(),
        )

        result = simulate(ctx)
        return result
