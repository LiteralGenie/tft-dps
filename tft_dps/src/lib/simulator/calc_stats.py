from lib.calc_ctx import CalcCtx
from lib.simulator.sim_state import SimState, SimStats


def calc_stats(s: SimState) -> SimStats:
    curr = s.stats
    bonus = _sum_item_bonus(s)

    return SimStats(
        ad=_calc_ad(s, bonus),
        ap=_calc_ap(s, bonus),
        speed=_calc_as(s, bonus),
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
    )


def _sum_item_bonus(s: SimState) -> SimStats:
    items: list[dict] = []
    for name, count in s.ctx.item_inventory.items():
        items += [s.ctx.item_info[name]] * count

    return sum(_item_to_stats(x) for x in items)  # type: ignore


def _calc_ad(s: SimState, bonus: SimStats):
    base = s.ctx.stats

    ad = base.ad
    ad *= base.stars**1.5
    ad *= 1 + bonus.ad / 100

    return ad


def _calc_ap(s: SimState, bonus: SimStats):
    base = s.ctx.stats

    ap = base.ap
    ap += bonus.ap

    return ap


def _calc_as(s: SimState, bonus: SimStats):
    b = s.ctx.stats

    speed = b.speed
    speed *= 1 + bonus.speed / 100

    return speed
