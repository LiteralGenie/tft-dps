import math

from tft_dps.lib.simulator.quirks.quirks import UnitQuirks
from tft_dps.lib.simulator.sim_state import SimMiscDamage, SimState, SimStats


class AhriQuirks(UnitQuirks):
    id = "Characters/TFT15_Ahri"

    FLAG_KEY_1 = "ahri_missing_hp_bonus"
    FLAG_KEY_2 = "ahri_overkill_frequency"
    notes = [
        "Bonus spell damage from missing health averaged to {ahri_missing_hp_bonus} per cast",
        "Overkill effect is triggered every {ahri_overkill_frequency} casts. Overkill damage is assumed to be zero so only the flat bonus is added.",
    ]

    def get_spell_damage(self, s: SimState) -> dict:
        svs = self._calc_spell_vars(s)

        dmg = 0

        dmg += svs["modifieddamage"] * (1 + s.ctx.flags[self.FLAG_KEY_1])

        num_casts = len(s.casts) + 1
        if (num_casts % s.ctx.flags[self.FLAG_KEY_2]) == 0:
            dmg += svs["overkilltargetspreadcount"] * svs["modifiedsecondarydamage"]

        return dict(
            magical=dmg,
        )


class CaitlynQuirks(UnitQuirks):
    id = "Characters/TFT15_Caitlyn"

    def get_spell_damage(self, s: SimState) -> dict:
        svs = self._calc_spell_vars(s)

        dmg = svs["totaldamage"]

        num_potential = 0
        if trait := s.ctx.trait_inventory.get("TFT15_BattleAcademia"):
            num_potential = trait.effects["numpotential"]

        num_bounces = svs["numbounces"] + num_potential * svs["bouncesperpotential"]
        dmg += num_bounces * svs["modifiedsecondarydamage"]

        return dict(
            physical=dmg,
        )


class DariusQuirks(UnitQuirks):
    id = "Characters/TFT15_Darius"

    FLAG_KEY_1 = "darius_spell_bonus_mult"
    FLAG_KEY_2 = "darius_kill_frequency"
    notes = [
        "Bonus spell damage from targeting tanks is averaged to {darius_spell_bonus_mult} of original bonus per cast",
        "On-kill bonus cast is triggered every {darius_kill_frequency} casts.",
    ]

    def get_spell_damage(self, s: SimState) -> dict:
        svs = self._calc_spell_vars(s)

        dmg = svs["modifieddamage"]

        dmg *= 1 + svs["tankdamageincrease"] * s.ctx.flags[self.FLAG_KEY_1]

        num_casts = len(s.casts) + 1
        if (num_casts % s.ctx.flags[self.FLAG_KEY_2]) == 0:
            dmg *= 1 + svs["percentdamagefalloff"]

        return dict(
            physical=dmg,
        )


class JayceQuirks(UnitQuirks):
    id = "Characters/TFT15_Jayce"

    FLAG_KEY = "jayce_aoe_targets"
    notes = ["AoE hits {jayce_aoe_targets}"]

    def get_spell_damage(self, s: SimState) -> dict:
        svs = self._calc_spell_vars(s)

        dmg = svs["totaldamage"] * s.ctx.flags[self.FLAG_KEY]

        num_potential = 0
        if trait := s.ctx.trait_inventory.get("TFT15_BattleAcademia"):
            num_potential = trait.effects["numpotential"]

        dmg += num_potential * svs["modifiedsparkdamage"]

        return dict(
            physical=dmg,
        )


class MalzaharQuirks(UnitQuirks):
    id = "Characters/TFT15_Malzahar"

    BUFF_KEY = "malz_spell"

    def get_spell_damage(self, s: SimState) -> dict:
        return dict()

    def run_events(self, s: "SimState"):
        did_cast = any(ev.type == "cast" for ev in s.events)
        if did_cast:
            svs = self._calc_spell_vars(s)
            self._start_dot(s, svs)

        for dot in s.buffs.get(self.BUFF_KEY, []):
            rem_ticks = dot["ticks_total"] - dot["ticks_applied"]
            if rem_ticks <= 0:
                continue

            num_to_apply = int((s.t - dot["start"]) / dot["tick_rate"])
            for _ in range(min(num_to_apply, rem_ticks)):
                s.misc_damage.append(
                    SimMiscDamage(
                        t=s.t,
                        physical_damage=0,
                        magical_damage=dot["tick_damage"],
                        true_damage=0,
                    )
                )
                dot["ticks_applied"] += 1

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

    def get_spell_damage(self, s: SimState) -> dict:
        svs = self._calc_spell_vars(s)
        aoe_mult = s.ctx.flags[self.FLAG_KEY]
        return dict(
            magical=aoe_mult * svs["modifieddamage"],
        )


class SennaQuirks(UnitQuirks):
    id = "Characters/TFT15_Senna"

    FLAG_KEY = "senna_aoe_targets"
    notes = ["AoE hits {senna_aoe_targets}"]

    def get_stats_override(self, s: SimState, update: SimStats) -> SimStats:
        update.cast_time = 1.25
        return update

    def get_spell_damage(self, s: SimState) -> dict:
        svs = self._calc_spell_vars(s)

        dmg = svs["totaldamage"]

        aoe_mult = s.ctx.flags[self.FLAG_KEY] - 1
        dmg *= 1 + aoe_mult * svs["reductionaftertwo"]

        return dict(
            physical=dmg,
        )


class SwainQuirks(UnitQuirks):
    id = "Characters/TFT15_Swain"

    FLAG_KEY = "swain_aoe_targets"
    notes = ["AoE hits {swain_aoe_targets}"]

    BUFF_KEY = "swain_spell"

    def get_spell_damage(self, s: SimState) -> dict:
        return dict()

    def run_events(self, s: "SimState"):
        did_cast = any(ev.type == "cast" for ev in s.events)
        if did_cast:
            svs = self._calc_spell_vars(s)
            self._start_buff(s, svs)

        if buff := s.buffs.get(self.BUFF_KEY):
            num_ticks = int(s.t - buff["start"])
            for _ in range(num_ticks):
                s.misc_damage.append(
                    SimMiscDamage(
                        t=s.t,
                        magical_damage=buff["tick_damage"],
                        physical_damage=0,
                        true_damage=0,
                    )
                )

    def _start_buff(self, s: SimState, svs: dict):
        if self.BUFF_KEY not in s.buffs:
            s.buffs[self.BUFF_KEY] = dict(
                start=s.t,
                tick_damage=svs["modifieddamage"],
            )
        else:
            s.buffs[self.BUFF_KEY]["tick_damage"] += svs["modifiedsecondarydamage"]

    def get_unit_bonus(self, s: SimState) -> SimStats | None:
        bonus = None

        if self.BUFF_KEY in s.buffs:
            bonus = SimStats.zeros()
            svs = self._calc_spell_vars(s)
            bonus.health += svs["modifiedinitialhealth"]
            bonus.health_max += svs["modifiedinitialhealth"]

        return bonus


class UdyrQuirks(UnitQuirks):
    id = "Characters/TFT15_Udyr"

    FLAG_KEY = "udyr_aoe_targets"
    notes = ["AoE hits {udyr_aoe_targets}"]

    BUFF_KEY = "udyr_spell"

    def get_spell_damage(self, s: SimState) -> dict:
        return dict()

    def run_events(self, s: SimState):
        if s.ctx.unit_id != self.id:
            return

        did_auto = any(ev.type == "auto" for ev in s.events)
        if did_auto:
            buff = s.buffs.get(self.BUFF_KEY, None)
            if buff:
                buff["num_autos"] += 1

                if buff["num_autos"] >= buff["total_autos"]:
                    self._end_buff(s)

        did_cast = any(ev.type == "cast" for ev in s.events)
        if did_cast:
            svs = self._calc_spell_vars(s)
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

    def get_auto_damage(self, s: SimState) -> dict:
        bonus = 0
        if buff := s.buffs.get(self.BUFF_KEY):
            aoe_mult = s.ctx.flags[self.FLAG_KEY]
            bonus = aoe_mult * buff["damage"]

        return dict(
            physical=(s.stats.ad + bonus) * self._calc_crit_bonus(s),
        )


class ViegoQuirks(UnitQuirks):
    id = "Characters/TFT15_Viego"

    BUFF_KEY = "viego_spell"

    def get_spell_damage(self, s: SimState) -> dict:
        return dict()

    def run_events(self, s: SimState):
        if s.ctx.unit_id != self.id:
            return

        did_cast = any(ev.type == "cast" for ev in s.events)
        if did_cast:
            svs = self._calc_spell_vars(s)
            self._start_buff(s, svs)

        did_auto = any(ev.type == "auto" for ev in s.events)
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

    def get_auto_damage(self, s: SimState) -> dict:
        svs = self._calc_spell_vars(s)

        bonus = svs["modifiedpassivedamage"]
        if buff := s.buffs.get(self.BUFF_KEY):
            bonus += buff["damage"][buff["num_autos"]]

        return dict(
            physical=s.stats.ad * self._calc_crit_bonus(s),
            magical=bonus,
        )


class YasuoQuirks(UnitQuirks):
    id = "Characters/TFT15_Yasuo"

    def get_spell_damage(self, s: SimState) -> dict:
        svs = self._calc_spell_vars(s)
        return dict(
            physical=svs["numtargets"] * svs["totaldamage"],
        )


class ZiggsQuirks(UnitQuirks):
    id = "Characters/TFT15_Ziggs"

    FLAG_KEY = "ziggs_aoe_targets"
    notes = ["AoE hits {ziggs_aoe_targets}"]

    def get_spell_damage(self, s: SimState) -> dict:
        svs = self._calc_spell_vars(s)
        aoe_mult = s.ctx.flags[self.FLAG_KEY]
        return dict(
            magical=aoe_mult * svs["modifiedexplosiondamage"],
        )

    def get_auto_damage(self, s: SimState) -> dict:
        svs = self._calc_spell_vars(s)
        return dict(
            magical=svs["totalattackdamage"] * (s.stats.crit_mult * s.stats.crit_rate),
            physical=0,
        )


# class KogMawQuirks(UnitQuirks):
#     id = "Characters/TFT15_KogMaw"

#     FLAG_KEY = "kogmaw_trainer_level"
#     notes = ["Trainer Leve {ziggs_aoe_targets}"]

#     def get_spell_damage(self, s: SimState) -> dict:
#         svs = self._calc_spell_vars(s)
#         return dict()


# class SmolderQuirks(UnitQuirks):
#     id = "Characters/TFT15_Smolder"

#     def get_spell_damage(self, s: SimState) -> dict:
#         svs = self._calc_spell_vars(s)
#         return dict()


# class RammusQuirks(UnitQuirks):
#     id = "Characters/TFT15_Rammus"

#     def get_spell_damage(self, s: SimState) -> dict:
#         svs = self._calc_spell_vars(s)
#         return dict()
