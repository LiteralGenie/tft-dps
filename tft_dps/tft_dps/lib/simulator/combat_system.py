from tft_dps.lib.simulator.quirks.item_quirks import SpearOfShojinQuirks
from tft_dps.lib.simulator.quirks.trait_quirks import (
    OldMentorQuirks,
    StarGuardianQuirks,
)

from .sim_state import SimAttack, SimCast, SimState, SimStats
from .sim_system import SimEvent, SimSystem


class CombatSystem(SimSystem):
    """attack -> cast delay -> cast -> attack delay"""

    FLAG_KEY_TANK_MANA_REGEN = "tank_mana_regen"
    notes = [
        "For tanks, mana from damage is modeled as {FLAG_KEY_TANK_MANA_REGEN}% of the unit's max health gained as mana every second"
    ]

    def __init__(self) -> None:
        self.attack_state: dict = dict(
            type="POST_AUTO",
            until=0,
        )
        self.mana = 0
        self.shojin_bonus = 0
        self.last_mana_regen_tick = 0
        self.tank_mana_regen = 0

    def hook_init(self, s: SimState):
        num_shojin = len(
            [id for id in s.ctx.item_inventory if id == SpearOfShojinQuirks.id]
        )
        item_info = s.ctx.item_info[SpearOfShojinQuirks.id]
        self.shojin_bonus = num_shojin * item_info["constants"]["FlatManaRestore"]

    def hook_stats_override(self, s: SimState, stats: SimStats):
        if s.t == 0:
            # On first tick, use mana bonus from items as current mana
            stats.mana = self.mana
        else:
            # Otherwise override with own value, incremented by autos / regen, decremented by casts
            self.mana = stats.mana

        self.tank_mana_regen = (
            stats.health_max * s.ctx.flags[self.FLAG_KEY_TANK_MANA_REGEN] / 100
        )

    def hook_main(self, s: SimState, stats: SimStats):
        evs = []

        t_sec = int(s.t)
        if t_sec > self.last_mana_regen_tick:
            self.last_mana_regen_tick = t_sec

            if s.mana_locks == 0:
                stats.mana += stats.mana_regen
                stats.mana += self.tank_mana_regen

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
                        stats.mana += self.shojin_bonus
                        stats.mana += s.buffs.get(OldMentorQuirks.BUFF_KEY_RYZE, 0)

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

                    if sg_ahri_mana := s.buffs.get(StarGuardianQuirks.BUFF_KEY_AHRI):
                        stats.mana += sg_ahri_mana
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
                physical_damage=d.phys,
                magical_damage=d.magic,
                true_damage=d.true,
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
                physical_damage=d.phys,
                magical_damage=d.magic,
                true_damage=d.true,
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
