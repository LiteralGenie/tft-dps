from abc import ABCMeta

from tft_dps.lib.simulator.crit_system import create_spell_crit_buff
from tft_dps.lib.simulator.quirks.quirks import ItemQuirks
from tft_dps.lib.simulator.sim_state import SimState, SimStats, sim_damage_misc
from tft_dps.lib.simulator.sim_system import SimEvent


class BFQuirks(ItemQuirks):
    id = "TFT_Item_BFSword"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.ad_mult = c["AD"] / 100

        return bonus


class BloodthirsterQuirks(ItemQuirks):
    id = "TFT_Item_Bloodthirster"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.ad_mult = c["AD"] / 100
        bonus.ap = c["AP"]
        bonus.mr = c["MagicResist"]

        return bonus


class BrambleVestQuirks(ItemQuirks):
    id = "TFT_Item_BrambleVest"

    FLAG_KEY = "bramble_aoe_targets"
    notes = ["AoE hits {bramble_aoe_targets} targets"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.last_passive_trigger = -99

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.health_mult = c["PercentMaxHP"]
        bonus.armor = c["Armor"]

        return bonus

    def hook_main(self, s: SimState, stats: SimStats) -> list | None:
        c = self._constants(s)

        elapsed = s.t - self.last_passive_trigger
        if elapsed < c["ICD"]:
            return

        self.last_passive_trigger = s.t
        s.misc_damage.append(
            sim_damage_misc(
                s,
                stats,
                ma=c["1StarAoEDamage"],
            )
        )


class ChainVestQuirks(ItemQuirks):
    id = "TFT_Item_ChainVest"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.armor = c["Armor"]

        return bonus


class SparringGlovesQuirks(ItemQuirks):
    id = "TFT_Item_SparringGloves"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.crit_rate = c["CritChance"] / 100

        return bonus


class DeathbladeQuirks(ItemQuirks):
    id = "TFT_Item_Deathblade"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.ad_mult = c["AD"]
        bonus.amp = c["BonusDamage"]

        return bonus


class DragonsClawQuirks(ItemQuirks):
    id = "TFT_Item_DragonsClaw"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.mr = c["MagicResist"]
        bonus.health_mult = c["PercentMaxHP"]

        return bonus


class ThiefsGlovesQuirks(ItemQuirks):
    id = "TFT_Item_ThiefsGloves"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.crit_rate = c["CritChance"] / 100
        bonus.health_max = c["Health"]

        return bonus


class ProtectorsVowQuirks(ItemQuirks):
    id = "TFT_Item_FrozenHeart"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.mana_regen = c["ManaRegen"]
        bonus.armor = c["Armor"]
        bonus.mr = c["MagicResist"]
        bonus.mana = c["CombatStartMana"]

        return bonus


class GiantsBeltQuirks(ItemQuirks):
    id = "TFT_Item_GiantsBelt"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.health_max = c["Health"]

        return bonus


class GiantSlayerQuirks(ItemQuirks):
    id = "TFT_Item_MadredsBloodrazor"

    notes = ["Max damage amp is always applied"]

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.ad_mult = c["AD"]
        bonus.ap = c["AP"]
        bonus.speed_mult = c["AS"] / 100
        bonus.amp = c["DamageAmp"] + c["{1543aa48}"]

        return bonus


class EdgeOfNightQuirks(ItemQuirks):
    id = "TFT_Item_GuardianAngel"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.ap = c["AP"]
        bonus.ad_mult = c["AD"]
        bonus.speed_mult = c["AS"] / 100
        bonus.armor = c["Armor"]

        return bonus


class GuinsoosRagebladeQuirks(ItemQuirks):
    id = "TFT_Item_GuinsoosRageblade"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.ap = c["AP"]
        bonus.speed_mult = c["AS"] / 100

        elapsed_sec = int(s.t)
        bonus.speed_mult += elapsed_sec * c["AttackSpeedPerStack"] / 100

        return bonus


class HandOfJusticeQuirks(ItemQuirks):
    id = "TFT_Item_UnstableConcoction"

    notes = ["Double AD and AP bonuses always applied"]

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.ad_mult = c["{f23e83fc}"] * c["AD_NotStatBar"]
        bonus.ap = c["{f23e83fc}"] * c["AP_NotStatBar"]
        bonus.crit_rate = c["CritChance"] / 100
        bonus.mana_regen = c["ManaRegen"]

        return bonus


class HextechGunbladeQuirks(ItemQuirks):
    id = "TFT_Item_HextechGunblade"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.ad_mult = c["AD"]
        bonus.ap = c["AP"]
        bonus.mana_regen = c["ManaRegen"]

        return bonus


class InfinityEdgeQuirks(ItemQuirks):
    id = "TFT_Item_InfinityEdge"

    def hook_init(self, s: SimState, stats: SimStats):
        c = self._constants(s)
        create_spell_crit_buff(s, c["CritDamageToGive"])

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.ad_mult = c["AD"]
        bonus.crit_rate = c["CritChance"] / 100

        return bonus


class IonicSparkQuirks(ItemQuirks):
    id = "TFT_Item_IonicSpark"

    FLAG_KEY_DAMAGE = "item_spark_damage"
    FLAG_KEY_FREQUENCY = "item_spark_frequency"

    notes = [
        "Damage is modeled as {item_spark_damage} damage every {item_spark_frequency} seconds"
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.last_passive_trigger = -99

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.health_max = c["Health"]
        bonus.ap = c["Ap"]
        bonus.mr = c["MagicResist"]

        return bonus

    def hook_main(self, s: SimState, stats: SimStats) -> list | None:
        elapsed = s.t - self.last_passive_trigger
        if elapsed < s.ctx.flags[self.FLAG_KEY_FREQUENCY]:
            return

        self.last_passive_trigger = s.t
        dmg = s.ctx.flags[self.FLAG_KEY_DAMAGE]
        s.misc_damage.append(
            sim_damage_misc(
                s,
                stats,
                ma=dmg,
            )
        )


class JeweledGauntletQuirks(ItemQuirks):
    id = "TFT_Item_JeweledGauntlet"

    def hook_init(self, s: SimState, stats: SimStats):
        c = self._constants(s)
        create_spell_crit_buff(s, c["CritDamageToGive"])

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.ap = c["AP"]
        bonus.crit_rate = c["CritChance"] / 100

        return bonus


class LastWhisperQuirks(ItemQuirks):
    id = "TFT_Item_LastWhisper"

    def hook_init(self, s: SimState, stats: SimStats):
        create_spell_crit_buff(s, 10)

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.ad_mult = c["AD"]
        bonus.speed_mult = c["AS"] / 100
        bonus.crit_rate = c["CritChance"] / 100

        return bonus


class ArchangelsStaffQuirks(ItemQuirks):
    id = "TFT_Item_ArchangelsStaff"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.mana_regen = c["ManaRegen"]
        bonus.ap = c["AP"]

        num_stacks = int(s.t / c["IntervalSeconds"])
        bonus.ap += num_stacks * c["APPerInterval"]

        return bonus


class QuicksilverQuirks(ItemQuirks):
    id = "TFT_Item_Quicksilver"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.mr = c["MagicResist"]
        bonus.speed_mult = c["AS"] / 100
        bonus.crit_rate = c["CritChance"] / 100

        max_stacks = c["SpellShieldDuration"] / c["ProcInterval"]
        num_stacks = int(s.t / c["ProcInterval"])
        frac = min(num_stacks / max_stacks, 1)
        bonus.speed_mult += frac * c["ProcAttackSpeed"]

        return bonus


class MorellonomiconQuirks(ItemQuirks):
    id = "TFT_Item_Morellonomicon"

    FLAG_KEY = "burn_damage_amp"
    notes = ["Damage is modeled as {burn_damage_amp}% extra damage amp"]

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.health_max = c["Health"]
        bonus.ap = c["AP"]
        bonus.mana_regen = c["ManaRegen"]

        bonus.amp += s.ctx.flags[self.FLAG_KEY] / 100

        return bonus


class NeedlesslyLargeRodQuirks(ItemQuirks):
    id = "TFT_Item_NeedlesslyLargeRod"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.ap = c["AP"]

        return bonus


class NegatronCloakQuirks(ItemQuirks):
    id = "TFT_Item_NegatronCloak"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.mr = c["MagicResist"]

        return bonus


class StrikersFlailQuirks(ItemQuirks):
    id = "TFT_Item_PowerGauntlet"

    notes = ["Max damage amp is always applied"]

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.health_max = c["Health"]
        bonus.speed_mult = c["AS"] / 100
        bonus.crit_rate = c["CritChance"] / 100
        bonus.amp = c["{1543aa48}"]
        bonus.amp += c["BuffDamageAmp"] * c["MaxStacks"]

        return bonus


class RabadonsDeathcapQuirks(ItemQuirks):
    id = "TFT_Item_RabadonsDeathcap"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.ap = c["AP"]
        bonus.amp = c["BonusDamage"]

        return bonus


class RedBuffQuirks(ItemQuirks):
    id = "TFT_Item_RapidFireCannon"

    FLAG_KEY = "burn_damage_amp"
    notes = ["Damage is modeled as {burn_damage_amp}% extra damage amp"]

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.speed_mult = c["AS"] / 100
        bonus.amp = c["{1543aa48}"]

        bonus.amp += s.ctx.flags[self.FLAG_KEY] / 100

        return bonus


class RecurveBowQuirks(ItemQuirks):
    id = "TFT_Item_RecurveBow"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.speed_mult = c["AS"] / 100

        return bonus


class SunfireCapeQuirks(ItemQuirks):
    id = "TFT_Item_RedBuff"

    FLAG_KEY = "sunfire_burn_damage"
    notes = ["Damage is modeled as {sunfire_burn_damage}% extra damage amp"]

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.health_max = c["Health"]
        bonus.armor = c["Armor"]
        bonus.health_mult = c["BonusPercentHP"]

        bonus.amp += s.ctx.flags[self.FLAG_KEY] / 100

        return bonus


class SpiritVisageQuirks(ItemQuirks):
    id = "TFT_Item_Redemption"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.health_max = c["Health"]
        bonus.mana_regen = c["ManaRegen"]

        return bonus


class KrakensFuryQuirks(ItemQuirks):
    id = "TFT_Item_RunaansHurricane"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.ad_mult = c["AD"]
        bonus.speed_mult = c["AS"] / 100
        bonus.mr = c["MagicResist"]

        bonus.ad_mult += len(s.attacks) * c["ADOnAttack"]

        return bonus


class SpearOfShojinQuirks(ItemQuirks):
    id = "TFT_Item_SpearOfShojin"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.mana_regen = c["ManaRegen"]
        bonus.ad_mult = c["AD"]
        bonus.ap = c["AP"]

        return bonus


class VoidStaffQuirks(ItemQuirks):
    id = "TFT_Item_StatikkShiv"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.mana_regen = c["ManaRegen"]
        bonus.ap = c["AP"]
        bonus.speed_mult = c["AS"] / 100

        return bonus


class GargoyleStoneplateQuirks(ItemQuirks):
    id = "TFT_Item_GargoyleStoneplate"

    FLAG_KEY = "gargoyle_num_enemies"
    notes = ["Number of attackers is assumed to be {gargoyle_num_enemies}"]

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.health_max = c["Health"]
        bonus.armor = c["Armor"]
        bonus.mr = c["MagicResist"]

        mult = s.ctx.flags[self.FLAG_KEY]
        bonus.armor += mult * c["ArmorPerEnemy"]
        bonus.mr += mult * c["MRPerEnemy"]

        return bonus


class TearOfTheGoddessQuirks(ItemQuirks):
    id = "TFT_Item_TearOfTheGoddess"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.mana_regen = c["ManaRegen"]

        return bonus


class TitansResolveQuirks(ItemQuirks):
    id = "TFT_Item_TitansResolve"

    FLAG_KEY = "titans_stack_frequency"
    notes = ["Stack gained every {titans_stack_frequency}s"]

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.armor = c["Armor"]
        bonus.speed_mult = c["AS"] / 100

        num_stacks = int(s.t / s.ctx.flags[self.FLAG_KEY])
        num_stacks = min(num_stacks, c["StackCap"])

        bonus.ad_mult += num_stacks * c["StackingAD"]
        bonus.ap += num_stacks * c["StackingSP"]

        if num_stacks == c["StackCap"]:
            bonus.armor += c["BonusResistsAtStackCap"]
            bonus.mr += c["BonusResistsAtStackCap"]

        return bonus


class WarmogsArmorQuirks(ItemQuirks):
    id = "TFT_Item_WarmogsArmor"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.health_max = c["Health"]
        bonus.health_mult = c["BonusPercentHP"]

        return bonus


class EvenshroudQuirks(ItemQuirks):
    id = "TFT_Item_SpectralGauntlet"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.health_mult = c["Health"]
        bonus.mr = c["MagicResist"]

        if s.t <= c["BonusResistDuration"]:
            bonus.armor += c["BonusResists"]
            bonus.mr += c["BonusResists"]

        return bonus


class CrownguardQuirks(ItemQuirks):
    id = "TFT_Item_Crownguard"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.health_max = c["Health"]
        bonus.ap = c["AP"]
        bonus.armor = c["Armor"]

        if s.t > c["ShieldDuration"]:
            bonus.ap += c["ShieldBonusAP"]

        return bonus


class SteadfastHeartQuirks(ItemQuirks):
    id = "TFT_Item_NightHarvester"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.health_max = c["Health"]
        bonus.armor = c["Armor"]
        bonus.crit_rate = c["CritChance"] / 100

        return bonus


class SteraksGageQuirks(ItemQuirks):
    id = "TFT_Item_SteraksGage"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.health_max = c["Health"]
        bonus.ad_mult = c["AD"]

        return bonus


class BlueBuffQuirks(ItemQuirks):
    id = "TFT_Item_BlueBuff"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.mana_regen = c["ManaRegen"]
        bonus.ad_mult = c["AD"]
        bonus.ap = c["AP"]

        return bonus


class AdaptiveHelmQuirks(ItemQuirks):
    id = "TFT_Item_AdaptiveHelm"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.mana_regen = c["ManaRegen"]
        bonus.mr = c["MagicResist"]

        role = s.ctx.unit_info["info"]["role"]
        if "Tank" in role or "Fighter" in role:
            bonus.armor += c["FrontlineResists"]
            bonus.mr += c["FrontlineResists"]
        else:
            bonus.ad_mult += c["BacklineADAP"] / 100
            bonus.ap += c["BacklineADAP"]

        return bonus


class NashorsToothQuirks(ItemQuirks):
    id = "TFT_Item_Leviathan"

    BUFF_KEY = "nashor"

    def hook_stats(self, s: SimState) -> SimStats | None:
        bonus = SimStats.zeros()
        c = self._constants(s)

        bonus.health_max = c["Health"]
        bonus.ap = c["AP"]
        bonus.speed_mult = c["AS"] / 100
        bonus.mana_regen = c["ManaRegen"]

        if buff := s.buffs.get(self.BUFF_KEY):
            bonus.speed_mult += buff["bonus_speed_mult"]

        return bonus

    def hook_events(
        self, s: SimState, evs: list[SimEvent], stats: SimStats
    ) -> list | None:
        did_cast = any(ev.type == "cast" for ev in evs)
        if did_cast:
            c = self._constants(s)
            self._start_buff(s, c)

        buff = s.buffs.get(self.BUFF_KEY, None)
        if buff and s.t > buff["until"]:
            self._end_buff(s)

    def _start_buff(self, s: "SimState", c: dict):
        s.buffs[self.BUFF_KEY] = dict(
            until=s.t + c["ASDuration"],
            bonus_speed_mult=c["AttackSpeedToGive"] / 100,
        )

    def _end_buff(self, s: "SimState"):
        del s.buffs[self.BUFF_KEY]


ITEM_QUIRK_MAP = {
    cls.id: cls
    for cls in locals().values()
    if type(cls) == ABCMeta and issubclass(cls, ItemQuirks) and cls is not ItemQuirks
}
