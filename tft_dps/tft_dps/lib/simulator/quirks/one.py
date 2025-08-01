from typing import TYPE_CHECKING

from tft_dps.lib.simulator.quirks.quirks import UnitQuirks

from ..sim_state import SimState, SimStats

if TYPE_CHECKING:
    from ..sim_state import SimState


class AatroxQuirks(UnitQuirks):
    id = "Characters/TFT15_Aatrox"

    def get_spell_damage(self, s: "SimState") -> dict:
        svs = self._calc_spell_vars(s)
        return dict(
            physical=svs["totaldamage"],
        )


class EzrealQuirks(UnitQuirks):
    id = "Characters/TFT15_Ezreal"

    BUFF_KEY = "ezreal_spell"

    def get_spell_damage(self, s: "SimState") -> dict:
        svs = self._calc_spell_vars(s)
        return dict(
            physical=svs["addamage"],
            magical=svs["apdamage"],
        )

    def get_unit_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()

        svs = self._calc_spell_vars(s)

        num_potential = 0
        if trait := s.ctx.trait_inventory.get("TFT15_BattleAcademia"):
            num_potential = trait.effects["numpotential"]

        if self.BUFF_KEY in s.buffs:
            bonus.speed += num_potential * svs["potential_as"] * 100

        bonus.ad += len(s.casts) * svs["bonusadperpotential"] * num_potential
        bonus.ap += len(s.casts) * svs["bonusapperpotential"] * num_potential

        return bonus

    def run_events(self, s: SimState):
        if s.ctx.unit_id != self.id:
            return

        buff = s.buffs.get(self.BUFF_KEY, None)
        if buff and s.t > buff["until"]:
            self._end_buff(s)

        did_cast = any(ev.type == "cast" for ev in s.events)
        if did_cast:
            self._start_buff(s)

    def _start_buff(self, s: SimState):
        svs = self._calc_spell_vars(s)

        s.buffs[self.BUFF_KEY] = dict(until=s.t + svs["potentialduration"])
        s.stats.mana = 0

    def _end_buff(self, s: SimState):
        del s.buffs[self.BUFF_KEY]


class GarenQuirks(UnitQuirks):
    id = "Characters/TFT15_Garen"

    def get_spell_damage(self, s: "SimState") -> dict:
        svs = self._calc_spell_vars(s)
        return dict(
            physical=svs["additionaldamage"] + svs["additionaldamage"],
        )

    def get_unit_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()

        svs = self._calc_spell_vars(s)

        num_potential = 0
        if trait := s.ctx.trait_inventory.get("TFT15_BattleAcademia"):
            num_potential = trait.effects["numpotential"]

        bonus_hp = len(s.casts) * (
            num_potential * svs["healthperpotential"] + svs["healthgainbase"]
        )
        bonus.health += bonus_hp
        bonus.health_max += bonus_hp

        return bonus


class GnarQuirks(UnitQuirks):
    id = "Characters/TFT15_Gnar"

    notes = ["Passive stacks fixed at {gnar_passive_stacks}"]

    BUFF_KEY = "gnar_spell"
    FLAG_KEY = "gnar_passive_stacks"

    def get_spell_damage(self, s: "SimState") -> dict:
        return dict()

    def run_events(self, s: SimState):
        if s.ctx.unit_id != self.id:
            return

        buff = s.buffs.get(self.BUFF_KEY, None)
        if buff and s.t > buff["until"]:
            self._end_buff(s)

        did_cast = any(ev.type == "cast" for ev in s.events)
        if did_cast:
            self._start_buff(s)

    def get_unit_bonus(self, s: SimState) -> SimStats:
        svs = self._calc_spell_vars(s)

        bonus = SimStats.zeros()
        bonus.speed = s.ctx.flags["gnar_passive_stacks"] * svs["asperstack"] * 100

        if self.BUFF_KEY in s.buffs:
            bonus.ad += svs["gnarad"] * 100

        return bonus

    def _start_buff(self, s: SimState):
        svs = self._calc_spell_vars(s)

        s.buffs[self.BUFF_KEY] = dict(until=s.t + svs["spell_duration"])
        s.mana_locks += 1
        s.stats.mana = 0

    def _end_buff(self, s: SimState):
        del s.buffs[self.BUFF_KEY]
        s.mana_locks -= 1


class KalistaQuirks(UnitQuirks):
    id = "Characters/TFT15_Kalista"

    def get_spell_damage(self, s: "SimState") -> dict:
        svs = self._calc_spell_vars(s)
        return dict(
            physical=svs["totaldamage"],
        )


class KayleQuirks(UnitQuirks):
    id = "Characters/TFT15_Kayle"

    FLAG_KEY_FREQ = "kayle_wave_frequency"
    FLAG_KEY_AOE = "kayle_aoe_targets"
    notes = [
        "Kayle launches waves every {kayle_wave_frequency} attacks",
        "AoE hits {kayle_aoe_targets} targets",
    ]

    def get_auto_damage(self, s: SimState):
        svs = self._calc_spell_vars(s)

        bonus = svs["modifieddamage"]

        num_attacks = len(s.attacks) + 1
        has_wave = (num_attacks % s.ctx.flags[self.FLAG_KEY_FREQ]) == 0
        if has_wave:
            aoe_mult = s.ctx.flags[self.FLAG_KEY_AOE]
            bonus += aoe_mult * svs["ascensionmodifiedmagicdamage"]

        return dict(
            physical=s.stats.ad,
            magical=bonus,
        )

    def get_spell_damage(self, s: "SimState") -> dict:
        return dict()


class KennenQuirks(UnitQuirks):
    id = "Characters/TFT15_Kennen"

    def get_spell_damage(self, s: "SimState") -> dict:
        svs = self._calc_spell_vars(s)
        return dict(
            magical=svs["numjolts"] * svs["modifieddamage"],
        )


class LucianQuirks(UnitQuirks):
    id = "Characters/TFT15_Lucian"

    def get_spell_damage(self, s: "SimState") -> dict:
        svs = self._calc_spell_vars(s)
        return dict(
            magical=svs["numshots"] * svs["modifieddamage"],
        )


class MalphiteQuirks(UnitQuirks):
    id = "Characters/TFT15_Malphite"

    FLAG_KEY = "malphite_aoe_targets"
    notes = ["AoE hits {malphite_aoe_targets}"]

    def get_spell_damage(self, s: "SimState") -> dict:
        svs = self._calc_spell_vars(s)
        aoe_mult = s.ctx.flags[self.FLAG_KEY]
        return dict(
            physical=aoe_mult * svs["modifieddamage"],
        )

    def get_unit_bonus(self, s: SimState) -> SimStats:
        svs = self._calc_spell_vars(s)
        stats = SimStats.zeros()
        stats.armor = svs["bonusresists"] * sum(s.ctx.item_inventory.values())
        return stats


class NaafiriQuirks(UnitQuirks):
    id = "Characters/TFT15_Naafiri"

    def get_spell_damage(self, s: "SimState") -> dict:
        svs = self._calc_spell_vars(s)
        return dict(
            physical=svs["modifieddamage"],
        )


class RellQuirks(UnitQuirks):
    id = "Characters/TFT15_Rell"

    FLAG_KEY = "rell_aoe_targets"
    notes = ["AoE hits {rell_aoe_targets}"]

    def get_spell_damage(self, s: "SimState") -> dict:
        svs = self._calc_spell_vars(s)
        aoe_mult = s.ctx.flags[self.FLAG_KEY]
        return dict(
            magical=aoe_mult * svs["modifieddamage"],
        )


class SivirQuirks(UnitQuirks):
    id = "Characters/TFT15_Sivir"

    FLAG_KEY = "sivir_aoe_targets"
    notes = ["AoE hits {sivir_aoe_targets}"]

    def get_spell_damage(self, s: "SimState") -> dict:
        svs = self._calc_spell_vars(s)
        aoe_mult = s.ctx.flags[self.FLAG_KEY]
        return dict(
            physical=aoe_mult * svs["totaldamage"],
        )


class SyndraQuirks(UnitQuirks):
    id = "Characters/TFT15_Syndra"

    def get_spell_damage(self, s: "SimState") -> dict:
        svs = self._calc_spell_vars(s)
        return dict(
            magical=svs["modifieddamage"],
        )


class ZacQuirks(UnitQuirks):
    id = "Characters/TFT15_Zac"

    FLAG_KEY = "zac_aoe_targets"
    notes = ["AoE hits {zac_aoe_targets}"]

    def get_spell_damage(self, s: "SimState") -> dict:
        svs = self._calc_spell_vars(s)
        aoe_mult = s.ctx.flags[self.FLAG_KEY]
        return dict(
            magical=aoe_mult * svs["finaldamage"],
        )
