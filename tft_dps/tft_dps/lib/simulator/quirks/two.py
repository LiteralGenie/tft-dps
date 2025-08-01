from tft_dps.lib.simulator.quirks.quirks import UnitQuirks
from tft_dps.lib.simulator.sim_state import SimState, SimStats


class DrMundoQuirks(UnitQuirks):
    id = "Characters/TFT15_DrMundo"

    BUFF_KEY = "mundo_spell"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.passives_applied = 0

    # Does not reset passive timer
    def get_spell_damage(self, s: SimState) -> dict:
        svs = self._calc_spell_vars(s)
        return dict(
            physical=svs["totaldamage"],
        )

    def get_auto_damage(self, s: SimState) -> dict:
        svs = self._calc_spell_vars(s)

        bonus = 0
        passive_stacks = int(s.t / svs["passivecadence"])
        has_passive_bonus = (passive_stacks - self.passives_applied) > 0
        if has_passive_bonus:
            bonus += svs["totaldamage"]

        return dict(
            physical=s.stats.ad + bonus,
        )

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

        s.buffs[self.BUFF_KEY] = dict(
            start=s.t,
            until=s.t + svs["duration"],
            duration=svs["duration"],
        )

    def _end_buff(self, s: SimState):
        del s.buffs[self.BUFF_KEY]

    def get_unit_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        svs = self._calc_spell_vars(s)

        num_casts = len(s.casts)
        if buff := s.buffs.get(self.BUFF_KEY):
            num_casts -= 1

            elapsed = (buff["until"] - buff["start"]) / buff["duration"]
            elapsed = min(elapsed, 1)
            num_casts += elapsed

        bonus_hp = num_casts * svs["totalheal"]
        bonus.health_max += bonus_hp
        bonus.health += bonus_hp

        return bonus


class GangplankQuirks(UnitQuirks):
    id = "Characters/TFT15_Gangplank"

    def get_spell_damage(self, s: SimState) -> dict:
        svs = self._calc_spell_vars(s)
        return dict(
            physical=svs["totaldamage"],
        )


class JannaQuirks(UnitQuirks):
    id = "Characters/TFT15_Janna"

    def get_spell_damage(self, s: SimState) -> dict:
        svs = self._calc_spell_vars(s)
        return dict(
            physical=svs["numbutterflies"] * svs["butterflydamage"],
        )


class JhinQuirks(UnitQuirks):
    id = "Characters/TFT15_Jhin"

    def get_stats_override(self, s: SimState, update: SimStats) -> SimStats:
        svs = self._calc_spell_vars(s)

        # Lock AS to 0.75 / 0.75 / 0.85
        base_as = s.ctx.base_stats.speed
        bonus_as = (update.speed - base_as) / base_as
        update.speed = svs["attackspeed"]

        # Convert bonus AS (relative to base, not locked value) to bonus AD
        base_ad = s.ctx.base_stats.ad
        bonus_ad = (update.ad - base_ad) / base_ad
        conversion_ad = bonus_as * 0.8
        update.ad = base_ad * (1 + bonus_ad + conversion_ad)

        return update

    def get_spell_damage(self, s: SimState) -> dict:
        return dict()

    def get_auto_damage(self, s: SimState) -> dict:
        svs = self._calc_spell_vars(s)

        num_attacks = len(s.attacks) + 1

        bonus = 0
        if (num_attacks % 4) == 0:
            bonus = svs["totaldamage"]

        return dict(
            physical=s.stats.ad + bonus,
        )


class KaiSaQuirks(UnitQuirks):
    id = "Characters/TFT15_KaiSa"

    FLAG_KEY = "kaisa_passive_stacks"
    notes = ["Passive stacks set to {kaisa_passive_stacks}"]

    def get_spell_damage(self, s: SimState) -> dict:
        svs = self._calc_spell_vars(s)
        return dict(
            physical=svs["totaldamage"] * svs["missilestofire"],
        )

    def get_unit_bonus(self, s: SimState) -> SimStats:
        svs = self._calc_spell_vars(s)

        bonus = SimStats.zeros()
        bonus.ad = svs["adperkill"] * s.ctx.flags[self.FLAG_KEY]

        return bonus


class KatarinaQuirks(UnitQuirks):
    id = "Characters/TFT15_Katarina"

    FLAG_KEY = "katarina_aoe_targets"
    notes = ["AoE hits {katarina_aoe_targets}"]

    def get_spell_damage(self, s: SimState) -> dict:
        svs = self._calc_spell_vars(s)

        dmg = svs["modifieddamage"]

        num_potential = 0
        if trait := s.ctx.trait_inventory.get("TFT15_BattleAcademia"):
            num_potential = trait.effects["numpotential"]

        if num_potential > 0:
            dmg *= svs["battlebonuspercentperpotential"] * num_potential

        aoe_mult = s.ctx.flags[self.FLAG_KEY]
        dmg *= aoe_mult

        return dict(
            magical=dmg,
        )


class KobukoQuirks(UnitQuirks):
    id = "Characters/TFT15_Kobuko"

    BUFF_KEY = "kobuko_spell"

    def get_spell_damage(self, s: SimState) -> dict:
        return dict()

    def get_auto_damage(self, s: SimState) -> dict:
        bonus = 0
        if self.BUFF_KEY in s.buffs:
            svs = self._calc_spell_vars(s)
            svs["modifieddamage"]

        return dict(
            physical=s.stats.ad + bonus,
        )

    def run_events(self, s: SimState):
        if s.ctx.unit_id != self.id:
            return

        did_auto = any(ev.type == "auto" for ev in s.events)
        if did_auto:
            buff = s.buffs.get(self.BUFF_KEY, None)
            if buff:
                self._end_buff(s)

        did_cast = any(ev.type == "cast" for ev in s.events)
        if did_cast:
            self._start_buff(s)

    def _start_buff(self, s: SimState):
        s.buffs[self.BUFF_KEY] = True
        s.mana_locks += 1

    def _end_buff(self, s: SimState):
        del s.buffs[self.BUFF_KEY]
        s.mana_locks -= 1


class LuxQuirks(UnitQuirks):
    id = "Characters/TFT15_Lux"

    FLAG_KEY = "lux_aoe_targets"
    notes = ["AoE hits {lux_aoe_targets}"]

    def get_spell_damage(self, s: SimState) -> dict:
        svs = self._calc_spell_vars(s)

        aoe_mult = s.ctx.flags[self.FLAG_KEY]
        dmg = svs["modifieddamage"] + aoe_mult * svs["modifiedbasedamage"]

        return dict(
            magical=dmg,
        )


class RakanQuirks(UnitQuirks):
    id = "Characters/TFT15_Rakan"

    def get_spell_damage(self, s: SimState) -> dict:
        svs = self._calc_spell_vars(s)
        return dict(
            magical=svs["modifieddamage"] * svs["numtargets"],
        )


class ShenQuirks(UnitQuirks):
    id = "Characters/TFT15_Shen"

    BUFF_KEY = "shen_spell"

    def get_spell_damage(self, s: SimState) -> dict:
        return dict()

    def get_auto_damage(self, s: SimState) -> dict:
        bonus = 0
        if self.BUFF_KEY in s.buffs:
            svs = self._calc_spell_vars(s)
            bonus = svs["modifieddamage"]

        return dict(
            physical=s.stats.ad,
            true=bonus,
        )

    def run_events(self, s: SimState):
        if s.ctx.unit_id != self.id:
            return

        did_auto = any(ev.type == "auto" for ev in s.events)
        if did_auto:
            buff = s.buffs.get(self.BUFF_KEY, None)
            if buff:
                buff["num_autos"] += 1

                svs = self._calc_spell_vars(s)
                if buff["num_autos"] >= svs["attackcount"]:
                    self._end_buff(s)

        did_cast = any(ev.type == "cast" for ev in s.events)
        if did_cast:
            self._start_buff(s)

    def _start_buff(self, s: SimState):
        s.buffs[self.BUFF_KEY] = dict(num_autos=0)
        s.mana_locks += 1

    def _end_buff(self, s: SimState):
        del s.buffs[self.BUFF_KEY]
        s.mana_locks -= 1


# Armor bonus not calculated
class ViQuirks(UnitQuirks):
    id = "Characters/TFT15_Vi"

    FLAG_KEY = "vi_aoe_targets"
    notes = ["AoE hits {vi_aoe_targets}"]

    def get_spell_damage(self, s: SimState) -> dict:
        svs = self._calc_spell_vars(s)
        aoe_mult = s.ctx.flags[self.FLAG_KEY]
        return dict(
            physical=aoe_mult * svs["modifieddamage"],
        )


class XayahQuirks(UnitQuirks):
    id = "Characters/TFT15_Xayah"

    BUFF_KEY = "xayah_spell"

    def get_spell_damage(self, s: SimState) -> dict:
        return dict()

    def get_auto_damage(self, s: SimState) -> dict:
        bonus = 0
        if self.BUFF_KEY in s.buffs:
            svs = self._calc_spell_vars(s)
            bonus = svs["modifieddamage"] * (1 + svs["additionaltargets"])

        return dict(
            physical=s.stats.ad + bonus,
        )

    def run_events(self, s: SimState):
        if s.ctx.unit_id != self.id:
            return

        did_auto = any(ev.type == "auto" for ev in s.events)
        if did_auto:
            buff = s.buffs.get(self.BUFF_KEY, None)
            if buff:
                buff["num_autos"] += 1

                svs = self._calc_spell_vars(s)
                if buff["num_autos"] >= svs["attacknum"]:
                    self._end_buff(s)

        did_cast = any(ev.type == "cast" for ev in s.events)
        if did_cast:
            self._start_buff(s)

    def _start_buff(self, s: SimState):
        s.buffs[self.BUFF_KEY] = dict(num_autos=0)
        s.mana_locks += 1

    def _end_buff(self, s: SimState):
        del s.buffs[self.BUFF_KEY]
        s.mana_locks -= 1

    def get_unit_bonus(self, s: SimState) -> SimStats | None:
        if not (buff := s.buffs.get(self.BUFF_KEY)):
            return None

        svs = self._calc_spell_vars(s)

        bonus = SimStats.zeros()
        bonus.speed = svs["attackspeed"] * 100

        return bonus


class XinZhaoQuirks(UnitQuirks):
    id = "Characters/TFT15_XinZhao"

    FLAG_KEY = "xin_aoe_targets"
    notes = ["AoE hits {xin_aoe_targets}"]

    def get_spell_damage(self, s: SimState) -> dict:
        svs = self._calc_spell_vars(s)
        aoe_mult = s.ctx.flags[self.FLAG_KEY]
        return dict(
            physical=aoe_mult * svs["modifieddamage"],
        )
