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

    PRE_AUTO_DELAY = 0.5

    PRE_CAST_DELAY = 0.3

    def __init__(self) -> None:
        self.attack_state: dict = dict()
        self.mana = 0
        self.shojin_bonus = 0
        self.mana_regen_tick_count = 0
        self.tank_mana_regen = 0
        self.mana_per_auto = 0
        self.bonus_mana_regen = 0

    def hook_init(self, s: SimState):
        num_shojin = len(
            [id for id in s.ctx.item_inventory if id == SpearOfShojinQuirks.id]
        )
        item_info = s.ctx.item_info[SpearOfShojinQuirks.id]
        self.shojin_bonus = (
            num_shojin * item_info["constants"]["FlatManaRestore"]["mValue"]
        )

        role = s.ctx.unit_info["info"]["role"]
        if "Tank" in role:
            self.mana_per_auto = 5
        elif "Fighter" in role:
            self.mana_per_auto = 10
        elif "Assassin" in role:
            self.mana_per_auto = 10
        elif "Marksman" in role:
            self.mana_per_auto = 10
        elif "Caster" in role:
            self.mana_per_auto = 7
            self.bonus_mana_regen = 2

    def hook_stats_override(self, s: SimState, stats: SimStats):
        if s.t == 0:
            # On first tick, use mana bonus from items as current mana
            self.mana = stats.mana
        else:
            # Otherwise override with own value, incremented by autos / regen, decremented by casts
            stats.mana = self.mana

        if "Tank" in s.ctx.unit_info["info"]["role"]:
            self.tank_mana_regen = (
                stats.health_max * s.ctx.flags[self.FLAG_KEY_TANK_MANA_REGEN] / 100
            )

        stats.mana_regen += self.bonus_mana_regen
        stats.mana_per_auto = self.mana_per_auto

        if not self.attack_state:
            self.attack_state = dict(
                type="PRE_AUTO",
                until=self.PRE_AUTO_DELAY * (1 / stats.effective_speed),
            )

    def hook_main(self, s: SimState, stats: SimStats):
        evs = []

        num_ticks = int(s.t * 2)
        if num_ticks > self.mana_regen_tick_count:
            self.mana_regen_tick_count = num_ticks

            if s.mana_locks == 0:
                stats.mana += stats.mana_regen / 2
                stats.mana += self.tank_mana_regen / 2
                # print("regen", stats.mana_regen / 2, self.tank_mana_regen / 2)

        try:
            match self.attack_state["type"]:
                case "PRE_AUTO":
                    # Wait for attack-speed based delay
                    if s.t < self.attack_state["until"]:
                        return evs

                    # Auto
                    evs.append(self._auto(s, stats))
                    if s.mana_locks == 0:
                        stats.mana += stats.mana_per_auto
                        stats.mana += self.shojin_bonus
                        stats.mana += s.buffs.get(OldMentorQuirks.BUFF_KEY_RYZE, 0)
                        # print(
                        #     "auto",
                        #     stats.mana_per_auto,
                        #     self.shojin_bonus,
                        #     s.buffs.get(OldMentorQuirks.BUFF_KEY_RYZE, 0),
                        # )

                    # Post-auto delay
                    self.attack_state = self._calc_post_auto_state(s, stats)
                    return evs
                case "POST_AUTO":
                    can_cast = s.mana_locks == 0 and stats.mana >= stats.mana_max
                    if can_cast:
                        # Start casting
                        stats.mana -= stats.mana_max
                        self.attack_state = dict(
                            type="PRE_CAST",
                            until=s.t + (self.PRE_CAST_DELAY * stats.cast_time),
                        )
                        s.mana_locks += 1
                        return evs

                    # Wait for attack-speed based delay
                    if s.t < self.attack_state["until"]:
                        return evs

                    # Start next auto
                    self.attack_state = self._calc_pre_auto_state(s, stats)
                    return evs
                case "PRE_CAST":
                    # Wait for cast-time based delay
                    if s.t < self.attack_state["until"]:
                        return evs

                    # Cast
                    evs.append(self._cast(s, stats))

                    stats.mana -= stats.mana_max
                    self.attack_state = dict(
                        type="POST_CAST",
                        until=s.t + ((1 - self.PRE_CAST_DELAY) * stats.cast_time),
                    )
                    return evs
                case "POST_CAST":
                    # Wait for cast-time based delay
                    if s.t < self.attack_state["until"]:
                        return evs

                    if sg_ahri_mana := s.buffs.get(StarGuardianQuirks.BUFF_KEY_AHRI):
                        stats.mana += sg_ahri_mana

                    # Start auto
                    self.attack_state = self._calc_pre_auto_state(s, stats)

                    s.mana_locks -= 1
                case _:
                    raise Exception()

            return evs
        finally:
            # if stats.mana != self.mana:
            #     print("wtf", s.t, self.mana, stats.mana)

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

    def _calc_pre_auto_state(self, s: SimState, stats: SimStats):
        delay = self.PRE_AUTO_DELAY * (1 / stats.effective_speed)
        return dict(
            type="PRE_AUTO",
            until=s.t + delay,
        )

    def _calc_post_auto_state(self, s: SimState, stats: SimStats):
        delay = (1 - self.PRE_AUTO_DELAY) * (1 / stats.effective_speed) / 2
        return dict(
            type="POST_AUTO",
            until=s.t + delay,
        )
