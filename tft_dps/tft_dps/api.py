from tft_dps.lib.cache import Cache
from tft_dps.lib.calc_ctx import CalcCtx, CalcCtxStats
from tft_dps.lib.resolver import (
    fetch_cached_and_get_items,
    fetch_cached_and_init_unit_processor,
)
from tft_dps.lib.simulator.simulate import simulate
from tft_dps.lib.simulator.unit_quirks import GarenQuirks
from tft_dps.lib.utils.misc_utils import log_http_requests
from tft_dps.lol_resolver.tft.units import TFTUnitsProcessor

log_http_requests()

VERSION = "pbe"


class SimulationRunner:
    def __init__(self, cache: Cache, unit_proc: TFTUnitsProcessor, items: dict) -> None:
        self.cache = cache
        self.unit_proc = unit_proc
        self.items = items

    @classmethod
    async def ainit(cls, cache: Cache):
        unit_proc = await fetch_cached_and_init_unit_processor(cache, VERSION)
        items = await fetch_cached_and_get_items(cache, VERSION)
        return cls(cache, unit_proc, items)

    async def run(self, unit_id: str):
        ctx = CalcCtx(
            unit_id=unit_id,
            T=30,
            item_info=self.items,
            unit_proc=self.unit_proc,
            item_inventory=dict(),
            stats=CalcCtxStats.from_unit(unit_id, 3, self.unit_proc),
            unit_quirks=GarenQuirks(),
            flags=dict(),
        )

        result = simulate(ctx)
        return result
