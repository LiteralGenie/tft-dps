import math

import loguru

from tft_dps.lib.cache import Cache
from tft_dps.lib.calc_ctx import CalcCtx, CalcCtxStats, CalcCtxTraits
from tft_dps.lib.constants import CHAMPION_UNITS, FLAGS, ITEMS, VERSION
from tft_dps.lib.paths import LOG_DIR
from tft_dps.lib.resolver import (
    fetch_cached_and_get_items,
    fetch_cached_and_get_traits,
    fetch_cached_and_init_unit_processor,
)
from tft_dps.lib.simulator.quirks.item_quirks import ITEM_QUIRK_MAP
from tft_dps.lib.simulator.quirks.trait_quirks import TRAIT_QUIRK_MAP
from tft_dps.lib.simulator.quirks.unit_quirk_map import UNIT_QUIRK_MAP
from tft_dps.lib.simulator.sim_state import SimResult
from tft_dps.lib.simulator.simulate import simulate
from tft_dps.lol_resolver.tft.units import TFTUnitsProcessor

loguru.logger.add(
    LOG_DIR / "sim.log",
    filter=lambda record: record["extra"].get("name") == "sim",
    rotation="10 MB",
    retention=2,
)
SIM_LOGGER = loguru.logger.bind(name="sim")


class SimRunner:
    """
    Builds everything needed to call simulate()
    """

    def __init__(
        self,
        cache: Cache,
        unit_proc: TFTUnitsProcessor,
        units: dict,
        items: dict,
        traits: dict,
        unit_props: dict,
    ) -> None:
        self.cache = cache
        self.unit_proc = unit_proc
        self.units = units
        self.items = items
        self.traits = traits
        self.unit_props = unit_props

    @classmethod
    async def ainit(cls, cache: Cache):
        unit_proc = await fetch_cached_and_init_unit_processor(cache, VERSION)
        items = await cls._get_items(cache)
        traits = await cls._get_traits(cache)
        units = cls._get_units(unit_proc)
        return cls(cache, unit_proc, units, items, traits, unit_proc.unit_properties)

    async def run(
        self,
        unit_id: str,
        stars: int,
        items: list[str],
        traits: dict[str, int],
    ) -> SimResult:
        unit_quirks = UNIT_QUIRK_MAP[unit_id](SIM_LOGGER)
        item_quirks = [ITEM_QUIRK_MAP[id](SIM_LOGGER) for id in items]
        trait_inventory = self._build_trait_inventory(traits)
        trait_quirks = [TRAIT_QUIRK_MAP[id](SIM_LOGGER) for id in trait_inventory]

        ctx = CalcCtx(
            T=30,
            unit_id=unit_id,
            unit_quirks=unit_quirks,
            unit_proc=self.unit_proc,
            unit_info=self.units[unit_id],
            base_stats=CalcCtxStats.from_unit(unit_id, stars, self.unit_proc),
            item_inventory=items,
            item_quirks=item_quirks,
            trait_inventory=trait_inventory,
            trait_quirks=trait_quirks,
            #
            item_info=self.items,
            trait_info=self.traits,
            flags=FLAGS,
        )

        result = simulate(ctx)
        return result

    @classmethod
    def _get_units(cls, unit_proc: TFTUnitsProcessor):
        units: dict = {}
        for id in CHAMPION_UNITS:
            info = unit_proc.get_unit(id, unit_proc.get_base_stats(id))
            if not info:
                continue

            # HP / AD aren't scaled to star level
            idxUnit = len(units)
            base_stats = unit_proc.get_base_stats(id)
            spell_vars = unit_proc.calc_spell_vars_for_level(id, 3, base_stats)
            info["role_items"] = [
                itemId for itemId in info["role_items"] if itemId in ITEMS
            ]

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

            t["breakpoints"].sort()

            num_bps = len(t["breakpoints"])
            if t["breakpoints"][0] > 1:
                num_bps += 1
                t["has_bp_1"] = False
            else:
                t["has_bp_1"] = True

            t["num_bits"] = math.ceil(math.log2(num_bps))
            t["num_bits"] = max(t["num_bits"], 1)

        return traits

    def _build_trait_inventory(
        self, trait_count: dict[str, int]
    ) -> dict[str, CalcCtxTraits]:
        result = dict()
        for id, tier_idx in trait_count.items():
            info = self.traits[id]
            if not info["has_bp_1"] and tier_idx == 0:
                continue

            real_idx = tier_idx
            if not info["has_bp_1"]:
                real_idx -= 1

            tier = info["tiers"][real_idx]
            bp = tier["breakpoint"]

            result[id] = CalcCtxTraits(
                id=id,
                index=real_idx,
                breakpoint=bp,
                effects_bonus=info["effects_bonus"][bp],
                effects_main=info["effects_main"],
            )

        return result
