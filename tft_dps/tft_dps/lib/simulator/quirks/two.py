from tft_dps.lib.simulator.quirks.quirks import UnitQuirks
from tft_dps.lib.simulator.sim_state import (
    SimDamage,
    SimState,
    SimStats,
    sim_damage_auto,
    sim_damage_spell,
)
from tft_dps.lib.simulator.sim_system import SimEvent


class DrMundoQuirks(UnitQuirks):
    id = "Characters/TFT15_DrMundo"

    BUFF_KEY_ACTIVE = "mundo_active"
    BUFF_KEY_STACKS = "mundo_passive"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.last_passive_trigger = -99

    def hook_stats(self, s: "SimState") -> "SimStats | None":
        if stacks := s.buffs.get(self.BUFF_KEY_STACKS):
            bonus = SimStats.zeros()

            bonus.health_max = stacks["bonus_health_max"]

            last_cast = stacks["last_cast"]
            duration = last_cast["end"] - last_cast["start"]
            elapsed = s.t - last_cast["start"]
            reduction = (1 - min(elapsed / duration, 1)) * last_cast["bonus_health_max"]

            bonus.health_max -= reduction

            return bonus

    # Casts do not reset passive timer
    def get_spell_damage(self, s: SimState, stats: SimStats) -> SimDamage:
        svs = self._calc_spell_vars(s, stats)
        return sim_damage_spell(
            s,
            stats,
            ph=svs["totaldamage"],
        )

    def get_auto_damage(self, s: SimState, stats: SimStats) -> SimDamage:
        svs = self._calc_spell_vars(s, stats)

        bonus = 0
        if s.t - self.last_passive_trigger > svs["passivecadence"]:
            bonus += svs["totaldamage"]

        return sim_damage_auto(
            s,
            stats,
            ph=(stats.effective_ad + bonus),
        )

    def hook_events(
        self, s: "SimState", evs: list["SimEvent"], stats: "SimStats"
    ) -> list | None:
        if s.ctx.unit_id != self.id:
            return

        active = s.buffs.get(self.BUFF_KEY_ACTIVE, None)
        if active and s.t > active["until"]:
            self._end_active_buff(s)

        did_cast = any(ev.type == "cast" for ev in evs)
        if did_cast:
            svs = self._calc_spell_vars(s, stats)
            self._start_active_buff(s, svs)
            self._increment_stacks_buff(s, svs)

    def _start_active_buff(self, s: SimState, svs: dict):
        s.buffs[self.BUFF_KEY_ACTIVE] = dict(
            start=s.t,
            until=s.t + svs["duration"],
            duration=svs["duration"],
        )

        self.t_wake = s.buffs[self.BUFF_KEY_ACTIVE]["until"] + 0.001

    def _end_active_buff(self, s: SimState):
        del s.buffs[self.BUFF_KEY_ACTIVE]
        self.t_wake = 999

    def _increment_stacks_buff(self, s: SimState, svs: dict):
        s.buffs.setdefault(
            self.BUFF_KEY_STACKS,
            dict(
                bonus_health_max=0,
                last_cast=...,
            ),
        )
        s.buffs[self.BUFF_KEY_STACKS]["bonus_health_max"] += svs["totalheal"]
        s.buffs[self.BUFF_KEY_STACKS]["last_cast"] = dict(
            bonus_health_max=svs["totalheal"],
            start=s.t,
            end=s.t + svs["duration"],
        )

        self.t_wake = s.buffs[self.BUFF_KEY_STACKS]["last_cast"]["end"] + 0.001


class GangplankQuirks(UnitQuirks):
    id = "Characters/TFT15_Gangplank"

    def get_spell_damage(self, s: SimState, stats: SimStats) -> SimDamage:
        svs = self._calc_spell_vars(s, stats)
        return sim_damage_spell(
            s,
            stats,
            ph=svs["totaldamage"],
        )


class JannaQuirks(UnitQuirks):
    id = "Characters/TFT15_Janna"

    def get_spell_damage(self, s: SimState, stats: SimStats) -> SimDamage:
        svs = self._calc_spell_vars(s, stats)
        return sim_damage_spell(
            s,
            stats,
            ph=svs["numbutterflies"] * svs["butterflydamage"],
        )


class JhinQuirks(UnitQuirks):
    id = "Characters/TFT15_Jhin"

    def hook_init(self, s: SimState, stats: SimStats):
        s.mana_locks += 1

    def hook_stats_override(self, s: SimState, stats: SimStats):
        svs = self._calc_spell_vars(s, stats)

        # Convert bonus AS to bonus AD
        speed_mult = stats.speed_mult
        stats.speed = svs["attackspeed"]
        stats.speed_mult = 1
        stats.ad_mult += speed_mult * 0.8

        return stats

    def get_auto_damage(self, s: SimState, stats: SimStats) -> SimDamage:
        svs = self._calc_spell_vars(s, stats)

        num_attacks = len(s.attacks) + 1

        if (num_attacks % 4) == 0:
            dmg = svs["totaldamage"]
        else:
            dmg = stats.effective_ad

        return sim_damage_auto(
            s,
            stats,
            ph=dmg,
        )


class KaiSaQuirks(UnitQuirks):
    id = "Characters/TFT15_KaiSa"

    FLAG_KEY = "kaisa_passive_stacks"
    notes = ["Passive stacks set to {kaisa_passive_stacks}"]

    BUFF_KEY = "kaisa_spell"

    def hook_init(self, s: SimState, stats: SimStats):
        self._init_buff(s, stats)

    def hook_stats(self, s: "SimState") -> "SimStats | None":
        if buff := s.buffs.get(self.BUFF_KEY):
            bonus = SimStats.zeros()
            bonus.ad_mult = buff["bonus_ad_mult"]
            return bonus

    def get_spell_damage(self, s: SimState, stats: SimStats) -> SimDamage:
        svs = self._calc_spell_vars(s, stats)
        return sim_damage_spell(
            s,
            stats,
            ph=svs["totaldamage"] * svs["missilestofire"],
        )

    def _init_buff(self, s: SimState, stats: SimStats):
        svs = self._calc_spell_vars(s, stats)

        bonus_ad_mult = (svs["adperkill"] / 100) * s.ctx.flags[self.FLAG_KEY]
        s.buffs[self.BUFF_KEY] = dict(
            bonus_ad_mult=bonus_ad_mult,
        )


class KatarinaQuirks(UnitQuirks):
    id = "Characters/TFT15_Katarina"

    FLAG_KEY = "katarina_aoe_targets"
    notes = ["AoE hits {katarina_aoe_targets}"]

    def get_spell_damage(self, s: SimState, stats: SimStats) -> SimDamage:
        svs = self._calc_spell_vars(s, stats)

        dmg = svs["modifieddamage"]

        num_potential = 0
        if trait := s.ctx.trait_inventory.get("TFT15_BattleAcademia"):
            num_potential = trait.effects_bonus["numpotential"]

        if num_potential > 0:
            dmg *= svs["battlebonuspercentperpotential"] * num_potential

        aoe_mult = s.ctx.flags[self.FLAG_KEY]
        dmg *= aoe_mult

        return sim_damage_spell(
            s,
            stats,
            ma=dmg,
        )


class KobukoQuirks(UnitQuirks):
    id = "Characters/TFT15_Kobuko"

    BUFF_KEY = "kobuko_spell"

    def get_auto_damage(self, s: SimState, stats: SimStats) -> SimDamage:
        bonus = 0
        if self.BUFF_KEY in s.buffs:
            svs = self._calc_spell_vars(s, stats)
            svs["modifieddamage"]

        return sim_damage_auto(
            s,
            stats,
            ph=stats.effective_ad + bonus,
        )

    def hook_events(
        self, s: "SimState", evs: list["SimEvent"], stats: "SimStats"
    ) -> list | None:
        if s.ctx.unit_id != self.id:
            return

        did_auto = any(ev.type == "auto" for ev in evs)
        if did_auto:
            buff = s.buffs.get(self.BUFF_KEY, None)
            if buff:
                self._end_buff(s)

        did_cast = any(ev.type == "cast" for ev in evs)
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

    def get_spell_damage(self, s: SimState, stats: SimStats) -> SimDamage:
        svs = self._calc_spell_vars(s, stats)

        aoe_mult = s.ctx.flags[self.FLAG_KEY]
        dmg = svs["modifieddamage"] + aoe_mult * svs["modifiedbasedamage"]

        return sim_damage_spell(
            s,
            stats,
            ma=dmg,
        )


class RakanQuirks(UnitQuirks):
    id = "Characters/TFT15_Rakan"

    def get_spell_damage(self, s: SimState, stats: SimStats) -> SimDamage:
        svs = self._calc_spell_vars(s, stats)
        return sim_damage_spell(
            s,
            stats,
            ma=svs["modifieddamage"] * svs["numtargets"],
        )


class ShenQuirks(UnitQuirks):
    id = "Characters/TFT15_Shen"

    BUFF_KEY_AUTO = "shen_spell_autos"
    BUFF_KEY_SHIELD = "shen_spell_shield"

    def get_auto_damage(self, s: SimState, stats: SimStats) -> SimDamage:
        bonus_damage = 0
        if buff := s.buffs.get(self.BUFF_KEY_AUTO):
            bonus_damage = buff["bonus_damage"]

        return sim_damage_auto(
            s,
            stats,
            ph=stats.effective_ad,
            tr=bonus_damage,
        )

    def hook_events(
        self, s: "SimState", evs: list["SimEvent"], stats: "SimStats"
    ) -> list | None:
        if s.ctx.unit_id != self.id:
            return

        did_auto = any(ev.type == "auto" for ev in evs)
        if did_auto:
            buff = s.buffs.get(self.BUFF_KEY_AUTO, None)
            if buff:
                buff["num_autos"] += 1

                svs = self._calc_spell_vars(s, stats)
                if buff["num_autos"] >= svs["attackcount"]:
                    self._end_buff_auto(s)

        if buff_shield := s.buffs.get(self.BUFF_KEY_SHIELD):
            if s.t > buff_shield["until"]:
                self._end_buff_shield(s)

        did_cast = any(ev.type == "cast" for ev in evs)
        if did_cast:
            svs = self._calc_spell_vars(s, stats)
            self._start_buff_auto(s, svs)
            self._start_buff_shield(s, svs)

    def _start_buff_auto(self, s: SimState, svs: dict):
        bonus_damage = svs["modifieddamage"]

        s.buffs[self.BUFF_KEY_AUTO] = dict(
            num_autos=0,
            bonus_damage=bonus_damage,
        )
        s.mana_locks += 1

    def _end_buff_auto(self, s: SimState):
        del s.buffs[self.BUFF_KEY_AUTO]
        s.mana_locks -= 1

    def _start_buff_shield(self, s: SimState, svs: dict):
        s.buffs[self.BUFF_KEY_SHIELD] = dict(
            until=s.t + svs["duration"],
        )
        s.mana_locks += 1

        self.t_wake = s.buffs[self.BUFF_KEY_SHIELD]["until"] + 0.001

    def _end_buff_shield(self, s: SimState):
        del s.buffs[self.BUFF_KEY_SHIELD]
        s.mana_locks -= 1
        self.t_wake = 999


# Armor bonus not calculated
class ViQuirks(UnitQuirks):
    id = "Characters/TFT15_Vi"

    FLAG_KEY = "vi_aoe_targets"
    notes = ["AoE hits {vi_aoe_targets}"]

    def get_spell_damage(self, s: SimState, stats: SimStats) -> SimDamage:
        svs = self._calc_spell_vars(s, stats)
        aoe_mult = s.ctx.flags[self.FLAG_KEY]
        return sim_damage_spell(
            s,
            stats,
            ph=aoe_mult * svs["modifieddamage"],
        )


class XayahQuirks(UnitQuirks):
    id = "Characters/TFT15_Xayah"

    BUFF_KEY = "xayah_spell"

    def get_auto_damage(self, s: SimState, stats: SimStats) -> SimDamage:
        dmg = stats.effective_ad

        if self.BUFF_KEY in s.buffs:
            svs = self._calc_spell_vars(s, stats)
            dmg += svs["modifieddamage"]
            dmg *= 1 + svs["additionaltargets"]

        return sim_damage_auto(
            s,
            stats,
            ph=dmg,
        )

    def hook_events(
        self, s: "SimState", evs: list["SimEvent"], stats: "SimStats"
    ) -> list | None:
        if s.ctx.unit_id != self.id:
            return

        did_auto = any(ev.type == "auto" for ev in evs)
        if did_auto:
            buff = s.buffs.get(self.BUFF_KEY, None)
            if buff:
                buff["num_autos"] += 1

                svs = self._calc_spell_vars(s, stats)
                if buff["num_autos"] >= svs["attacknum"]:
                    self._end_buff(s)

        did_cast = any(ev.type == "cast" for ev in evs)
        if did_cast:
            self._start_buff(s, stats)

    def _start_buff(self, s: SimState, stats: SimStats):
        svs = self._calc_spell_vars(s, stats)

        s.buffs[self.BUFF_KEY] = dict(
            num_autos=0,
            bonus_speed_mult=svs["attackspeed"],
        )
        s.mana_locks += 1

    def _end_buff(self, s: SimState):
        del s.buffs[self.BUFF_KEY]
        s.mana_locks -= 1

    def hook_stats(self, s: "SimState") -> "SimStats | None":
        if buff := s.buffs.get(self.BUFF_KEY):
            bonus = SimStats.zeros()
            bonus.speed_mult = buff["bonus_speed_mult"]
            return bonus


class XinZhaoQuirks(UnitQuirks):
    id = "Characters/TFT15_XinZhao"

    FLAG_KEY = "xin_aoe_targets"
    notes = ["AoE hits {xin_aoe_targets}"]

    def get_spell_damage(self, s: SimState, stats: SimStats) -> SimDamage:
        svs = self._calc_spell_vars(s, stats)
        aoe_mult = s.ctx.flags[self.FLAG_KEY]
        return sim_damage_spell(
            s,
            stats,
            ph=aoe_mult * svs["modifieddamage"],
        )
