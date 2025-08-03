from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, TypedDict

from .sim_system import SimSystem

if TYPE_CHECKING:
    from ..calc_ctx import CalcCtx


@dataclass
class SimState:
    ctx: "CalcCtx"
    systems: list[SimSystem]
    t: float
    attacks: list["SimAttack"]
    casts: list["SimCast"]
    # currently no events for misc damage
    misc_damage: list["SimMiscDamage"]
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
    ad: float  # not-a-small-frac
    ad_mult: float
    ap: float  # not-a-small-frac
    speed: float
    speed_mult: float
    mana: float  # not-a-small-frac
    mana_max: float
    mana_regen: float
    mana_per_auto: float
    health_max: float  # not-a-small-frac
    health_mult: float
    armor: float  # not-a-small-frac
    mr: float  # not-a-small-frac
    crit_rate: float
    crit_mult: float
    cast_time: float
    range: float
    move_speed: float
    amp: float

    def __add__(self, other: "SimStats") -> "SimStats":
        return SimStats(
            health_mult=1,
            #
            ad=self.ad + other.ad,
            ad_mult=self.ad_mult + other.ad_mult,
            ap=self.ap + other.ap,
            speed=self.speed + other.speed,
            speed_mult=self.speed_mult + other.speed_mult,
            mana=self.mana + other.mana,
            mana_max=self.mana_max + other.mana_max,
            mana_regen=self.mana_regen + other.mana_regen,
            mana_per_auto=self.mana_per_auto + other.mana_per_auto,
            health_max=self.health_max + other.health_max,
            armor=self.armor + other.armor,
            mr=self.mr + other.mr,
            crit_rate=self.crit_rate + other.crit_rate,
            crit_mult=self.crit_mult + other.crit_mult,
            cast_time=self.cast_time + other.cast_time,
            range=self.range + other.range,
            move_speed=self.move_speed + other.move_speed,
            amp=self.amp + other.amp,
        )

    def __radd__(self, other: "SimStats") -> "SimStats":
        return self.__add__(other)

    def to_raw(self):
        return {
            0: self.ap,
            1: self.armor,
            2: self.effective_ad,
            3: 1,
            4: self.effective_speed,
            6: self.mr,
            7: 0,
            8: self.crit_rate,
            9: self.crit_mult,
            12: self.effective_health,
            29: 0,
            34: 1,
        }

    @classmethod
    def zeros(cls):
        return cls(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    @property
    def effective_ad(self):
        return self.ad * self.ad_mult

    @property
    def effective_health(self):
        return self.health_max * self.health_mult

    @property
    def effective_speed(self):
        return self.speed * self.speed_mult

    @property
    def crit_bonus(self):
        return 1 + (self.crit_mult - 1) * self.crit_rate


class SimAttack(TypedDict):
    t: float
    physical_damage: float
    magical_damage: float
    true_damage: float


class SimCast(TypedDict):
    t: float
    physical_damage: float
    magical_damage: float
    true_damage: float


class SimMiscDamage(TypedDict):
    t: float
    physical_damage: float
    magical_damage: float
    true_damage: float


class SimResult(TypedDict):
    attacks: list[SimAttack]
    casts: list[SimCast]
    misc_damage: list[SimMiscDamage]
    initial_stats: SimStats
    final_stats: SimStats
