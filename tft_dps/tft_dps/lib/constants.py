VERSION = "latest"
PORT = 4723

MAX_IDS_PER_SIMULATE = 10_000
PACKED_ID_BITS = 40

ITEMS = [
    "TFT_Item_BFSword",
    "TFT_Item_NeedlesslyLargeRod",
    "TFT_Item_RecurveBow",
    "TFT_Item_SparringGloves",
    "TFT_Item_TearOfTheGoddess",
    "TFT_Item_GiantsBelt",
    "TFT_Item_ChainVest",
    "TFT_Item_NegatronCloak",
    #
    "TFT_Item_Deathblade",
    "TFT_Item_HextechGunblade",
    "TFT_Item_MadredsBloodrazor",  # giant slayer
    "TFT_Item_InfinityEdge",
    "TFT_Item_SpearOfShojin",
    "TFT_Item_SteraksGage",
    "TFT_Item_GuardianAngel",  # edge of night
    "TFT_Item_Bloodthirster",
    #
    "TFT_Item_RabadonsDeathcap",
    "TFT_Item_GuinsoosRageblade",
    "TFT_Item_JeweledGauntlet",
    "TFT_Item_ArchangelsStaff",
    "TFT_Item_Morellonomicon",
    "TFT_Item_Crownguard",
    "TFT_Item_IonicSpark",
    #
    "TFT_Item_RapidFireCannon",  # red buff
    "TFT_Item_LastWhisper",
    "TFT_Item_StatikkShiv",  # void staff
    "TFT_Item_Leviathan",  # nashors tooth
    "TFT_Item_TitansResolve",
    "TFT_Item_RunaansHurricane",  # kraken's fury
    #
    "TFT_Item_ThiefsGloves",
    "TFT_Item_UnstableConcoction",  # hand of justice
    "TFT_Item_PowerGauntlet",  # strikers flail
    "TFT_Item_NightHarvester",  # steadfast heart
    "TFT_Item_Quicksilver",
    #
    "TFT_Item_BlueBuff",
    "TFT_Item_Redemption",  # spirit visage
    "TFT_Item_FrozenHeart",  # protectors vow
    "TFT_Item_AdaptiveHelm",
    #
    "TFT_Item_WarmogsArmor",
    "TFT_Item_RedBuff",  # sunfire
    "TFT_Item_SpectralGauntlet",  # evenshroud
    #
    "TFT_Item_BrambleVest",  # bramble vest
    "TFT_Item_GargoyleStoneplate",
    #
    "TFT_Item_DragonsClaw",
]

CHAMPION_UNITS = [
    "Characters/TFT15_Aatrox",
    "Characters/TFT15_Ahri",
    "Characters/TFT15_Akali",
    "Characters/TFT15_Ashe",
    "Characters/TFT15_Braum",
    "Characters/TFT15_Caitlyn",
    "Characters/TFT15_Darius",
    "Characters/TFT15_Ezreal",
    "Characters/TFT15_Garen",
    "Characters/TFT15_Gwen",
    "Characters/TFT15_Janna",
    "Characters/TFT15_JarvanIV",
    "Characters/TFT15_Jayce",
    "Characters/TFT15_Jhin",
    "Characters/TFT15_Jinx",
    "Characters/TFT15_KSante",
    "Characters/TFT15_KaiSa",
    "Characters/TFT15_Kalista",
    "Characters/TFT15_Katarina",
    "Characters/TFT15_Kayle",
    "Characters/TFT15_Kennen",
    "Characters/TFT15_Kobuko",
    # "Characters/TFT15_LeeSin",
    "Characters/TFT15_Leona",
    # "Characters/TFT15_Lulu",
    "Characters/TFT15_Lux",
    "Characters/TFT15_Malphite",
    "Characters/TFT15_Malzahar",
    "Characters/TFT15_Naafiri",
    "Characters/TFT15_Poppy",
    "Characters/TFT15_Rakan",
    "Characters/TFT15_Rell",
    "Characters/TFT15_Ryze",
    "Characters/TFT15_Samira",
    # "Characters/TFT15_Seraphine",
    "Characters/TFT15_Sett",
    "Characters/TFT15_Swain",
    "Characters/TFT15_Syndra",
    "Characters/TFT15_Udyr",
    # "Characters/TFT15_Varus",
    "Characters/TFT15_Viego",
    "Characters/TFT15_Xayah",
    "Characters/TFT15_XinZhao",
    "Characters/TFT15_Yasuo",
    "Characters/TFT15_Yone",
    "Characters/TFT15_Yuumi",
    "Characters/TFT15_Zac",
    "Characters/TFT15_Ziggs",
    # "Characters/TFT15_Swain_DemonForm",
    "Characters/TFT15_Volibear",
    # "Characters/TFT15_KogMaw",
    # "Characters/TFT15_Smolder",
    "Characters/TFT15_Senna",
    "Characters/TFT15_Lucian",
    "Characters/TFT15_Gangplank",
    "Characters/TFT15_DrMundo",
    "Characters/TFT15_Gnar",
    "Characters/TFT15_Karma",
    "Characters/TFT15_Vi",
    # "Characters/TFT15_Galio",
    "Characters/TFT15_Sivir",
    "Characters/TFT15_TwistedFate",
    "Characters/TFT15_Shen",
    # "Characters/TFT15_Rammus",
    # "Characters/TFT15_Thresh",
    # "Characters/TFT15_Zyra",
    "Characters/TFT15_Neeko",
    # "Characters/TFT15_Ekko",
]

FLAGS = dict(
    gnar_max_damage=10_000,
    kayle_wave_frequency=3,
    kayle_aoe_targets=1.25,
    malphite_aoe_targets=2,
    rell_aoe_targets=2,
    sivir_aoe_targets=3,
    zac_aoe_targets=2,
    #
    kaisa_passive_stacks=40,
    katarina_aoe_targets=2,
    lux_aoe_targets=2,
    vi_aoe_targets=2,
    xin_aoe_targets=2,
    #
    ahri_missing_hp_bonus=1.2,
    ahri_overkill_frequency=3,
    darius_spell_bonus_mult=0.9,
    darius_kill_frequency=5,
    jayce_aoe_targets=2,
    neeko_aoe_targets=2,
    senna_aoe_targets=3,
    swain_aoe_targets=2,
    udyr_aoe_targets=2,
    ziggs_aoe_targets=2,
    #
    akali_strike_targets=3,
    akali_dash_targets=2,
    jarvan_aoe_targets=4,
    ksante_allout_delay=7,
    karma_aoe_targets=2,
    leona_aoe_targets=4,
    leona_sunburst_targets=5,
    poppy_shield_duration=3,
    poppy_aoe_targets=2,
    ryze_aoe_targets=2,
    samira_aoe_targets=4,
    sett_aoe_targets=2,
    sett_spell_heal_mult=2,
    volibear_aoe_targets=2,
    volibear_slam_frequency=7,
    #
    braum_aoe_targets_primary=3,
    braum_aoe_targets_secondary=2,
    braum_execute_bonus=0.5,
    gwen_aoe_targets_spell=6,
    gwen_aoe_targets_auto=4,
    # seraphine_aoe_targets=7,
    yone_aoe_targets=6,
    zyra_decay=0.5,
    #
    item_spark_damage=300,
    item_spark_frequency=3,
    burn_damage_amp=2,
    sunfire_burn_damage=4,
    gargoyle_num_enemies=6,
    titans_stack_frequency=0.4,
    giant_bonus_amp_frac=50,
    bramble_aoe_targets=3,
    #
    tank_mana_regen=0.2,
    #
    sniper_hexes=4,
    star_jinx_as=10,
)
