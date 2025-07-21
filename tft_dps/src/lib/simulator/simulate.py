from lib.calc_ctx import CalcCtx
from lib.simulator.calc_stats import init_stats
from lib.simulator.combat_system import CombatSystem
from lib.simulator.sim_state import SimState

"""
Simulate combat with N ms ticks via an event-loop-like approach
On each iteration (point in time), a series of systems (functions) are executed
For example, a system that handles combat (auto attacks and spell casts) can be run
Another system that handles passives like archangel's staff will be run after

Systems can have internal state but a global state object will be passed into each system on run
Systems can react to other systems through an event queue.
Each system populates the queue when the system is run. After that system finishes, all systems get a chance to inspect the queue before it is emptied.
"""

TICK_PERIOD_MS = 50


def simulate(ctx: CalcCtx):
    s = SimState(
        t=0,
        systems=[],
        events=[],
        ctx=ctx,
        attacks=[],
        casts=[],
        stats=init_stats(ctx),
    )

    # Init systems
    s.systems.append(CombatSystem())

    while s.t <= ctx.T:
        # print(f"{s.t:.1f}s", s.attacks, s.casts)
        for sys in s.systems:
            s.events = []
            sys.run(s)

            for effect_sys in s.systems:
                effect_sys.run_events(s)

        s.t += TICK_PERIOD_MS / 1000

    return s
