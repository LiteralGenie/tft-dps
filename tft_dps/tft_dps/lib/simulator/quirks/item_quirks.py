from abc import ABCMeta

from tft_dps.lib.simulator.quirks.quirks import ItemQuirks
from tft_dps.lib.simulator.sim_state import SimState, SimStats


class BFQuirks(ItemQuirks):
    id = "TFT_Item_BFSword"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        bonus.ad = c["AD"] * 100

        return bonus


class BloodthirsterQuirks(ItemQuirks):
    id = "TFT_Item_Bloodthirster"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        bonus.ad = c["AD"] * 100
        bonus.ap = c["AP"]
        bonus.mr = c["MagicResist"]

        return bonus


class BrambleVestQuirks(ItemQuirks):
    id = "TFT_Item_BrambleVest"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        bonus.health_mult = c["PercentMaxHP"]
        bonus.armor = c["Armor"]

        return bonus


class ChainVestQuirks(ItemQuirks):
    id = "TFT_Item_ChainVest"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        bonus.armor = c["Armor"]

        return bonus


class SparringGlovesQuirks(ItemQuirks):
    id = "TFT_Item_SparringGloves"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        bonus.crit_rate = c["CritChance"]

        return bonus


class DeathbladeQuirks(ItemQuirks):
    id = "TFT_Item_Deathblade"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        bonus.ad = c["AD"] * 100
        bonus.amp = c["BonusDamage"]

        return bonus


class DragonsClawQuirks(ItemQuirks):
    id = "TFT_Item_DragonsClaw"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        bonus.health_mult = c["PercentMaxHP"]
        bonus.mr = c["MagicResist"]

        return bonus


class ThiefsGlovesQuirks(ItemQuirks):
    id = "TFT_Item_ThiefsGloves"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        bonus.crit_rate = c["CritChance"]
        bonus.health_max = c["Health"]

        return bonus


class ProtectorsVowQuirks(ItemQuirks):
    id = "TFT_Item_FrozenHeart"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        bonus.mana_regen = c["ManaRegen"]
        bonus.armor = c["Armor"]
        bonus.mr = c["MagicResist"]
        bonus.mana

        return bonus


class GiantsBeltQuirks(ItemQuirks):
    id = "TFT_Item_GiantsBelt"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        return bonus


class MadredsBloodrazorQuirks(ItemQuirks):
    id = "TFT_Item_MadredsBloodrazor"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        return bonus


class GuardianAngelQuirks(ItemQuirks):
    id = "TFT_Item_GuardianAngel"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        return bonus


class GuinsoosRagebladeQuirks(ItemQuirks):
    id = "TFT_Item_GuinsoosRageblade"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        return bonus


class UnstableConcoctionQuirks(ItemQuirks):
    id = "TFT_Item_UnstableConcoction"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        return bonus


class HextechGunbladeQuirks(ItemQuirks):
    id = "TFT_Item_HextechGunblade"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        return bonus


class InfinityEdgeQuirks(ItemQuirks):
    id = "TFT_Item_InfinityEdge"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        return bonus


class IonicSparkQuirks(ItemQuirks):
    id = "TFT_Item_IonicSpark"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        return bonus


class JeweledGauntletQuirks(ItemQuirks):
    id = "TFT_Item_JeweledGauntlet"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        return bonus


class LastWhisperQuirks(ItemQuirks):
    id = "TFT_Item_LastWhisper"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        return bonus


class ArchangelsStaffQuirks(ItemQuirks):
    id = "TFT_Item_ArchangelsStaff"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        return bonus


class QuicksilverQuirks(ItemQuirks):
    id = "TFT_Item_Quicksilver"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        return bonus


class MorellonomiconQuirks(ItemQuirks):
    id = "TFT_Item_Morellonomicon"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        return bonus


class NeedlesslyLargeRodQuirks(ItemQuirks):
    id = "TFT_Item_NeedlesslyLargeRod"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        return bonus


class NegatronCloakQuirks(ItemQuirks):
    id = "TFT_Item_NegatronCloak"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        return bonus


class PowerGauntletQuirks(ItemQuirks):
    id = "TFT_Item_PowerGauntlet"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        return bonus


class RabadonsDeathcapQuirks(ItemQuirks):
    id = "TFT_Item_RabadonsDeathcap"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        return bonus


class RapidFireCannonQuirks(ItemQuirks):
    id = "TFT_Item_RapidFireCannon"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        return bonus


class RecurveBowQuirks(ItemQuirks):
    id = "TFT_Item_RecurveBow"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        return bonus


class RedBuffQuirks(ItemQuirks):
    id = "TFT_Item_RedBuff"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        return bonus


class RedemptionQuirks(ItemQuirks):
    id = "TFT_Item_Redemption"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        return bonus


class RunaansHurricaneQuirks(ItemQuirks):
    id = "TFT_Item_RunaansHurricane"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        return bonus


class SpearOfShojinQuirks(ItemQuirks):
    id = "TFT_Item_SpearOfShojin"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        return bonus


class StatikkShivQuirks(ItemQuirks):
    id = "TFT_Item_StatikkShiv"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        return bonus


class GargoyleStoneplateQuirks(ItemQuirks):
    id = "TFT_Item_GargoyleStoneplate"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        return bonus


class TearOfTheGoddessQuirks(ItemQuirks):
    id = "TFT_Item_TearOfTheGoddess"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        return bonus


class TitansResolveQuirks(ItemQuirks):
    id = "TFT_Item_TitansResolve"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        return bonus


class WarmogsArmorQuirks(ItemQuirks):
    id = "TFT_Item_WarmogsArmor"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        return bonus


class SpectralGauntletQuirks(ItemQuirks):
    id = "TFT_Item_SpectralGauntlet"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        return bonus


class CrownguardQuirks(ItemQuirks):
    id = "TFT_Item_Crownguard"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        return bonus


class NightHarvesterQuirks(ItemQuirks):
    id = "TFT_Item_NightHarvester"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        return bonus


class SteraksGageQuirks(ItemQuirks):
    id = "TFT_Item_SteraksGage"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        return bonus


class BlueBuffQuirks(ItemQuirks):
    id = "TFT_Item_BlueBuff"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        return bonus


class AdaptiveHelmQuirks(ItemQuirks):
    id = "TFT_Item_AdaptiveHelm"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        return bonus


class LeviathanQuirks(ItemQuirks):
    id = "TFT_Item_Leviathan"

    def get_stat_bonus(self, s: SimState) -> SimStats:
        bonus = SimStats.zeros()
        c = self.info(s)["constants"]

        return bonus


ITEM_QUIRK_MAP = {
    cls.id: cls
    for cls in locals().values()
    if type(cls) == ABCMeta and issubclass(cls, ItemQuirks) and cls is not ItemQuirks
}
