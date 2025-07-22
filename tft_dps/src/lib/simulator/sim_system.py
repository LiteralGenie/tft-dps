from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lib.simulator.sim_state import SimState


class SimSystem(ABC):
    def run(self, s: "SimState"):
        pass

    def run_events(self, s: "SimState"):
        pass
