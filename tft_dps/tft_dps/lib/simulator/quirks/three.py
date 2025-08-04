import math

from tft_dps.lib.simulator.quirks.quirks import UnitQuirks
from tft_dps.lib.simulator.sim_state import (
    SimDamage,
    SimState,
    SimStats,
    sim_damage_auto,
    sim_damage_spell,
)
from tft_dps.lib.simulator.sim_system import SimEvent


class AhriQuirks(UnitQuirks):
    id = "Characters/TFT15_Ahri"

    FLAG_KEY_1 = "ahri_missing_hp_bonus"
    FLAG_KEY_2 = "ahri_overkill_frequency"
    notes = [
        "Bonus spell damage from missing health averaged to {ahri_missing_hp_bonus} per cast",
        "Overkill effect is triggered every {ahri_overkill_frequency} casts. Overkill damage is assumed to be zero so only the flat bonus is added.",
    ]

    def get_spell_damage(self, s: SimState, stats: SimStats) -> SimDamage:
        svs = self._calc_spell_vars(s, stats)

        dmg = svs["modifieddamage"] * (1 + s.ctx.flags[self.FLAG_KEY_1])

        num_casts = len(s.casts) + 1
        if (num_casts % s.ctx.flags[self.FLAG_KEY_2]) == 0:
            dmg += svs["overkilltargetspreadcount"] * svs["modifiedsecondarydamage"]

        return sim_damage_spell(
            s,
            stats,
            ma=dmg,
        )


class CaitlynQuirks(UnitQuirks):
    id = "Characters/TFT15_Caitlyn"

    def get_spell_damage(self, s: SimState, stats: SimStats) -> SimDamage:
        svs = self._calc_spell_vars(s, stats)

        dmg = svs["totaldamage"]

        num_potential = 0
        if trait := s.ctx.trait_inventory.get("TFT15_BattleAcademia"):
            num_potential = trait.effects_bonus["numpotential"]

        num_bounces = svs["numbounces"] + num_potential * svs["bouncesperpotential"]
        dmg += num_bounces * svs["modifiedsecondarydamage"]

        return sim_damage_spell(
            s,
            stats,
            ph=dmg,
        )


class DariusQuirks(UnitQuirks):
    id = "Characters/TFT15_Darius"

    FLAG_KEY_1 = "darius_spell_bonus_mult"
    FLAG_KEY_2 = "darius_kill_frequency"
    notes = [
        "Bonus spell damage from targeting tanks is averaged to {darius_spell_bonus_mult} of original bonus per cast",
        "On-kill bonus cast is triggered every {darius_kill_frequency} casts.",
    ]

    def get_spell_damage(self, s: SimState, stats: SimStats) -> SimDamage:
        svs = self._calc_spell_vars(s, stats)

        dmg = svs["modifieddamage"]

        dmg *= 1 + svs["tankdamageincrease"] * s.ctx.flags[self.FLAG_KEY_1]

        num_casts = len(s.casts) + 1
        if (num_casts % s.ctx.flags[self.FLAG_KEY_2]) == 0:
            dmg *= 1 + svs["percentdamagefalloff"]

        return sim_damage_spell(
            s,
            stats,
            ph=dmg,
        )


class JayceQuirks(UnitQuirks):
    id = "Characters/TFT15_Jayce"

    FLAG_KEY = "jayce_aoe_targets"
    notes = ["AoE hits {jayce_aoe_targets}"]

    def get_spell_damage(self, s: SimState, stats: SimStats) -> SimDamage:
        svs = self._calc_spell_vars(s, stats)

        dmg = svs["totaldamage"] * s.ctx.flags[self.FLAG_KEY]

        num_potential = 0
        if trait := s.ctx.trait_inventory.get("TFT15_BattleAcademia"):
            num_potential = trait.effects_bonus["numpotential"]

        dmg += num_potential * svs["modifiedsparkdamage"]

        return sim_damage_spell(
            s,
            stats,
            ph=dmg,
        )


class MalzaharQuirks(UnitQuirks):
    id = "Characters/TFT15_Malzahar"

    BUFF_KEY = "malz_spell"

    def hook_events(
        self, s: "SimState", evs: list[SimEvent], stats: SimStats
    ) -> list | None:
        did_cast = any(ev.type == "cast" for ev in evs)
        if did_cast:
            svs = self._calc_spell_vars(s, stats)
            self._start_dot(s, svs)

        t_wake = 999

        for dot in s.buffs.get(self.BUFF_KEY, []):
            rem_ticks = dot["ticks_total"] - dot["ticks_applied"]
            if rem_ticks <= 0:
                continue

            num_to_apply = int((s.t - dot["start"]) / dot["tick_rate"])
            for _ in range(min(num_to_apply, rem_ticks)):
                s.misc_damage.append(
                    sim_damage_spell(
                        s,
                        stats,
                        ma=dot["tick_damage"],
                    )
                )
                dot["ticks_applied"] += 1

            t_wake = min(
                int((num_to_apply + 1) * dot["tick_rate"]),
                t_wake,
            )

        self.t_wake = t_wake

    def _start_dot(self, s: SimState, svs: dict):
        num_ticks = math.ceil(svs["duration"] / svs["tickrate"])
        tick_damage = svs["modifieddamage"] / num_ticks

        s.buffs.setdefault(self.BUFF_KEY, [])
        s.buffs[self.BUFF_KEY].append(
            dict(
                start=s.t,
                ticks_applied=0,
                ticks_total=num_ticks,
                tick_damage=tick_damage,
                tick_rate=svs["tickrate"],
            )
        )


class NeekoQuirks(UnitQuirks):
    id = "Characters/TFT15_Neeko"

    FLAG_KEY = "neeko_aoe_targets"
    notes = ["AoE hits {neeko_aoe_targets}"]

    def get_spell_damage(self, s: SimState, stats: SimStats) -> SimDamage:
        svs = self._calc_spell_vars(s, stats)
        aoe_mult = s.ctx.flags[self.FLAG_KEY]
        return sim_damage_spell(
            s,
            stats,
            ma=aoe_mult * svs["modifieddamage"],
        )


class SennaQuirks(UnitQuirks):
    id = "Characters/TFT15_Senna"

    FLAG_KEY = "senna_aoe_targets"
    notes = ["AoE hits {senna_aoe_targets}"]

    def hook_stats_override(self, s: SimState, stats: SimStats):
        stats.cast_time = 1.25

    def get_spell_damage(self, s: SimState, stats: SimStats) -> SimDamage:
        svs = self._calc_spell_vars(s, stats)

        dmg = svs["totaldamage"]

        aoe_mult = s.ctx.flags[self.FLAG_KEY] - 1
        dmg *= 1 + aoe_mult * svs["reductionaftertwo"]

        return sim_damage_spell(
            s,
            stats,
            ph=dmg,
        )


class SwainQuirks(UnitQuirks):
    id = "Characters/TFT15_Swain"

    FLAG_KEY = "swain_aoe_targets"
    notes = ["AoE hits {swain_aoe_targets}"]

    BUFF_KEY = "swain_spell"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = None

        if buff := s.buffs.get(self.BUFF_KEY):
            bonus = SimStats.zeros()
            bonus.health_max = buff["bonus_health_max"]

        return bonus

    def hook_main(self, s: SimState, stats: SimStats) -> list | None:
        buff = s.buffs.get(self.BUFF_KEY)
        if not buff:
            return

        elapsed = s.t - buff["start"]
        num_ticks = int(elapsed)
        rem_ticks = num_ticks - buff["ticks_applied"]
        for _ in range(rem_ticks):
            s.misc_damage.append(
                sim_damage_spell(
                    s,
                    stats,
                    ma=buff["tick_damage"],
                )
            )
            buff["ticks_applied"] += 1

        self.t_wake = num_ticks + 1

    def hook_events(
        self, s: "SimState", evs: list[SimEvent], stats: SimStats
    ) -> list | None:
        did_cast = any(ev.type == "cast" for ev in evs)
        if did_cast:
            svs = self._calc_spell_vars(s, stats)
            self._start_buff(s, svs)

    def _start_buff(self, s: SimState, svs: dict):
        if self.BUFF_KEY not in s.buffs:
            bonus_health_max = svs["modifiedinitialhealth"]
            s.buffs[self.BUFF_KEY] = dict(
                start=s.t,
                ticks_applied=0,
                tick_damage=svs["modifieddamage"],
                bonus_health_max=bonus_health_max,
            )
        else:
            s.buffs[self.BUFF_KEY]["tick_damage"] += svs["modifiedsecondarydamage"]


class UdyrQuirks(UnitQuirks):
    id = "Characters/TFT15_Udyr"

    FLAG_KEY = "udyr_aoe_targets"
    notes = ["AoE hits {udyr_aoe_targets}"]

    BUFF_KEY = "udyr_spell"

    def get_auto_damage(self, s: SimState, stats: SimStats) -> SimDamage:
        bonus = 0
        if buff := s.buffs.get(self.BUFF_KEY):
            aoe_mult = s.ctx.flags[self.FLAG_KEY]
            bonus = aoe_mult * buff["damage"]

        return sim_damage_auto(
            s,
            stats,
            ph=stats.effective_ad + bonus,
        )

    def hook_events(
        self, s: "SimState", evs: list[SimEvent], stats: SimStats
    ) -> list | None:
        if s.ctx.unit_id != self.id:
            return

        did_auto = any(ev.type == "auto" for ev in evs)
        if did_auto:
            buff = s.buffs.get(self.BUFF_KEY, None)
            if buff:
                buff["num_autos"] += 1

                if buff["num_autos"] >= buff["total_autos"]:
                    self._end_buff(s)

        did_cast = any(ev.type == "cast" for ev in evs)
        if did_cast:
            svs = self._calc_spell_vars(s, stats)
            self._start_buff(s, svs)

    def _start_buff(self, s: SimState, svs: dict):
        s.buffs[self.BUFF_KEY] = dict(
            num_autos=0,
            total_autos=svs["numattacks"],
            damage=svs["modifiedaoedamage"],
        )
        s.mana_locks += 1

    def _end_buff(self, s: SimState):
        del s.buffs[self.BUFF_KEY]
        s.mana_locks -= 1


class ViegoQuirks(UnitQuirks):
    id = "Characters/TFT15_Viego"

    BUFF_KEY = "viego_spell"

    def get_auto_damage(self, s: SimState, stats: SimStats) -> SimDamage:
        svs = self._calc_spell_vars(s, stats)

        bonus = svs["modifiedpassivedamage"]
        if buff := s.buffs.get(self.BUFF_KEY):
            bonus += buff["damage"][buff["num_autos"]]

        return sim_damage_auto(
            s,
            stats,
            ph=stats.effective_ad,
            ma=bonus,
        )

    def hook_events(
        self, s: "SimState", evs: list[SimEvent], stats: SimStats
    ) -> list | None:
        if s.ctx.unit_id != self.id:
            return

        did_cast = any(ev.type == "cast" for ev in evs)
        if did_cast:
            svs = self._calc_spell_vars(s, stats)
            self._start_buff(s, svs)

        did_auto = any(ev.type == "auto" for ev in evs)
        if did_auto:
            buff = s.buffs.get(self.BUFF_KEY, None)
            if buff:
                buff["num_autos"] += 1

                if buff["num_autos"] >= len(buff["damage"]):
                    self._end_buff(s)

    def _start_buff(self, s: SimState, svs: dict):
        s.buffs[self.BUFF_KEY] = dict(
            num_autos=0,
            damage=[
                svs["modifiedcombodamage"],
                svs["modifiedcombodamage"],
                svs["modifiedfinalcombodamage"],
            ],
        )
        s.mana_locks += 1

    def _end_buff(self, s: SimState):
        del s.buffs[self.BUFF_KEY]
        s.mana_locks -= 1


class YasuoQuirks(UnitQuirks):
    id = "Characters/TFT15_Yasuo"

    def get_spell_damage(self, s: SimState, stats: SimStats) -> SimDamage:
        svs = self._calc_spell_vars(s, stats)
        return sim_damage_spell(
            s,
            stats,
            ph=svs["numtargets"] * svs["totaldamage"],
        )


class ZiggsQuirks(UnitQuirks):
    id = "Characters/TFT15_Ziggs"

    FLAG_KEY = "ziggs_aoe_targets"
    notes = ["AoE hits {ziggs_aoe_targets}"]

    def get_spell_damage(self, s: SimState, stats: SimStats) -> SimDamage:
        svs = self._calc_spell_vars(s, stats)
        aoe_mult = s.ctx.flags[self.FLAG_KEY]
        return sim_damage_spell(
            s,
            stats,
            ma=aoe_mult * svs["modifiedexplosiondamage"],
        )

    def get_auto_damage(self, s: SimState, stats: SimStats) -> SimDamage:
        svs = self._calc_spell_vars(s, stats)
        return sim_damage_auto(
            s,
            stats,
            ma=svs["totalattackdamage"],
        )


# class KogMawQuirks(UnitQuirks):
#     id = "Characters/TFT15_KogMaw"

#     FLAG_KEY = "kogmaw_trainer_level"
#     notes = ["Trainer Leve {ziggs_aoe_targets}"]

#     def get_spell_damage(self, s: SimState, stats: SimStats) -> SimDamage:
#         svs = self._calc_spell_vars(s, stats)
#         return dict()


# class SmolderQuirks(UnitQuirks):
#     id = "Characters/TFT15_Smolder"

#     def get_spell_damage(self, s: SimState, stats: SimStats) -> SimDamage:
#         svs = self._calc_spell_vars(s, stats)
#         return dict()


# class RammusQuirks(UnitQuirks):
#     id = "Characters/TFT15_Rammus"

#     def get_spell_damage(self, s: SimState, stats: SimStats) -> SimDamage:
#         svs = self._calc_spell_vars(s, stats)
#         return dict()
