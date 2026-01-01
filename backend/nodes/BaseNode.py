from dataclasses import dataclass, field

@dataclass(eq=True, frozen=True)
class BaseNode:
    id: str
    type: str
    position: object = field(compare=False, hash=False)

    def execute_node(self, context):
        raise NotImplementedError