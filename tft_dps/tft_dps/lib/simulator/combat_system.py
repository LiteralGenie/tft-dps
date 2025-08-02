from .sim_event import SimEvent
from .sim_state import SimAttack, SimCast, SimState, SimStats
from .sim_system import SimSystem


class CombatSystem(SimSystem):
    """attack -> cast delay -> cast -> attack delay"""

    def __init__(self) -> None:
        self.attack_state: dict = dict(
            type="POST_AUTO",
            until=0,
        )
        self.mana = 0

    def hook_stats_override(self, s: SimState, stats: SimStats):
        if s.t == 0:
            # On first tick, use mana bonus from items as current mana
            stats.mana = self.mana
        else:
            # Otherwise override with own value, incremented by autos / regen, decremented by casts
            self.mana = stats.mana

    def hook_main(self, s: SimState, stats: SimStats):
        evs = []

        try:
            match self.attack_state["type"]:
                case "POST_AUTO":
                    # Wait for attack-speed based delay
                    if s.t < self.attack_state["until"]:
                        return evs

                    # Auto
                    evs.append(self._auto(s, stats))
                    if s.mana_locks == 0:
                        stats.mana += stats.mana_per_auto

                    if s.mana_locks == 0 and stats.mana >= stats.mana_max:
                        # Start casting
                        stats.mana -= stats.mana_max
                        self.attack_state = dict(
                            type="PRE_CAST",
                            until=s.t + stats.cast_time,
                        )
                    else:
                        # Start next auto
                        self.attack_state = self._calc_post_auto_state(s, stats)
                case "PRE_CAST":
                    # Wait for cast-time based delay
                    if s.t < self.attack_state["until"]:
                        return evs

                    # Cast
                    evs.append(self._cast(s, stats))

                    # Start auto
                    self.attack_state = self._calc_post_auto_state(s, stats)
                case _:
                    raise Exception()

            return evs
        finally:
            self.mana = stats.mana

    def _auto(self, s: SimState, stats: SimStats):
        d = s.ctx.unit_quirks.get_auto_damage(s, stats)
        s.attacks.append(
            SimAttack(
                t=s.t,
                physical_damage=d.get("physical", 0),
                magical_damage=d.get("magical", 0),
                true_damage=d.get("true", 0),
            )
        )
        return SimEvent(
            type="auto",
            data=s.attacks[-1],
        )

    def _cast(self, s: SimState, stats: SimStats):
        d = s.ctx.unit_quirks.get_spell_damage(s, stats)
        s.casts.append(
            SimCast(
                t=s.t,
                physical_damage=d.get("physical", 0),
                magical_damage=d.get("magical", 0),
                true_damage=d.get("true", 0),
            )
        )
        return SimEvent(
            type="cast",
            data=s.attacks[-1],
        )

    def _calc_post_auto_state(self, s: SimState, stats: SimStats):
        delay = 1 / stats.speed
        return dict(
            type="POST_AUTO",
            until=s.t + delay,
        )
