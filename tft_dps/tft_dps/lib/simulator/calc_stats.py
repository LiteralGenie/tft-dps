from ..calc_ctx import CalcCtx
from .sim_state import SimState, SimStats


def calc_stats(s: SimState) -> SimStats:
    curr = s.stats

    bonus = SimStats.zeros()
    bonus += _sum_item_bonus(s)

    if unit_bonus := s.ctx.unit_quirks.get_unit_bonus(s):
        bonus += unit_bonus

    health = _calc_hp(s, bonus)

    update = SimStats(
        ad=_calc_ad(s, bonus),
        ap=_calc_ap(s, bonus),
        speed=_calc_as(s, bonus),
        mana=curr.mana,
        mana_max=curr.mana_max,
        health=health,
        health_max=health,
        armor=0,
        mr=0,
        crit_rate=0,
        crit_mult=0,
        cast_time=0,
    )

    update = s.ctx.unit_quirks.get_stats_override(s, update)

    return update


def init_stats(ctx: CalcCtx) -> SimStats:
    b = ctx.base_stats

    stats = SimStats(
        ad=b.ad,
        ap=b.ap,
        speed=b.speed,
        mana=b.mana_initial,
        mana_max=b.mana_max,
        health=b.health,
        health_max=b.health,
        armor=0,
        mr=0,
        crit_rate=0,
        crit_mult=0,
        cast_time=0,
    )

    return stats


def _item_to_stats(item: dict) -> SimStats:
    c = {k: v["mValue"] for k, v in item["constants"].items()}

    return SimStats(
        ad=c.get("AD", 0),
        ap=c.get("AP", 0),
        speed=c.get("AS", 0),
        mana=c.get("Mana", 0),
        mana_max=0,
        health=c.get("Health", 0),
        health_max=c.get("Health", 0),
        armor=0,
        mr=0,
        crit_rate=0,
        crit_mult=0,
        cast_time=0,
    )


def _sum_item_bonus(s: SimState) -> SimStats:
    bonus = SimStats.zeros()

    for name, count in s.ctx.item_inventory.items():
        for _ in range(count):
            item = _item_to_stats(s.ctx.item_info[name])
            bonus += item

    return bonus


def _calc_ad(s: SimState, bonus: SimStats):
    base = s.ctx.base_stats

    ad = base.ad
    ad *= 1.5 ** (base.stars - 1)
    ad *= 1 + bonus.ad / 100

    return ad


def _calc_hp(s: SimState, bonus: SimStats):
    base = s.ctx.base_stats

    hp = base.health
    hp *= 1.8 ** (base.stars - 1)
    hp *= 1 + bonus.health / 100

    return hp


def _calc_ap(s: SimState, bonus: SimStats):
    base = s.ctx.base_stats

    ap = base.ap
    ap += bonus.ap

    return ap


def _calc_as(s: SimState, bonus: SimStats):
    b = s.ctx.base_stats

    speed = b.speed
    speed *= 1 + bonus.speed / 100

    return speed
