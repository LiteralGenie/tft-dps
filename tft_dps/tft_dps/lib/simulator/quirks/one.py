from typing import TYPE_CHECKING

from tft_dps.lib.simulator.quirks.quirks import UnitQuirks
from tft_dps.lib.simulator.sim_event import SimEvent
from tft_dps.lib.simulator.sim_state import SimState, SimStats

from ..sim_state import SimStats

if TYPE_CHECKING:
    from ..sim_state import SimState, SimStats


class AatroxQuirks(UnitQuirks):
    id = "Characters/TFT15_Aatrox"

    def get_spell_damage(self, s: "SimState", stats: SimStats) -> dict:
        svs = self._calc_spell_vars(s, stats)
        return dict(
            physical=svs["totaldamage"],
        )


class EzrealQuirks(UnitQuirks):
    id = "Characters/TFT15_Ezreal"

    BUFF_KEY_ACTIVE = "ezreal_spell_active"
    BUFF_KEY_PASSIVE = "ezreal_spell_passive"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()

        if active := s.buffs.get(self.BUFF_KEY_ACTIVE):
            bonus.speed_mult += active["bonus_speed_mult"]
        if passive := s.buffs.get(self.BUFF_KEY_ACTIVE):
            bonus.ad_mult += passive["bonus_ad_mult"]
            bonus.ap += passive["bonus_ap"]

        return bonus

    def get_spell_damage(self, s: "SimState", stats: SimStats) -> dict:
        svs = self._calc_spell_vars(s, stats)
        return dict(
            physical=svs["addamage"],
            magical=svs["apdamage"],
        )

    def hook_events(
        self, s: "SimState", evs: list[SimEvent], stats: SimStats
    ) -> list | None:
        buff = s.buffs.get(self.BUFF_KEY_ACTIVE, None)
        if buff and s.t > buff["until"]:
            self._end_active_buff(s)

        did_cast = any(ev.type == "cast" for ev in evs)
        if did_cast:
            svs = self._calc_spell_vars(s, stats)
            self._start_active_buff(s, stats, svs)
            self._increment_passive_buff(s, stats, svs)

    def _start_active_buff(self, s: "SimState", stats: SimStats, svs: dict):
        num_potential = 0
        if trait := s.ctx.trait_inventory.get("TFT15_BattleAcademia"):
            num_potential = trait.effects["numpotential"]

        bonus_speed_mult = num_potential * svs["potentialas"]

        s.buffs[self.BUFF_KEY_ACTIVE] = dict(
            until=s.t + svs["potentialduration"],
            bonus_speed_mult=bonus_speed_mult,
        )

    def _end_active_buff(self, s: "SimState"):
        del s.buffs[self.BUFF_KEY_ACTIVE]

    def _increment_passive_buff(self, s: "SimState", stats: SimStats, svs: dict):
        num_potential = 0
        if trait := s.ctx.trait_inventory.get("TFT15_BattleAcademia"):
            num_potential = trait.effects["numpotential"]

        bonus_ad_mult = svs["bonusadperpotential"] * num_potential
        bonus_ap = svs["bonusapperpotential"] * num_potential

        s.buffs.setdefault(
            self.BUFF_KEY_PASSIVE,
            dict(bonus_ad_mult=0, bonus_ap=0),
        )
        s.buffs[self.BUFF_KEY_PASSIVE]["bonus_ad_mult"] += bonus_ad_mult
        s.buffs[self.BUFF_KEY_PASSIVE]["bonus_ap"] += bonus_ap


class GarenQuirks(UnitQuirks):
    id = "Characters/TFT15_Garen"

    BUFF_KEY = "garen_passive"

    def hook_stats(self, s: SimState) -> SimStats | None:
        if passive := s.buffs.get(self.BUFF_KEY):
            bonus = SimStats.zeros()
            bonus.health_max += passive["bonus_health"]
            return bonus

    def get_spell_damage(self, s: "SimState", stats: SimStats) -> dict:
        svs = self._calc_spell_vars(s, stats)
        return dict(
            physical=svs["additionaldamage"],
        )

    def hook_events(
        self, s: "SimState", evs: list[SimEvent], stats: SimStats
    ) -> list | None:
        if s.ctx.unit_id != self.id:
            return

        did_cast = any(ev.type == "cast" for ev in evs)
        if did_cast:
            svs = self._calc_spell_vars(s, stats)
            self._increment_passive_buff(s, stats, svs)

    def _increment_passive_buff(self, s: "SimState", stats: SimStats, svs: dict):
        num_potential = 0
        if trait := s.ctx.trait_inventory.get("TFT15_BattleAcademia"):
            num_potential = trait.effects["numpotential"]

        bonus_health = num_potential * svs["healthperpotential"] + svs["healthgainbase"]

        s.buffs.setdefault(
            self.BUFF_KEY,
            dict(bonus_health=0),
        )
        s.buffs[self.BUFF_KEY]["bonus_health"] += bonus_health


class GnarQuirks(UnitQuirks):
    id = "Characters/TFT15_Gnar"

    FLAG_KEY = "gnar_passive_stacks"
    notes = ["Passive stacks fixed at {gnar_passive_stacks}"]

    BUFF_KEY_ACTIVE = "gnar_spell_active"
    BUFF_KEY_PASSIVE = "gnar_spell_passive"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()

        if active := s.buffs.get(self.BUFF_KEY_ACTIVE):
            bonus.ad_mult = active["bonus_ad_mult"]

        if passive := s.buffs.get(self.BUFF_KEY_ACTIVE):
            bonus.speed_mult = passive["bonus_speed_mult"]

        return bonus

    def hook_events(
        self, s: "SimState", evs: list[SimEvent], stats: SimStats
    ) -> list | None:
        did_cast = any(ev.type == "cast" for ev in evs)
        if did_cast:
            svs = self._calc_spell_vars(s, stats)
            self._start_active_buff(s, stats, svs)

        buff = s.buffs.get(self.BUFF_KEY_ACTIVE, None)
        if buff and s.t > buff["until"]:
            self._end_active_buff(s)

        self._set_passive_buff(s, stats)

    def _start_active_buff(self, s: "SimState", stats: SimStats, svs: dict):
        s.buffs[self.BUFF_KEY_ACTIVE] = dict(
            until=s.t + svs["spellduration"], bonus_ad_mult=svs["gnarad"]
        )
        s.mana_locks += 1

    def _end_active_buff(self, s: "SimState"):
        del s.buffs[self.BUFF_KEY_ACTIVE]
        s.mana_locks -= 1

    def _set_passive_buff(self, s: "SimState", stats: SimStats):
        if self.BUFF_KEY_PASSIVE not in s.buffs:
            svs = self._calc_spell_vars(s, stats)
            bonus_speed_mult = s.ctx.flags["gnar_passive_stacks"] * svs["asperstack"]
            s.buffs[self.BUFF_KEY_PASSIVE] = dict(
                bonus_speed_mult=bonus_speed_mult,
            )


class KalistaQuirks(UnitQuirks):
    id = "Characters/TFT15_Kalista"

    def get_spell_damage(self, s: "SimState", stats: SimStats) -> dict:
        svs = self._calc_spell_vars(s, stats)
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

    def hook_init(self, s: SimState):
        s.mana_locks += 1

    def get_auto_damage(self, s: SimState, stats: SimStats) -> dict:
        svs = self._calc_spell_vars(s, stats)

        md = svs["modifieddamage"]

        num_attacks = len(s.attacks) + 1
        has_wave = (num_attacks % s.ctx.flags[self.FLAG_KEY_FREQ]) == 0
        if has_wave:
            aoe_mult = s.ctx.flags[self.FLAG_KEY_AOE]
            md += aoe_mult * svs["ascensionmodifiedmagicdamage"]

        return dict(
            physical=stats.effective_ad * stats.crit_bonus,
            magical=md,
        )


class KennenQuirks(UnitQuirks):
    id = "Characters/TFT15_Kennen"

    def get_spell_damage(self, s: "SimState", stats: SimStats) -> dict:
        svs = self._calc_spell_vars(s, stats)
        return dict(
            magical=svs["numjolts"] * svs["modifieddamage"],
        )


class LucianQuirks(UnitQuirks):
    id = "Characters/TFT15_Lucian"

    def get_spell_damage(self, s: "SimState", stats: SimStats) -> dict:
        svs = self._calc_spell_vars(s, stats)
        return dict(
            magical=svs["numshots"] * svs["modifieddamage"],
        )


class MalphiteQuirks(UnitQuirks):
    id = "Characters/TFT15_Malphite"

    FLAG_KEY = "malphite_aoe_targets"
    notes = ["AoE hits {malphite_aoe_targets}"]

    BUFF_KEY = "malphite_spell"

    def hook_stats_override(self, s: SimState, stats: SimStats):
        if self.BUFF_KEY not in s.buffs:
            self._set_passive_buff(s, stats)

    def hook_stats(self, s: SimState) -> SimStats | None:
        if passive := s.buffs.get(self.BUFF_KEY):
            bonus = SimStats.zeros()
            bonus.armor = passive["bonus_armor"]

    def get_spell_damage(self, s: "SimState", stats: SimStats) -> dict:
        svs = self._calc_spell_vars(s, stats)
        aoe_mult = s.ctx.flags[self.FLAG_KEY]
        return dict(
            physical=aoe_mult * svs["modifieddamage"],
        )

    def _set_passive_buff(self, s: "SimState", stats: SimStats):
        svs = self._calc_spell_vars(s, stats)
        s.buffs.setdefault(
            self.BUFF_KEY,
            dict(
                bonus_armor=svs["bonusresists"] * len(s.ctx.item_inventory),
            ),
        )


class NaafiriQuirks(UnitQuirks):
    id = "Characters/TFT15_Naafiri"

    def get_spell_damage(self, s: "SimState", stats: SimStats) -> dict:
        svs = self._calc_spell_vars(s, stats)
        return dict(
            physical=svs["modifieddamage"],
        )


class RellQuirks(UnitQuirks):
    id = "Characters/TFT15_Rell"

    FLAG_KEY = "rell_aoe_targets"
    notes = ["AoE hits {rell_aoe_targets}"]

    def get_spell_damage(self, s: "SimState", stats: SimStats) -> dict:
        svs = self._calc_spell_vars(s, stats)
        aoe_mult = s.ctx.flags[self.FLAG_KEY]
        return dict(
            magical=aoe_mult * svs["modifieddamage"],
        )


class SivirQuirks(UnitQuirks):
    id = "Characters/TFT15_Sivir"

    FLAG_KEY = "sivir_aoe_targets"
    notes = ["AoE hits {sivir_aoe_targets}"]

    def get_spell_damage(self, s: "SimState", stats: SimStats) -> dict:
        svs = self._calc_spell_vars(s, stats)
        aoe_mult = s.ctx.flags[self.FLAG_KEY]
        return dict(
            physical=aoe_mult * svs["totaldamage"],
        )


class SyndraQuirks(UnitQuirks):
    id = "Characters/TFT15_Syndra"

    def get_spell_damage(self, s: "SimState", stats: SimStats) -> dict:
        svs = self._calc_spell_vars(s, stats)
        return dict(
            magical=svs["modifieddamage"],
        )


class ZacQuirks(UnitQuirks):
    id = "Characters/TFT15_Zac"

    FLAG_KEY = "zac_aoe_targets"
    notes = ["AoE hits {zac_aoe_targets}"]

    def get_spell_damage(self, s: "SimState", stats: SimStats) -> dict:
        svs = self._calc_spell_vars(s, stats)
        aoe_mult = s.ctx.flags[self.FLAG_KEY]
        return dict(
            magical=aoe_mult * svs["finaldamage"],
        )
