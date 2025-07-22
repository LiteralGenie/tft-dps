import abc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lib.simulator.sim_state import SimState


class UnitQuirks(abc.ABC):
    id = str

    def get_auto_damage(self, s: "SimState") -> dict:
        return dict(
            physical=s.stats.ad,
            magical=0,
        )

    @abc.abstractmethod
    def get_spell_damage(self, s: "SimState") -> dict: ...

    def _format_stats_for_unit_proc(self, s: "SimState"):
        st = s.stats
        return {
            0: st.ap,
            1: 0,  # st.armor,
            2: st.ad,  # attack damage
            3: 0,
            4: st.speed,  # attack speed
            6: [round(getf(root_record, "baseSpellBlock", 0), 5)]
            * 5,  # magic resistance
            7: [round(getf(root_record, "baseMoveSpeed", 0), 5)] * 5,  # move speed
            8: [round(getf(root_record, "baseCritChance", 0), 5)] * 5,  # crit chance
            9: [round(getf(root_record, "critDamageMultiplier", 0), 5)]
            * 5,  # crit damage
            12: [
                round(getf(root_record, "baseHP", 0) * self.hp_coef[i], 5)
                for i in range(5)
            ],  # max health
            29: [round(getf(root_record, "attackRange", 0), 5)] * 5,  # attack range
            34: [1] * 5,  # dodge chance
        }
