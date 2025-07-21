from lib.simulator.sim_event import SimEvent
from lib.simulator.sim_state import SimAttack, SimCast, SimState
from lib.simulator.sim_system import SimSystem


class CombatSystem(SimSystem):
    """attack -> cast delay -> cast -> attack delay"""

    """
    @todo
        mana per auto
        cast damage
        events
    """

    def __init__(self) -> None:
        self.state: dict = dict(
            type="POST_AUTO",
            until=0,
        )

        self.mana_per_auto = 10

    def run(self, s: SimState):
        match self.state["type"]:
            case "POST_AUTO":
                # Wait for attack-speed based delay
                if s.t < self.state["until"]:
                    return

                # Auto
                self._auto(s)
                s.stats.mana += self.mana_per_auto

                if s.stats.mana >= s.stats.mana_max:
                    # Start casting
                    s.stats.mana -= s.stats.mana_max
                    self.state = dict(
                        type="PRE_CAST",
                        until=s.t + s.ctx.stats.cast_time,
                    )
                else:
                    # Start next auto
                    self.state = dict(
                        type="POST_AUTO",
                        until=0,
                    )
            case "PRE_CAST":
                # Wait for cast-time based delay
                if s.t < self.state["until"]:
                    return

                # Cast
                self._cast(s)

                # Start auto
                delay = (1 / s.stats.speed,)
                self.state = dict(
                    type="POST_AUTO",
                    until=delay,
                )
            case _:
                raise Exception()

    def _auto(self, s: SimState):
        s.attacks.append(
            SimAttack(
                s.t,
                s.stats.ad,
            )
        )
        s.events.append(
            SimEvent(
                type="auto",
                data=s.attacks[-1],
            )
        )

    def _cast(self, s: SimState):
        s.casts.append(SimCast(s.t, 0))
        s.events.append(
            SimEvent(
                type="cast",
                data=s.attacks[-1],
            )
        )
