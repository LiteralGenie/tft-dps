from tft_dps.lib.simulator.quirks.quirks import UnitQuirks
from tft_dps.lib.simulator.sim_state import (
    SimDamage,
    SimState,
    SimStats,
    sim_damage_auto,
    sim_damage_spell,
)
from tft_dps.lib.simulator.sim_system import SimEvent


class AkaliQuirks(UnitQuirks):
    id = "Characters/TFT15_Akali"

    FLAG_KEY_1 = "akali_strike_targets"
    FLAG_KEY_2 = "akali_dash_targets"
    notes = [
        "Each spell cast triggers {akali_strike_targets} dashes that hit a marked unit and {akali_dash_targets} additional units."
    ]

    def get_spell_damage(self, s: "SimState", stats: SimStats) -> SimDamage:
        svs = self._calc_spell_vars(s, stats)

        num_marks = s.ctx.flags[self.FLAG_KEY_1]
        dmg = num_marks * svs["total_strike_damage"]

        num_secondary_hits = s.ctx.flags[self.FLAG_KEY_2]
        dmg += num_marks * num_secondary_hits * svs["total_dash_damage"]

        return sim_damage_spell(
            s,
            stats,
            ma=dmg,
        )


# @todo: double check ashe damage
class AsheQuirks(UnitQuirks):
    id = "Characters/TFT15_Ashe"

    BUFF_KEY = "ashe_spell"

    def get_auto_damage(self, s: SimState, stats: SimStats) -> SimDamage:
        dmg = stats.effective_ad

        if buff := s.buffs.get(self.BUFF_KEY):
            dmg += buff["bonus_damage"]

        return sim_damage_auto(
            s,
            stats,
            ph=dmg,
        )

    def hook_events(
        self, s: SimState, evs: list[SimEvent], stats: SimStats
    ) -> list | None:
        did_cast = any(ev.type == "cast" for ev in evs)
        if did_cast:
            svs = self._calc_spell_vars(s, stats)
            self._start_buff(s, svs)

        did_auto = any(ev.type == "auto" for ev in evs)
        if did_auto and (buff := s.buffs.get(self.BUFF_KEY)):
            buff["num_autos"] += 1

            if buff["num_autos"] >= buff["total_autos"]:
                self._end_buff(s)

    def _start_buff(self, s: "SimState", svs: dict):
        bonus_damage = svs["totalarrows"] * svs["modifieddamage"]
        s.buffs[self.BUFF_KEY] = dict(
            num_autos=0,
            total_autos=svs["attackcount"],
            bonus_damage=bonus_damage,
        )
        s.mana_locks += 1

    def _end_buff(self, s: "SimState"):
        del s.buffs[self.BUFF_KEY]
        s.mana_locks -= 1


class JarvanIVQuirks(UnitQuirks):
    id = "Characters/TFT15_JarvanIV"

    FLAG_KEY = "jarvan_aoe_targets"
    notes = ["AoE hits {jarvan_aoe_targets}"]

    def get_spell_damage(self, s: "SimState", stats: SimStats) -> SimDamage:
        svs = self._calc_spell_vars(s, stats)
        aoe_mult = s.ctx.flags[self.FLAG_KEY]
        return sim_damage_spell(
            s,
            stats,
            ma=aoe_mult * svs["modifieddamage"],
        )


class JinxQuirks(UnitQuirks):
    id = "Characters/TFT15_Jinx"

    BUFF_KEY = "jinx_spell"

    def get_spell_damage(self, s: "SimState", stats: SimStats) -> SimDamage:
        svs = self._calc_spell_vars(s, stats)

        dmg = svs["modifieddamage"]
        dmg += svs["modifiedrocketaoedamage"]

        return sim_damage_spell(
            s,
            stats,
            ph=dmg,
        )

    def hook_events(
        self, s: SimState, evs: list[SimEvent], stats: SimStats
    ) -> list | None:
        if s.ctx.unit_id != self.id:
            return

        did_auto = any(ev.type == "auto" for ev in evs)
        if did_auto:
            svs = self._calc_spell_vars(s, stats)
            self._start_buff(s, stats, svs)

    def _start_buff(self, s: SimState, stats: SimStats, svs: dict):
        bonus_speed_mult = svs["modifiedasperstack"]

        crit_bonus = svs["aspercrit"] - bonus_speed_mult
        bonus_speed_mult += crit_bonus * stats.crit_rate

        if self.BUFF_KEY not in s.buffs:
            s.buffs[self.BUFF_KEY] = dict(
                bonus_speed_mult=bonus_speed_mult,
            )
        else:
            s.buffs[self.BUFF_KEY]["bonus_speed_mult"] += bonus_speed_mult

        s.buffs[self.BUFF_KEY]["bonus_speed_mult"] = min(
            svs["modifiedmaxas"] / 100, s.buffs[self.BUFF_KEY]["bonus_speed_mult"]
        )

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = None
        if buff := s.buffs.get(self.BUFF_KEY):
            bonus = SimStats.zeros()
            bonus.speed_mult += buff["bonus_speed_mult"]

        return bonus


class KSanteQuirks(UnitQuirks):
    id = "Characters/TFT15_KSante"

    FLAG_KEY = "ksante_allout_delay"
    notes = ["ALL OUT activates after {ksante_allout_delay} seconds"]

    BUFF_KEY = "ksante_allout"

    def hook_init(self, s: SimState, stats: SimStats):
        self.t_wake = s.ctx.flags[self.FLAG_KEY] + 0.001

    def hook_stats_override(self, s: SimState, stats: SimStats):
        if self.BUFF_KEY not in s.buffs:
            stats.cast_time = 3
            stats.mana_max = 90
        else:
            stats.cast_time = 0.5
            stats.mana_max = 30

        return stats

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = None
        if buff := s.buffs.get(self.BUFF_KEY):
            bonus = SimStats.zeros()
            bonus.speed_mult = buff["bonus_speed_mult"]

    def get_spell_damage(self, s: "SimState", stats: SimStats) -> SimDamage:
        svs = self._calc_spell_vars(s, stats)

        dmg = 0
        if buff := s.buffs.get(self.BUFF_KEY):
            dmg = svs["modifiedtankdamage"]
        else:
            dmg = svs["modifiedfighterdamage"]

        return sim_damage_spell(
            s,
            stats,
            ph=dmg,
        )

    def hook_events(
        self, s: SimState, evs: list[SimEvent], stats: SimStats
    ) -> list | None:
        if s.t > s.ctx.flags[self.FLAG_KEY] and self.BUFF_KEY not in s.buffs:
            svs = self._calc_spell_vars(s, stats)
            self._start_buff(s, svs)

    def _start_buff(self, s: SimState, svs: dict):
        bonus_speed_mult = svs["flatasbuff"]

        s.buffs[self.BUFF_KEY] = dict(
            bonus_speed_mult=bonus_speed_mult,
        )


class KarmaQuirks(UnitQuirks):
    id = "Characters/TFT15_Karma"

    FLAG_KEY = "karma_aoe_targets"
    notes = ["AoE hits {karma_aoe_targets}"]

    def get_spell_damage(self, s: "SimState", stats: SimStats) -> SimDamage:
        svs = self._calc_spell_vars(s, stats)
        aoe_mult = s.ctx.flags[self.FLAG_KEY]
        return sim_damage_spell(
            s,
            stats,
            ma=aoe_mult * svs["modifieddamage"],
        )


class LeonaQuirks(UnitQuirks):
    id = "Characters/TFT15_Leona"

    FLAG_KEY_1 = "leona_aoe_targets"
    FLAG_KEY_2 = "leona_sunburst_targets"
    notes = [
        "Primary AoE hits {leona_aoe_targets} units and secondary AoE (sunburst) hits {leona_sunburst_targets} units"
    ]

    def get_spell_damage(self, s: "SimState", stats: SimStats) -> SimDamage:
        svs = self._calc_spell_vars(s, stats)

        aoe_mult_1 = s.ctx.flags[self.FLAG_KEY_1]
        dmg = aoe_mult_1 * svs["modifieddamage"]

        # num_potential = 0
        # if trait := s.ctx.trait_inventory.get("TFT15_BattleAcademia"):
        #     num_potential = trait.effects["numpotential"]

        aoe_mult_2 = s.ctx.flags[self.FLAG_KEY_2]
        dmg += aoe_mult_2 * svs["modifiedsunburstdamage"]

        return sim_damage_spell(
            s,
            stats,
            ma=dmg,
        )


class PoppyQuirks(UnitQuirks):
    id = "Characters/TFT15_Poppy"

    FLAG_KEY_1 = "poppy_shield_duration"
    FLAG_KEY_2 = "poppy_aoe_targets"
    notes = [
        "Spell damage applied {poppy_shield_duration} seconds after casting",
        "AoE hits {poppy_aoe_targets} targets",
    ]

    def hook_stats_override(self, s: SimState, stats: SimStats):
        stats.cast_time = s.ctx.flags[self.FLAG_KEY_1]

    def get_spell_damage(self, s: "SimState", stats: SimStats) -> SimDamage:
        svs = self._calc_spell_vars(s, stats)

        dmg = svs["modifieddamage"]

        aoe_mult = s.ctx.flags[self.FLAG_KEY_2]
        dmg += aoe_mult * svs["secondarydamage"]

        return sim_damage_spell(
            s,
            stats,
            ph=dmg,
        )


class RyzeQuirks(UnitQuirks):
    id = "Characters/TFT15_Ryze"

    FLAG_KEY = "ryze_aoe_targets"
    notes = [
        "AoE hits {ryze_aoe_targets} targets",
    ]

    def hook_stats_override(self, s: SimState, stats: SimStats):
        svs = self._calc_spell_vars(s, stats)
        stats.cast_time = svs["duration"]

    def get_spell_damage(self, s: "SimState", stats: SimStats) -> SimDamage:
        svs = self._calc_spell_vars(s, stats)

        dmg = svs["modifieddamage"]

        aoe_mult = s.ctx.flags[self.FLAG_KEY]
        dmg += aoe_mult * svs["modifiedadditionaldamage"]

        return sim_damage_spell(
            s,
            stats,
            ma=dmg,
        )


class SamiraQuirks(UnitQuirks):
    id = "Characters/TFT15_Samira"

    FLAG_KEY = "samira_aoe_targets"
    notes = [
        "AoE hits {samira_aoe_targets} targets",
    ]

    def get_spell_damage(self, s: "SimState", stats: SimStats) -> SimDamage:
        svs = self._calc_spell_vars(s, stats)

        num_casts = len(s.casts) + 1
        if num_casts % 4 == 0:
            aoe_mult = s.ctx.flags[self.FLAG_KEY]
            dmg = aoe_mult * svs["modifieddamage"]
        else:
            dmg = svs["modifiedqbulletdamage"]

        return sim_damage_spell(
            s,
            stats,
            ph=dmg,
        )


class SettQuirks(UnitQuirks):
    id = "Characters/TFT15_Sett"

    FLAG_KEY_1 = "sett_aoe_targets"
    FLAG_KEY_2 = "sett_spell_heal_mult"
    notes = [
        "AoE hits {sett_aoe_targets} targets",
        "Healing received at any point is assumed to be {sett_spell_heal_mult}x the healing from spell casts",
    ]

    BUFF_KEY = "sett_spell"

    def get_spell_damage(self, s: "SimState", stats: SimStats) -> SimDamage:
        svs = self._calc_spell_vars(s, stats)

        dmg = svs["modifiedflurrydamage"]

        aoe_mult = s.ctx.flags[self.FLAG_KEY_1]
        dmg += aoe_mult * svs["modifiedconedamage"]

        total_healing = svs["modifiedheal"]
        total_healing += s.buffs.get(self.BUFF_KEY, dict()).get("healing", 0)
        dmg += (
            aoe_mult
            * svs["modifiedtruedamage"]
            * (total_healing / svs["healingtreshold"])
        )

        return sim_damage_spell(
            s,
            stats,
            ph=dmg,
        )

    def hook_events(
        self, s: SimState, evs: list[SimEvent], stats: SimStats
    ) -> list | None:
        did_cast = any(ev.type == "cast" for ev in evs)
        if did_cast:
            svs = self._calc_spell_vars(s, stats)
            self._start_buff(s, svs)

    def _start_buff(self, s: SimState, svs: dict):
        s.buffs.setdefault(
            self.BUFF_KEY,
            dict(healing=0),
        )
        s.buffs[self.BUFF_KEY]["healing"] += svs["modifiedheal"]


class VolibearQuirks(UnitQuirks):
    id = "Characters/TFT15_Volibear"

    FLAG_KEY_1 = "volibear_aoe_targets"
    FLAG_KEY_2 = "volibear_slam_frequency"
    notes = [
        "AoE hits {volibear_aoe_targets} targets",
        "Every {volibear_slam_frequency} autos triggers the target-change slam effect",
    ]

    BUFF_KEY = "volibear_spell"

    def get_auto_damage(self, s: SimState, stats: SimStats) -> SimDamage:
        svs = self._calc_spell_vars(s, stats)

        num_autos = len(s.attacks) + 1
        if (num_autos % int(svs["attackstoslam"])) == 0:
            aoe_mult = s.ctx.flags.get(self.FLAG_KEY_1)
            dmg = aoe_mult * svs["slamdamage"]
        else:
            dmg = stats.effective_ad

        return sim_damage_auto(
            s,
            stats,
            ph=dmg,
        )

    def hook_events(
        self, s: SimState, evs: list[SimEvent], stats: SimStats
    ) -> list | None:
        did_cast = any(ev.type == "cast" for ev in evs)
        if did_cast:
            svs = self._calc_spell_vars(s, stats)
            self._start_buff(s, svs)

        if buff := s.buffs.get(self.BUFF_KEY):
            if s.t > buff["until"]:
                self._end_buff(s)

        did_auto = any(ev.type == "auto" for ev in evs)
        is_target_change = (len(s.attacks) % s.ctx.flags[self.FLAG_KEY_2]) == 0
        if did_auto and is_target_change:
            svs = self._calc_spell_vars(s, stats)
            aoe_mult = s.ctx.flags.get(self.FLAG_KEY_1)
            dmg = aoe_mult * svs["slamdamage"] * svs["targetchangepercent"]
            s.misc_damage.append(
                sim_damage_spell(
                    s,
                    stats,
                    ph=dmg,
                )
            )

    def _start_buff(self, s: SimState, svs: dict):
        s.buffs[self.BUFF_KEY] = dict(
            until=s.t + svs["duration"],
            bonus_speed=svs["attackspeed"] * 100,
        )
        s.mana_locks += 1

        self.t_wake = s.buffs[self.BUFF_KEY]["until"] + 0.001

    def _end_buff(self, s: SimState):
        del s.buffs[self.BUFF_KEY]
        s.mana_locks -= 1
        self.t_wake = 999

    def get_unit_bonus(self, s: SimState) -> SimStats | None:
        bonus = None

        if buff := s.buffs.get(self.BUFF_KEY):
            bonus = SimStats.zeros()
            bonus.speed = buff["bonus_speed"]

        return bonus


class YuumiQuirks(UnitQuirks):
    id = "Characters/TFT15_Yuumi"

    def get_spell_damage(self, s: "SimState", stats: SimStats) -> SimDamage:
        svs = self._calc_spell_vars(s, stats)

        num_potential = 0
        if trait := s.ctx.trait_inventory.get("TFT15_BattleAcademia"):
            num_potential = trait.effects_bonus["numpotential"]

        num_casts = len(s.casts) + 1
        num_pages = svs["basenumberofpageslaunched"]
        num_pages += num_casts * svs["baseadditionalpages"]

        base_dmg = num_pages * svs["modifieddamage"]

        num_bonus_pages = num_pages / 5.0
        potential_dmg = (
            num_bonus_pages
            * num_potential
            * svs["percentpagedamageperpotential"]
            * svs["modifieddamage"]
        )

        return sim_damage_spell(
            s,
            stats,
            ph=base_dmg,
            tr=potential_dmg,
        )
