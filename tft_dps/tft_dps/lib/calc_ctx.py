from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..lol_resolver.tft.units import TFTUnitsProcessor

if TYPE_CHECKING:
    from .simulator.quirks.quirks import ItemQuirks, UnitQuirks


@dataclass
class CalcCtx:
    T: int
    unit_id: str
    unit_info: dict
    base_stats: "CalcCtxStats"
    item_inventory: list[str]
    item_info: dict[str, dict]
    item_quirks: list["ItemQuirks"]
    trait_inventory: dict[str, "CalcCtxTraits"]
    trait_info: dict
    unit_proc: TFTUnitsProcessor
    unit_quirks: "UnitQuirks"
    flags: dict


@dataclass
class CalcCtxStats:
    stars: int

    ad: float
    ap: float
    health: int
    speed: float

    cast_time: float
    mana_initial: int
    mana_max: int
    mana_per_auto: int

    crit_rate: float
    crit_mult: float

    range: float
    move_speed: float

    armor: float
    mr: float

    @classmethod
    def from_unit(cls, id: str, stars: int, unit_proc: TFTUnitsProcessor):
        base = unit_proc.get_base_stats(id)
        root = unit_proc.get_root_record(id)

        return cls(
            stars=stars,
            ad=base[2],
            ap=base[0],
            health=base[12],
            speed=base[4],
            cast_time=0.5,
            mana_initial=base[12],
            mana_max=root.get("maxMana", 0),
            mana_per_auto=root.get("primaryAbilityResource", dict()).get("arBase", 100),
            crit_rate=base[8],
            crit_mult=base[9],
            range=base[7],
            move_speed=base[29],
            armor=base[1],
            mr=base[6],
        )


@dataclass
class CalcCtxTraits:
    id: str
    breakpoint: int
    index: int
    effects: dict
