from dataclasses import dataclass
from typing import Any

@dataclass(eq=True, frozen=True)
class BaseNode:
    id: str
    type: str
    position: Any

    def execute_node(self, context: dict):
        raise NotImplementedError
