from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SimEvent:
    type: str
    data: Any
