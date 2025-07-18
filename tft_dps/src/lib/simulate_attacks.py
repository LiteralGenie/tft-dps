from dataclasses import dataclass

from calc_ctx import CalcCtx


@dataclass
class SimState:
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


@dataclass(frozen=True)
class SimAttack:
    t: float
    damage: float


@dataclass(frozen=True)
class SimCast:
    t: float
    damage: float


def simulate(ctx: CalcCtx) -> SimState:
    s = SimState(
        t=0,
        attacks=[],
        casts=[],
        stats=SimStats(
            ad=calc_ad_initial(ctx),
            ap=calc_ap_initial(ctx),
            speed=calc_speed_initial(ctx),
            mana=calc_mana_initial(ctx),
        ),
    )

    mana_per_auto = calc_mana_per_auto(ctx)

    while True:
        # Auto attack
        s.attacks.append(SimAttack(s.t, s.stats.ad))
        s.stats.mana += mana_per_auto

        # Spell cast
        if s.stats.mana >= ctx.stats.mana_max:
            s.stats.mana -= ctx.stats.mana_max
            s.casts.append(generate_cast(s, ctx))

            simulate_time_step(ctx.stats.cast_time, s, ctx)
            if s.t > ctx.T:
                break

        # Next attack delay
        simulate_time_step(1 / s.stats.speed, s, ctx)
        if s.t > ctx.T:
            break

    return s


def simulate_time_step(elapsed: float, s: SimState, ctx: CalcCtx):
    ti = s.t
    tf = s.t + elapsed

    # Rageblade
    ti_floor = int(ti)
    tf_floor = int(tf)

    steps = tf_floor - ti_floor
    s.stats.speed += 0.05 * steps * ctx.items["rageblade"]

    return s


def generate_cast(s: SimState, ctx: CalcCtx) -> SimCast:
    return SimCast(
        t=s.t,
        damage=0,
    )


def calc_mana_initial(ctx: CalcCtx):
    return 0


def calc_speed_initial(ctx: CalcCtx):
    return 0.75


def calc_ad_initial(ctx: CalcCtx):
    return 45


def calc_ap_initial(ctx: CalcCtx):
    return 100


def calc_mana_per_auto(ctx: CalcCtx):
    return 10
