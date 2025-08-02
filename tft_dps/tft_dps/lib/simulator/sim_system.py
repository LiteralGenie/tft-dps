from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tft_dps.lib.simulator.sim_event import SimEvent
    from tft_dps.lib.simulator.sim_state import SimState, SimStats


class SimSystem(ABC):
    def hook_init(self, s: "SimState"):
        """Runs after initializing SimState, before first tick"""
        pass

    def hook_stats(self, s: "SimState") -> "SimStats | None":
        """Runs during stat calculation (before each system's hook_tick())

        Stats are reset to base values each tick (kinda)
        Each hook_stats() should return stats to be added to these base values
        """
        pass

    def hook_stats_override(self, s: "SimState", stats: "SimStats"):
        """Runs after hook_stats() for all systems have run"""
        pass

    def hook_main(self, s: "SimState", stats: "SimStats") -> list | None:
        """Runs each tick"""
        pass

    def hook_events(
        self, s: "SimState", evs: list["SimEvent"], stats: "SimStats"
    ) -> list | None:
        """Runs once per tick, after all systems have run"""
        pass
