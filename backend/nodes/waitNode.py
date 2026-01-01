from time import sleep
from . import BaseNode

class WaitNode(BaseNode.BaseNode):
    def __init__(self, id, type, position, config):
        super().__init__(id, type, position)
        self.config = config

    def execute_node(self, context):
        if not self.config.get("delay").isalnum():
            return False
        sleep(int(self.config.get("delay")))
        return True