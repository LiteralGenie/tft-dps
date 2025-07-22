from lib.simulator.sim_state import SimState
from lib.simulator.unit_quirks import UnitQuirks


class AatroxQuirks(UnitQuirks):
    id = "Characters/TFT15_Aatrox"

    def get_spell_damage(self, s: SimState) -> dict:
        raw_stats = s.stats.to_raw()
        spell_vars = s.ctx.unit_proc.calc_spell_vars_for_level(
            self.id, s.ctx.stats.stars, raw_stats
        )
        return dict(
            physical=spell_vars["addamage"],
            magical=spell_vars["apdamage"],
        )
