from ..calc_ctx import CalcCtx
from .combat_system import CombatSystem
from .sim_state import SimResult, SimState, SimStats
from .sim_system import SimSystem

"""
Simulate game loop

First bootstrap ...
    systems - functions invoked each tick (loop iteration)
    base stats - 1* unit stats, scaling from stars and items recalculated each tick
    state (see below)

Then run main gameloop where on each tick ...
    iterate over each system and ...
        calculate stat values
        run system's hook_main()
            systems can return a list of "events" (arbitrary data) that's later communicated to other systems
    iterate over each system again ...
        calculate stat values
        run hook_events(), giving each a system a chance to respond to events from previous phase
            systems can again return events that's appened to a new event array
        continue this phase until no events are emitted

State is mainly ...
    - current time
    - damage dealt
    - buffs
        arbitrary data that needs to persist over multiple ticks
        each entry is usually only generated and used by a single system
            just to muddy matters, systems dont have to store state here
            eg the CombatSystem uses instance properties for whether the next attack is an auto or cast
            but all of the UnitSystem subclasses use SimState.buffs
            it just bothers me to call the first one a buff ¯\_(ツ)_/¯

In constrast, events ...
    - are meant for communication between systems
    - only live a single tick
so events can be seen as
    data from one system
    that needs the help of another system
    before it can be stored on the main state
"""

TICK_PERIOD_MS = 10


def simulate(ctx: CalcCtx) -> SimResult:
    s = SimState(
        t=0,
        systems=_init_systems(ctx),
        ctx=ctx,
        attacks=[],
        casts=[],
        misc_damage=[],
        buffs=dict(),
        mana_locks=0,
    )

    for sys in s.systems:
        sys.hook_init(s)

    # Side effects from hook_stats() and hook_stats_override() is necessary here
    initial_stats = _calc_stats(s)

    while s.t <= ctx.T:
        new_events = []
        for sys in s.systems:
            stats = _calc_stats(s)
            evs = sys.hook_main(s, stats) or []
            new_events.extend(evs)

        max_its = 20
        for idx in range(max_its):
            prev_events = new_events
            new_events = []

            for sys in s.systems:
                stats = _calc_stats(s)
                evs = sys.hook_events(s, prev_events, stats) or []
                new_events.extend(evs)

            if not new_events:
                break
        else:
            raise Exception("Possibly infinite hook_events() phase")

        s.t += TICK_PERIOD_MS / 1000

    final_stats = _calc_stats(s)

    return SimResult(
        attacks=s.attacks,
        casts=s.casts,
        misc_damage=s.misc_damage,
        initial_stats=initial_stats,
        final_stats=final_stats,
        has_errors=False,
    )


def _init_systems(ctx: CalcCtx):
    systems: list[SimSystem] = [
        CombatSystem(),
        ctx.unit_quirks,
    ]

    return systems


def _calc_stats(s: SimState) -> SimStats:
    base = _init_stats(s.ctx)

    bonus = SimStats.zeros()
    for sys in s.systems:
        if b := sys.hook_stats(s):
            bonus += b

    total = base + bonus

    for sys in s.systems:
        sys.hook_stats_override(s, total)

    return total


def _init_stats(ctx: CalcCtx) -> SimStats:
    b = ctx.base_stats

    stats = SimStats(
        ad=b.ad,
        ad_mult=1,
        ap=b.ap,
        speed=b.speed,
        speed_mult=1,
        mana=b.mana_initial,
        mana_max=b.mana_max,
        mana_per_auto=b.mana_per_auto,
        mana_regen=0,
        health_max=b.health,
        health_mult=1,
        armor=b.armor,
        mr=b.mr,
        crit_rate=b.crit_rate,
        crit_mult=b.crit_mult,
        cast_time=b.cast_time,
        range=b.range,
        move_speed=b.move_speed,
        amp=0,
    )

    stats.ad *= 1.5 ** (ctx.base_stats.stars - 1)
    stats.health_max *= 1.8 ** (ctx.base_stats.stars - 1)

    return stats
