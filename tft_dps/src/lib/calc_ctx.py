from dataclasses import dataclass

from lol_resolver.tft.units import TFTUnitsProcessor


@dataclass
class CalcCtx:
    T: int
    unit_id: str
    stats: "CalcCtxStats"
    item_inventory: dict[str, int]
    item_info: dict[str, dict]
    unit_proc: TFTUnitsProcessor


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

    @classmethod
    def from_unit(cls, stars: int, unit: dict):
        s = unit["stats"]

        return cls(
            stars=stars,
            ad=s["attackDamage"],
            ap=100,
            health=s["health"],
            speed=s["attackSpeed"],
            cast_time=0.5,
            mana_initial=s["startingMana"],
            mana_max=s["maxMana"],
            mana_per_auto=s["manaPerAttack"],
        )
