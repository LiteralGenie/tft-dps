from abc import ABCMeta

from tft_dps.lib.simulator.crit_system import create_spell_crit_buff
from tft_dps.lib.simulator.quirks.quirks import TraitQuirks
from tft_dps.lib.simulator.sim_state import SimState, SimStats, sim_damage_misc
from tft_dps.lib.simulator.sim_system import SimEvent


class BastionQuirks(TraitQuirks):
    id = "TFT15_Bastion"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        eb = self._eb(s)

        bonus.armor += eb["bonusarmor"]
        bonus.mr += eb["bonusmr"]
        if s.t < eb["duration"]:
            bonus.armor *= eb["statmultiplier"]
            bonus.mr *= eb["statmultiplier"]

        return bonus


class BattleAcademiaQuirks(TraitQuirks):
    id = "TFT15_BattleAcademia"


class ExecutionerQuirks(TraitQuirks):
    id = "TFT15_Destroyer"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        eb = self._eb(s)

        bonus.crit_rate = eb["critchanceamppercent"] / 100
        bonus.crit_mult = eb["critamppercent"] / 100

        create_spell_crit_buff(s, 0)

        return bonus


class DragonFistQuirks(TraitQuirks):
    id = "TFT15_DragonFist"


class EdgelordQuirks(TraitQuirks):
    id = "TFT15_Edgelord"

    notes = ["Low-target-health bonus is always active"]

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        eb = self._eb(s)

        bonus.ad = eb["ad"]
        bonus.speed_mult = eb["bonusas"]

        return bonus


class WraithQuirks(TraitQuirks):
    id = "TFT15_Empyrean"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.last_activation = 0
        self.last_activation_dmg = 0

    def hook_main(self, s: SimState, stats: SimStats) -> list | None:
        eb = self._eb(s)

        elapsed = s.t - self.last_activation
        if elapsed < 5:
            return

        xs = [
            x
            for grp in [s.casts, s.attacks, s.misc_damage]
            for x in grp
            if x["t"] >= self.last_activation
        ]

        dmg = sum(
            value * x["mult"]
            for x in xs
            for value in [x["physical_damage"], x["magical_damage"], x["true_damage"]]
        )

        after_reduction = dmg * eb["damagepercent"]
        after_reduction -= self.last_activation_dmg

        s.misc_damage.append(
            sim_damage_misc(
                s,
                stats,
                ma=after_reduction,
            )
        )

        self.last_activation = s.t
        self.last_activation_dmg = after_reduction


class HeavyweightQuirks(TraitQuirks):
    id = "TFT15_Heavyweight"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        eb = self._eb(s)

        bonus.health_max = 100
        bonus.health_mult = eb["bonuspercenthealth"]

        return bonus

    def hook_stats_override(self, s: SimState, stats: SimStats):
        eb = self._eb(s)

        stats.ad_mult += (
            stats.effective_health * (eb["healthpercenttoad"] / 100)
        ) / 100


class SorcererQuirks(TraitQuirks):
    id = "TFT15_Spellslinger"

    notes = ["On-target-death effect is modeled as additional damage amp"]

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        eb = self._eb(s)

        bonus.ap = eb["abilitypower"]
        bonus.amp = eb["healthpct"] * eb["targetnum"]

        return bonus


class MonsterTrainerQuirks(TraitQuirks):
    id = "TFT15_MonsterTrainer"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        eb = self._eb(s)

        return bonus


class OldMentorQuirks(TraitQuirks):
    id = "TFT15_OldMentor"

    effect_map = {
        "Characters/TFT15_Kobuko": "durability",
        "Characters/TFT15_Udyr": "adap",
        "Characters/TFT15_Yasuo": "as",
        "Characters/TFT15_Ryze": "mana",
    }

    BUFF_KEY_RYZE = "ryze_mentor_mana"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        em = self._em(s)

        unit_id = s.ctx.unit_id
        bp = s.ctx.trait_inventory[self.id].breakpoint
        if bp == 1:
            keys = [unit_id]
        elif bp == 4:
            keys = list(self.effect_map.keys())
        else:
            keys = []

        kvs = {k: em[self.effect_map[k]] for k in keys}
        for k, v in kvs.items():
            match k:
                case "Characters/TFT15_Kobuko":
                    pass
                case "Characters/TFT15_Udyr":
                    bonus.ad_mult = v
                    bonus.ap = v
                case "Characters/TFT15_Yasuo":
                    bonus.speed_mult = v
                case "Characters/TFT15_Ryze":
                    s.buffs[self.BUFF_KEY_RYZE] = v
                case _:
                    self.logger.error(
                        f"Mentor trait active on non-mentor unit {s.ctx.unit_id}"
                    )

        return bonus


class ProdigyQuirks(TraitQuirks):
    id = "TFT15_Prodigy"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        eb = self._eb(s)

        bonus.mana_regen += eb["prodigybonusmana"]

        return bonus


class ProtectorQuirks(TraitQuirks):
    id = "TFT15_Protector"


class JuggernautQuirks(TraitQuirks):
    id = "TFT15_Juggernaut"


class SniperQuirks(TraitQuirks):
    id = "TFT15_Sniper"

    FLAG_KEY = "sniper_hexes"
    notes = ["Target assumed to be {sniper_hexes} away"]

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        eb = self._eb(s)

        bonus.amp = eb["percentdamageincrease"] / 100

        num_hexes = s.ctx.flags[self.FLAG_KEY]
        bonus.amp += num_hexes * eb["perhexincrease"] / 100

        return bonus


class SoulFighterQuirks(TraitQuirks):
    id = "TFT15_SoulFighter"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        eb = self._eb(s)

        num_stacks = min(int(s.t), eb["maxstacks"])

        bonus.ad_mult = num_stacks * eb["statspersecond"]
        bonus.ap = num_stacks * eb["statspersecond"] * 100
        bonus.health_max = num_stacks * eb["flathealth"]

        if num_stacks == eb["maxstacks"]:
            bonus.amp = eb["bonustruedamage"]

        return bonus


class StarGuardianQuirks(TraitQuirks):
    id = "TFT15_StarGuardian"

    FLAG_KEY_STAR_JINX = "star_jinx_as"
    notes = [
        "Activation order: (current unit) -> Syndra (AP) -> Ahri (mana) -> Xayah (auto dmg) - > Jinx (AS) -> Seraphine (all) -> ...rest... -> emblem",
        "Bonus AS from Jinx modeled as +{star_jinx_as} AS bonus",
    ]

    effects = {
        "Characters/TFT15_Syndra": "{99ff11e5}",
        "Characters/TFT15_Ahri": "{05ce3a8e}",
        "Characters/TFT15_Xayah": "{5416a34e}",
        "Characters/TFT15_Jinx": "{39509739}",
        "Characters/TFT15_Seraphine": "{39509739}",
        #
        "Characters/TFT15_Rell": "",
        "Characters/TFT15_Neeko": "",
        "Characters/TFT15_Poppy": "{ca26eef7}",
    }

    BUFF_KEY_AHRI = "sg_ahri_mana"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.units = []
        self.last_xayah_auto = 0
        self.mult = 1

    def hook_init(self, s: SimState, stats: SimStats):
        self.units = list(self.effects.keys())
        self.units.remove(s.ctx.unit_id)
        self.units = [s.ctx.unit_id] + self.units
        self.units = self.units[: s.ctx.trait_inventory[self.id].breakpoint]

        em = self._em(s)

        self.mult = self._eb(s)["multiplier"]
        if s.ctx.trait_inventory[self.id].breakpoint > len(self.effects):
            self.mult += em["emblembonus"]

        if "Characters/TFT15_Ahri" in self.units:
            s.buffs[self.BUFF_KEY_AHRI] = (
                self.mult * em[self.effects["Characters/TFT15_Ahri"]]
            )

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        em = self._em(s)

        for unit_id in self.units:
            match unit_id:
                case "Characters/TFT15_Syndra":
                    v = em[self.effects[unit_id]]
                    num_stacks = int(s.t / em["syndratimer"])
                    bonus.ap += num_stacks * v * self.mult
                case "Characters/TFT15_Ahri":
                    pass
                case "Characters/TFT15_Xayah":
                    pass
                case "Characters/TFT15_Jinx":
                    bonus.speed_mult += (
                        self.mult * s.ctx.flags[self.FLAG_KEY_STAR_JINX] / 100
                    )
                case "Characters/TFT15_Seraphine":
                    v = em[self.effects[unit_id]]
                    bonus.health_mult += v * self.mult
                    bonus.ad_mult += v * self.mult
                    bonus.speed_mult += v * self.mult
                    bonus.crit_rate += v * self.mult
                    bonus.crit_mult += v * self.mult
                case "Characters/TFT15_Rell":
                    pass
                case "Characters/TFT15_Neeko":
                    pass
                case "Characters/TFT15_Poppy":
                    pass

        return bonus

    def hook_events(
        self, s: SimState, evs: list[SimEvent], stats: SimStats
    ) -> list | None:
        num_attacks = len(s.attacks)
        is_xayah_auto = num_attacks % 3 == 0 and num_attacks > self.last_xayah_auto
        if not is_xayah_auto:
            return

        self.last_xayah_auto = num_attacks

        em = self._em(s)
        s.attacks[-1]["magical_damage"] += (
            self.mult * em[self.effects["Characters/TFT15_Xayah"]]
        )


class SupremeCellsQuirks(TraitQuirks):
    id = "TFT15_SupremeCells"

    notes = ["Execute effect modeled as a damage amp bonus"]

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        eb = self._eb(s)

        bonus.amp = eb["overlorddamageamp"] / 100

        return bonus

    def hook_stats_override(self, s: SimState, stats: SimStats):
        em = self._em(s)
        stats.amp *= 1 + em["overlordexecute"]
        stats.amp += em["overlordexecute"]


class SentaiRangerQuirks(TraitQuirks):
    id = "TFT15_SentaiRanger"

    notes = ["Not modeled ¯\_(ツ)_/¯"]


class LuchadorQuirks(TraitQuirks):
    id = "TFT15_Luchador"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        eb = self._eb(s)

        bonus.ad_mult = eb["adbonus"]

        return bonus


class GemForceQuirks(TraitQuirks):
    id = "TFT15_GemForce"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        eb = self._eb(s)

        return bonus


class TheCrewQuirks(TraitQuirks):
    id = "TFT15_TheCrew"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bp = s.ctx.trait_inventory[self.id].breakpoint
        if bp >= 7:
            bonus = SimStats.zeros()
            em = self._em(s)

            bonus.health_max = em["7piecehealth"]
            bonus.amp = em["7pieceamp"]

            return bonus


class CaptainQuirks(TraitQuirks):
    id = "TFT15_Captain"


class RosemotherQuirks(TraitQuirks):
    id = "TFT15_Rosemother"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        eb = self._eb(s)

        return bonus


class StrategistQuirks(TraitQuirks):
    id = "TFT15_Strategist"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        eb = self._eb(s)

        bonus.amp = eb["damageamp"] * 3 / 100

        return bonus


class DuelistQuirks(TraitQuirks):
    id = "TFT15_Duelist"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        eb = self._eb(s)

        num_stacks = min(len(s.attacks), eb["maxstacks"])
        bonus.speed_mult = num_stacks * eb["attackspeedpercent"]

        return bonus


class ElTigreQuirks(TraitQuirks):
    id = "TFT15_ElTigre"


TRAIT_QUIRK_MAP = {
    cls.id: cls
    for cls in locals().values()
    if type(cls) == ABCMeta and issubclass(cls, TraitQuirks) and cls is not TraitQuirks
}
