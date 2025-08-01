import abc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from loguru import Logger

from tft_dps.lib.calc_ctx import CalcCtx
from tft_dps.lib.simulator.sim_state import SimState, SimStats
from tft_dps.lib.simulator.sim_system import SimSystem


class UnitQuirks(SimSystem):
    id: str

    notes: list[str] = []

    def __init__(self, logger: "Logger"):
        super().__init__()

        self.logger = logger

    def get_auto_damage(self, s: SimState) -> dict:
        return dict(
            physical=s.stats.ad,
            magical=0,
        )

    @abc.abstractmethod
    def get_spell_damage(self, s: SimState) -> dict: ...

    def get_unit_bonus(self, s: SimState) -> SimStats | None:
        return None

    def get_stats_override(self, s: SimState, update: SimStats) -> SimStats:
        return update

    def init_ctx(self, ctx: CalcCtx) -> CalcCtx:
        return ctx

    def _calc_spell_vars(self, s: SimState):
        raw_stats = s.stats.to_raw()
        return s.ctx.unit_proc.calc_spell_vars_for_level(
            self.id, s.ctx.base_stats.stars, raw_stats
        )

    def run(self, s: SimState):
        pass


class NoopUnitQuirks(UnitQuirks):
    def get_spell_damage(self, s: SimState) -> dict:
        return dict(
            physical=0,
            magical=0,
        )
