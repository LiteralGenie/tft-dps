from abc import ABC, abstractmethod

from lib.simulator.sim_state import SimState


class SimSystem(ABC):
    @abstractmethod
    def run(self, s: SimState): ...

    def run_events(self, s: SimState):
        pass
