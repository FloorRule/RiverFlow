from . import BaseNode
from simpleeval import simple_eval

class ConditionNode(BaseNode.BaseNode):
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
        expr = self.config.get("expression")
        return simple_eval(expr, names=context, functions={"len": len})