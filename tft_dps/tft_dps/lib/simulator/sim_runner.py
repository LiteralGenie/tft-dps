from tft_dps.lib.cache import Cache
from tft_dps.lib.calc_ctx import CalcCtx, CalcCtxStats
from tft_dps.lib.constants import CHAMPION_UNITS, ITEMS, VERSION
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
        units: dict,
        items: dict,
        traits: dict,
    ) -> None:
        self.cache = cache
        self.unit_proc = unit_proc
        self.units = units
        self.items = items
        self.traits = traits

    @classmethod
    async def ainit(cls, cache: Cache):
        unit_proc = await fetch_cached_and_init_unit_processor(cache, VERSION)
        items = await cls._get_items(cache)
        traits = await cls._get_traits(cache)
        units = cls._get_units(unit_proc)
        return cls(cache, unit_proc, units, items, traits)

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

    @classmethod
    def _get_units(cls, unit_proc: TFTUnitsProcessor):
        units: dict = {}
        for id in CHAMPION_UNITS:
            idxUnit = len(units)
            base_stats = unit_proc.get_base_stats(id)
            info = unit_proc.get_unit(id, unit_proc.get_base_stats(id))
            spell_vars = unit_proc.calc_spell_vars_for_level(id, 3, base_stats)
            if info:
                units[info["id"]] = dict(
                    index=idxUnit,
                    base_stats=base_stats,
                    spell_vars=spell_vars,
                    info=info,
                )
        return units

    @classmethod
    async def _get_items(cls, cache: Cache):
        items = await fetch_cached_and_get_items(cache, VERSION)

        for k, v in list(items.items()):
            try:
                idxItem = ITEMS.index(k) + 1
            except ValueError:
                del items[k]
                continue

            v: dict = v.copy()
            v.update(index=idxItem)
            items[k] = v

        return items

    @classmethod
    async def _get_traits(cls, cache: Cache):
        traits = await fetch_cached_and_get_traits(cache, VERSION)

        styleToRarity = {
            4: "unique",
            None: "bronze",
            3: "silver",
            5: "gold",
            6: "prismatic",
        }

        for t in traits.values():
            lastBp = None
            tiers = []

            assert len(t["breakpoints"]) == len(t["styles"])
            for bp, style in zip(t["breakpoints"], t["styles"]):
                tier = dict(breakpoint=bp, rarity=styleToRarity[style])

                if bp != lastBp:
                    tiers.append(tier)
                else:
                    tiers[-1] = tier

                lastBp = bp

            t["tiers"] = tiers

        return traits
