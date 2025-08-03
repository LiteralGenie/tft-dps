from tft_dps.lib.simulator.sim_state import SimState, SimStats
from tft_dps.lib.simulator.sim_system import SimSystem


class CritSystem(SimSystem):
    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus_crit_mult = 0
        if buff := s.buffs.get("spell_crit"):
            bonus_crit_mult = sum(buff[1:])

        if bonus_crit_mult > 0:
            bonus = SimStats.zeros()
            bonus.crit_mult = bonus_crit_mult
            return bonus


def create_spell_crit_buff(s: "SimState", crit_mult_on_dupe: float):
    s.buffs.setdefault("spell_crit", [])
    s.buffs["spell_crit"].append(crit_mult_on_dupe)
    s.buffs["spell_crit"].sort()
