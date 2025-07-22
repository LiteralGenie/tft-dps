from lib.simulator.sim_event import SimEvent
from lib.simulator.sim_state import SimAttack, SimCast, SimState
from lib.simulator.sim_system import SimSystem


class CombatSystem(SimSystem):
    """attack -> cast delay -> cast -> attack delay"""

    """
    @todo
        cast damage
        events
    """

    def __init__(self) -> None:
        self.state: dict = dict(
            type="POST_AUTO",
            until=0,
        )

    def run(self, s: SimState):
        match self.state["type"]:
            case "POST_AUTO":
                # Wait for attack-speed based delay
                if s.t < self.state["until"]:
                    return

                # Auto
                self._auto(s)
                s.stats.mana += s.ctx.stats.mana_per_auto

                if s.stats.mana >= s.stats.mana_max:
                    # Start casting
                    s.stats.mana -= s.stats.mana_max
                    self.state = dict(
                        type="PRE_CAST",
                        until=s.t + s.ctx.stats.cast_time,
                    )
                else:
                    # Start next auto
                    self.state = self._calc_post_auto_state(s)
            case "PRE_CAST":
                # Wait for cast-time based delay
                if s.t < self.state["until"]:
                    return

                # Cast
                self._cast(s)

                # Start auto
                self.state = self._calc_post_auto_state(s)
            case _:
                raise Exception()

    def _auto(self, s: SimState):
        d = s.ctx.unit_quirks.get_auto_damage(s)
        s.attacks.append(
            SimAttack(
                s.t,
                physical_damage=d["physical"],
                magical_damage=d["magical"],
            )
        )
        s.events.append(
            SimEvent(
                type="auto",
                data=s.attacks[-1],
            )
        )

    def _cast(self, s: SimState):
        d = s.ctx.unit_quirks.get_spell_damage(s)
        s.casts.append(
            SimCast(
                s.t,
                physical_damage=d["physical"],
                magical_damage=d["magical"],
            )
        )
        s.events.append(
            SimEvent(
                type="cast",
                data=s.attacks[-1],
            )
        )

    def _calc_post_auto_state(self, s: SimState):
        delay = 1 / s.stats.speed
        return dict(
            type="POST_AUTO",
            until=s.t + delay,
        )
