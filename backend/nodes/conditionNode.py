from backend.nodes import BaseNode

class ConditionNode(BaseNode):
    def __init__(self, id, type, position, config):
        super().__init__(id, type, position)
        self.config = config
        self.trueNode = None
        self.falseNode = None

    def set_condition_true(self, true):
        self.trueNode = true

    def set_condition_false(self, false):
        self.falseNode = false

    def execute_node(self, context):
        key = self.config.get("variable")
        return bool(context.get(key))