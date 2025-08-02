from tft_dps.lib.simulator.quirks.quirks import UnitQuirks, UnitQuirksDamage
from tft_dps.lib.simulator.sim_state import SimState, SimStats
from tft_dps.lib.simulator.sim_system import SimEvent


class BraumQuirks(UnitQuirks):
    id = "Characters/TFT15_Braum"

    FLAG_KEY_1 = "braum_aoe_targets_primary"
    FLAG_KEY_2 = "braum_aoe_targets_secondary"
    FLAG_KEY_3 = "braum_execute_bonus"
    notes = [
        "Primary AoE (spin) hits {braum_aoe_targets_primary} units",
        "Secondary AoE (throw) hits {braum_aoe_targets_secondary} units",
        "Execute damage is calculated as true damage equal to ({braum_execute_bonus} * execute_threshold) of the single-target damage",
    ]

    def hook_stats_override(self, s: SimState, stats: SimStats):
        svs = self._calc_spell_vars(s, stats)
        stats.cast_time = svs["duration"]

    def get_spell_damage(self, s: SimState, stats: SimStats) -> UnitQuirksDamage:
        svs = self._calc_spell_vars(s, stats)

        dmg = svs["modifieddamage"]

        aoe_mult_1 = s.ctx.flags[self.FLAG_KEY_1]
        dmg += aoe_mult_1 * svs["modifiedaoedamage"]

        aoe_mult_2 = s.ctx.flags[self.FLAG_KEY_2]
        dmg += aoe_mult_2 * svs["modifiedthrowdamage"]

        bonus_frac = s.ctx.flags[self.FLAG_KEY_3]
        execute_dmg = bonus_frac * svs["executethresholdap"] * svs["modifieddamage"]

        return UnitQuirksDamage(
            phys=dmg,
            true=execute_dmg,
        )


class GwenQuirks(UnitQuirks):
    id = "Characters/TFT15_Gwen"

    FLAG_KEY_1 = "gwen_aoe_targets_spell"
    FLAG_KEY_2 = "gwen_aoe_targets_auto"
    notes = [
        "Spell AoE hits {gwen_aoe_targets_spell} units",
        "Auto attack AoE hits {gwen_aoe_targets_auto} units",
    ]

    def get_spell_damage(self, s: SimState, stats: SimStats) -> UnitQuirksDamage:
        svs = self._calc_spell_vars(s, stats)

        num_casts = len(s.casts) + 1
        if num_casts % 3 == 0:
            dmg = svs["needlecount"] * svs["modifiedneedledamage"]
        else:
            dmg = svs["modifieddivideddamage"]
            dmg += svs["modifiedburstdamage"]
            dmg *= 1 + svs["threadincrease"]

        return UnitQuirksDamage(
            magic=dmg,
        )

    def get_auto_damage(self, s: SimState, stats: SimStats) -> UnitQuirksDamage:
        svs = self._calc_spell_vars(s, stats)

        aoe_mult = s.ctx.flags[self.FLAG_KEY_2]
        dmg = aoe_mult * svs["modifiedconedamage"]
        dmg *= stats.crit_bonus

        return UnitQuirksDamage(
            magic=dmg,
        )


# class LeeSinQuirks(UnitQuirks):
#     id = "Characters/TFT15_LeeSin"


# class SeraphineQuirks(UnitQuirks):
#     id = "Characters/TFT15_Seraphine"

#     FLAG_KEY = "seraphine_aoe_targets_spell"
#     notes = [
#         "AoE hits {seraphine_aoe_targets_spell} units",
#     ]

#     def get_spell_damage(self, s: SimState, stats: SimStats) -> UnitQuirksDamage:
#         return super().get_spell_damage(s)


class TwistedFateQuirks(UnitQuirks):
    id = "Characters/TFT15_TwistedFate"

    BUFF_KEY = "tf_spell"

    def get_auto_damage(self, s: SimState, stats: SimStats) -> UnitQuirksDamage:
        svs = self._calc_spell_vars(s, stats)

        crit_bonus = stats.crit_bonus

        phys = svs["attacknumenemies"] * stats.effective_ad * crit_bonus

        magic = 0
        for idx in range(int(svs["attacknumenemies"])):
            reduction = (1 - svs["multattackdamagereduction"]) ** idx
            magic += svs["modifiedpassivedamage"] * reduction * crit_bonus

        return UnitQuirksDamage(
            phys=phys,
            magic=magic,
        )

    def hook_events(
        self, s: SimState, evs: list[SimEvent], stats: SimStats
    ) -> list | None:
        did_auto = any(ev.type == "auto" for ev in evs)
        if did_auto:
            svs = self._calc_spell_vars(s, stats)
            self._end_buff(s, svs)

        did_cast = any(ev.type == "cast" for ev in evs)
        if did_cast:
            svs = self._calc_spell_vars(s, stats)
            self._end_buff(s, svs)

    def _start_buff(self, s: SimState, svs: dict):
        s.buffs.setdefault(
            self.BUFF_KEY,
            dict(marks=0),
        )
        s.buffs[self.BUFF_KEY] += svs["attacknumenemies"]

    def _end_buff(self, s: SimState, svs: dict):
        s.buffs.setdefault(
            self.BUFF_KEY,
            dict(marks=0),
        )
        s.buffs[self.BUFF_KEY]["marks"] = 0

    def get_spell_damage(self, s: SimState, stats: SimStats) -> UnitQuirksDamage:
        svs = self._calc_spell_vars(s, stats)

        phys = svs["modifieddamage"] * svs["spellnumenemies"]

        num_marks = s.buffs.get(self.BUFF_KEY, dict()).get("marks", 0)
        magical = num_marks * svs["modifiedpassivedamage"]

        return UnitQuirksDamage(
            phys=phys,
            magic=magical,
        )


# class VarusQuirks(UnitQuirks):
#     id = "Characters/TFT15_Varus"


class YoneQuirks(UnitQuirks):
    id = "Characters/TFT15_Yone"

    FLAG_KEY = "yone_aoe_targets"
    notes = [
        "AoE hits {yone_aoe_targets} units total",
    ]

    BUFF_KEY = "yone_spell"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        bonus.speed = s.buffs.get(self.BUFF_KEY, dict()).get("bonus_speed", 0)
        return bonus

    def get_spell_damage(self, s: SimState, stats: SimStats) -> UnitQuirksDamage:
        svs = self._calc_spell_vars(s, stats)

        aoe_mult = s.ctx.flags[self.FLAG_KEY]
        dmg = aoe_mult * svs["modifiedstrikedamage"]

        return UnitQuirksDamage(
            phys=dmg,
        )

    def get_auto_damage(self, s: SimState, stats: SimStats) -> UnitQuirksDamage:
        svs = self._calc_spell_vars(s, stats)

        num_autos = len(s.attacks) + 1
        if (num_autos % 2) == 0:
            dmg = UnitQuirksDamage(
                true=svs["modifiedattacktruedamage"] * stats.crit_bonus,
            )
        else:
            dmg = UnitQuirksDamage(
                magic=svs["modifiedattackmagicdamage"] * stats.crit_bonus,
            )

        return dmg

    def hook_events(
        self, s: SimState, evs: list[SimEvent], stats: SimStats
    ) -> list | None:
        did_auto = any(ev.type == "auto" for ev in evs)
        if did_auto:
            svs = self._calc_spell_vars(s, stats)
            self._start_buff(s, svs)

    def _start_buff(self, s: SimState, svs: dict):
        s.buffs.setdefault(
            self.BUFF_KEY,
            dict(bonus_speed=0),
        )
        s.buffs[self.BUFF_KEY]["bonus_speed"] += svs["asperattack"] * 100


class ZyraQuirks(UnitQuirks):
    id = "Characters/TFT15_Zyra"

    FLAG_KEY = "zyra_decay"
    notes = [
        "Attack speed bonus from spell averaged to {zyra_decay} of initial bonus",
    ]

    BUFF_KEY = "zyra_spell"

    def get_spell_damage(self, s: SimState, stats: SimStats) -> UnitQuirksDamage:
        svs = self._calc_spell_vars(s, stats)

        dmg = svs["modifieddamage"] * svs["numplants"] * svs["summonattacks"]

        return UnitQuirksDamage(
            magic=dmg,
        )

    def hook_events(
        self, s: SimState, evs: list[SimEvent], stats: SimStats
    ) -> list | None:
        did_cast = any(ev.type == "cast" for ev in evs)
        if did_cast:
            svs = self._calc_spell_vars(s, stats)
            self._start_buff(s, svs)

    def _start_buff(self, s: SimState, svs: dict):
        s.buffs[self.BUFF_KEY] = dict(
            bonus_speed=svs["flatteamas"] + svs["bonusas"],
        )

    def get_unit_bonus(self, s: SimState) -> SimStats | None:
        bonus = None

        if buff := s.buffs.get(self.BUFF_KEY):
            bonus = SimStats.zeros()
            bonus.speed = buff["bonus_speed"] * s.ctx.flags[self.FLAG_KEY]

        return bonus
