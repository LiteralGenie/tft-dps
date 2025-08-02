import abc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from loguru import Logger

from tft_dps.lib.simulator.sim_state import SimState, SimStats
from tft_dps.lib.simulator.sim_system import SimSystem


class UnitQuirks(SimSystem):
    id: str

    notes: list[str] = []

    def __init__(self, logger: "Logger"):
        super().__init__()

        self.logger = logger

    def get_auto_damage(self, s: SimState, stats: SimStats) -> dict:
        return dict(
            physical=stats.effective_ad * stats.crit_bonus,
        )

    @abc.abstractmethod
    def get_spell_damage(self, s: SimState, stats: SimStats) -> dict: ...

    def _calc_spell_vars(self, s: SimState, stats: SimStats):
        raw_stats = stats.to_raw()
        return s.ctx.unit_proc.calc_spell_vars_for_level(
            self.id, s.ctx.base_stats.stars, raw_stats
        )


class NoopUnitQuirks(UnitQuirks):
    def get_spell_damage(self, s: SimState) -> dict:
        return dict()


class ItemQuirks(SimSystem):
    id: str

    notes: list[str] = []

    def __init__(self, logger: "Logger"):
        super().__init__()

        self.logger = logger

    @abc.abstractmethod
    def get_stat_bonus(self, s: SimState) -> SimStats: ...

    def _calc_spell_vars(self, s: SimState):
        # @todo
        pass

    def info(self, s: SimState):
        return s.ctx.item_info[self.id]
