from time import sleep
from backend.nodes import BaseNode

class WaitNode(BaseNode):
    def __init__(self, id, type, position, config):
        super().__init__(id, type, position)
        self.config = config

    def execute_node(self, context):
        if not self.config.get("delay").isalnum():
            return False
        sleep(int(self.config.get("delay")))
        return True