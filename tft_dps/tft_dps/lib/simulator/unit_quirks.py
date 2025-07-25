import abc
from typing import TYPE_CHECKING

from .sim_state import SimState, SimStats
from .sim_system import SimSystem

if TYPE_CHECKING:
    from .sim_state import SimState


class UnitQuirks(SimSystem):
    id: str

    notes: list[str] = []

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


class AatroxQuirks(UnitQuirks):
    id = "Characters/TFT15_Aatrox"

    def get_spell_damage(self, s: "SimState") -> dict:
        spell_vars = self._calc_spell_vars(s)
        return dict(
            physical=spell_vars["addamage"],
            magical=spell_vars["apdamage"],
        )


class EzrealQuirks(UnitQuirks):
    id = "Characters/TFT15_Ezreal"

    def get_spell_damage(self, s: "SimState") -> dict:
        spell_vars = self._calc_spell_vars(s)
        return dict(
            physical=spell_vars["addamage"],
            magical=spell_vars["apdamage"],
        )


class GarenQuirks(UnitQuirks):
    id = "Characters/TFT15_Garen"

    def get_spell_damage(self, s: "SimState") -> dict:
        spell_vars = self._calc_spell_vars(s)
        return dict(
            physical=spell_vars["basespelldamage"] + spell_vars["additionaldamage"],
            magical=0,
        )


class GnarQuirks(UnitQuirks):
    id = "Characters/TFT15_Gnar"

    notes = ["Passive stacks fixed at {gnar_passive_stacks}"]

    BUFF_KEY = "gnar_spell"
    FLAG_KEY = "gnar_passive_stacks"

    def get_spell_damage(self, s: "SimState") -> dict:
        return dict(physical=0, magical=0)

    def run_events(self, s: SimState):
        if s.ctx.unit_id != self.id:
            return

        buff = s.buffs.get(self.BUFF_KEY, None)
        if buff and s.t > buff["until"]:
            self._end_buff(s)
            return

        did_cast = any(ev.type == "cast" for ev in s.events)
        if did_cast:
            self._start_buff(s)
            return

    def get_unit_bonus(self, s: SimState) -> SimStats:
        spell_vars = self._calc_spell_vars(s)

        bonus = SimStats.zeros()
        bonus.speed = (
            s.ctx.flags["gnar_passive_stacks"] * spell_vars["as_per_stack"] * 100
        )

        if self.BUFF_KEY in s.buffs:
            bonus.ad += spell_vars["gnarad"] * 100

        return bonus

    def _start_buff(self, s: SimState):
        spell_vars = self._calc_spell_vars(s)

        s.buffs[self.BUFF_KEY] = dict(until=s.t + spell_vars["spell_duration"])
        s.mana_locks += 1
        s.stats.mana = 0

    def _end_buff(self, s: SimState):
        del s.buffs[self.BUFF_KEY]
        s.mana_locks -= 1


class KalistaQuirks(UnitQuirks):
    id = "Characters/TFT15_Kalista"

    def get_spell_damage(self, s: "SimState") -> dict:
        spell_vars = self._calc_spell_vars(s)
        return dict(
            physical=spell_vars["addamage"],
            magical=spell_vars["apdamage"],
        )


class KayleQuirks(UnitQuirks):
    id = "Characters/TFT15_Kayle"

    notes = ["Passive activated every {kayle_wave_frequency} attacks"]

    def get_spell_damage(self, s: "SimState") -> dict:
        spell_vars = self._calc_spell_vars(s)
        return dict(
            physical=spell_vars["addamage"],
            magical=spell_vars["apdamage"],
        )
