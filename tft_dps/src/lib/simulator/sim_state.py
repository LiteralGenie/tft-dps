from dataclasses import dataclass

from lib.calc_ctx import CalcCtx
from lib.simulator.sim_event import SimEvent
from lib.simulator.sim_system import SimSystem


@dataclass
class SimState:
    ctx: CalcCtx
    systems: list[SimSystem]
    events: list[SimEvent]
    t: float
    attacks: list["SimAttack"]
    casts: list["SimCast"]
    stats: "SimStats"


@dataclass
class SimStats:
    ad: float
    ap: float
    speed: float
    mana: int
    mana_max: int
    health: int
    health_max: int


@dataclass(frozen=True)
class SimAttack:
    t: float
    damage: float


@dataclass(frozen=True)
class SimCast:
    t: float
    damage: float
