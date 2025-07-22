from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lib.simulator.sim_state import SimState


class SimSystem(ABC):
    @abstractmethod
    def run(self, s: "SimState"): ...

    def run_events(self, s: "SimState"):
        pass
