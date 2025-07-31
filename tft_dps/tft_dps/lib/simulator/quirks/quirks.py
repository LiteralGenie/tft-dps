import abc

import loguru

from tft_dps.lib.simulator.sim_state import SimState, SimStats
from tft_dps.lib.simulator.sim_system import SimSystem


class UnitQuirks(SimSystem):
    id: str

    notes: list[str] = []

    def __init__(self, logger: loguru.Logger):
        super().__init__()

        self.logger = logger

    def get_auto_damage(self, s: "SimState") -> dict:
        return dict(
            physical=s.stats.ad,
            magical=0,
        )

    @abc.abstractmethod
    def get_spell_damage(self, s: "SimState") -> dict: ...

    def get_unit_bonus(self, s: "SimState") -> "SimStats":
        return SimStats.zeros()

    def _calc_spell_vars(self, s: "SimState"):
        raw_stats = s.stats.to_raw()
        return s.ctx.unit_proc.calc_spell_vars_for_level(
            self.id, s.ctx.base_stats.stars, raw_stats
        )

    def run(self, s: SimState):
        pass
