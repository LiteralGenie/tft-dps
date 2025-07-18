from dataclasses import dataclass


@dataclass
class CalcCtx:
    T: int
    stats: "CalcCtxStats"
    items: dict[str, int]


@dataclass
class CalcCtxStats:
    ad: float
    ap: float
    speed: float

    cast_time: float
    mana_initial: int
    mana_max: int
    mana_per_auto: int
