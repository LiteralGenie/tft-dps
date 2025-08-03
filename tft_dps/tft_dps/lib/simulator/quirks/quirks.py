from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from loguru import Logger

from attr import dataclass

from tft_dps.lib.simulator.sim_state import SimState, SimStats
from tft_dps.lib.simulator.sim_system import SimSystem


class UnitQuirks(SimSystem):
    id: str

    notes: list[str] = []

    def __init__(self, logger: "Logger"):
        super().__init__()

        self.logger = logger

    def get_auto_damage(self, s: SimState, stats: SimStats) -> "UnitQuirksDamage":
        return UnitQuirksDamage(
            phys=stats.effective_ad * stats.crit_bonus,
        )

    def get_spell_damage(self, s: SimState, stats: SimStats) -> "UnitQuirksDamage":
        return UnitQuirksDamage()

    def _calc_spell_vars(self, s: SimState, stats: SimStats):
        raw_stats = stats.to_raw()
        return s.ctx.unit_proc.calc_spell_vars_for_level(
            self.id, s.ctx.base_stats.stars, raw_stats
        )


@dataclass
class UnitQuirksDamage:
    phys: float = 0
    magic: float = 0
    true: float = 0


class NoopUnitQuirks(UnitQuirks):
    def get_spell_damage(self, s: SimState) -> dict:
        return dict()


class ItemQuirks(SimSystem):
    id: str

    notes: list[str] = []

    def __init__(self, logger: "Logger"):
        super().__init__()

        self.logger = logger

    def _calc_spell_vars(self, s: SimState):
        # @todo
        pass

    def _constants(self, s: SimState):
        return {
            k: v["mValue"] for k, v in s.ctx.item_info[self.id]["constants"].items()
        }


class TraitQuirks(SimSystem):
    id: str

    notes: list[str] = []

    def __init__(self, logger: "Logger"):
        super().__init__()

        self.logger = logger

    def _eb(self, s: SimState):
        return s.ctx.trait_inventory[self.id].effects_bonus

    def _em(self, s: SimState):
        return s.ctx.trait_inventory[self.id].effects_main
