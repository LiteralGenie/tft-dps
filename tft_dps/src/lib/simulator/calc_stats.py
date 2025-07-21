from lib.calc_ctx import CalcCtx
from lib.simulator.sim_state import SimState, SimStats


def calc_stats(s: SimState) -> SimStats:
    curr = s.stats

    return SimStats(
        ad=_calc_ad(s),
        ap=_calc_ap(s),
        speed=_calc_as(s),
        mana=curr.mana,
        mana_max=curr.mana_max,
        health=curr.health,
        health_max=curr.health_max,
    )


def init_stats(ctx: CalcCtx) -> SimStats:
    b = ctx.stats

    stats = SimStats(
        ad=b.ad,
        ap=b.ap,
        speed=b.speed,
        mana=b.mana_initial,
        mana_max=b.mana_max,
        health=b.health,
        health_max=b.health,
    )

    return stats


def _calc_ad(s: SimState):
    b = s.ctx.stats

    ad = b.ad
    ad *= b.stars**1.5

    bonus = 0
    for item, count in s.ctx.items:
        bonus += 0

    ad *= 1 + bonus

    return ad


def _calc_ap(s: SimState):
    b = s.ctx.stats

    ad = b.ad
    ad *= b.stars**1.5

    bonus = 0
    for item, count in s.ctx.items:
        bonus += 0

    ad *= 1 + bonus

    return ad


def _calc_as(s: SimState):
    b = s.ctx.stats

    speed = b.speed

    bonus = 0
    for item, count in s.ctx.items:
        bonus += 0

    speed *= 1 + bonus

    return speed
