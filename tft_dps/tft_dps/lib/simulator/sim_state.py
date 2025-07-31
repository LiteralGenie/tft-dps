from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, TypedDict

from .sim_event import SimEvent
from .sim_system import SimSystem

if TYPE_CHECKING:
    from ..calc_ctx import CalcCtx


@dataclass
class SimState:
    ctx: "CalcCtx"
    systems: list[SimSystem]
    events: list[SimEvent]
    t: float
    attacks: list["SimAttack"]
    casts: list["SimCast"]
    stats: "SimStats"
    buffs: dict[str, Any]
    mana_locks: int

    def as_dict(self):
        return dict(
            t=self.t,
            attacks=self.attacks,
            casts=self.casts,
        )


@dataclass
class SimStats:
    ad: float
    ap: float
    speed: float
    mana: float
    mana_max: float
    health: float
    health_max: float

    def __add__(self, other: "SimStats") -> "SimStats":
        return SimStats(
            ad=self.ad + other.ad,
            ap=self.ap + other.ap,
            speed=self.speed + other.speed,
            mana=self.mana + other.mana,
            mana_max=self.mana_max + other.mana_max,
            health=self.health + other.health,
            health_max=self.health_max + other.health_max,
        )

    def __radd__(self, other: "SimStats") -> "SimStats":
        return self.__add__(other)

    def to_raw(self):
        return {
            0: self.ap,
            1: 0,
            2: self.ad,
            3: 1,
            4: self.speed,
            6: 0,
            7: 0,
            8: 0,
            9: 1.4,
            12: self.health_max,
            29: 0,
            34: 1,
        }

    @classmethod
    def zeros(cls):
        return cls(0, 0, 0, 0, 0, 0, 0)


class SimAttack(TypedDict):
    t: float
    physical_damage: float
    magical_damage: float


class SimCast(TypedDict):
    t: float
    physical_damage: float
    magical_damage: float


class SimResult(TypedDict):
    attacks: list[SimAttack]
    casts: list[SimCast]
    initial_stats: SimStats
    final_stats: SimStats
    notes: list[str]
