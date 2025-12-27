from backend.nodes import BaseNode

class conditionNode(BaseNode):
  def __init__(self, id, type, position, config):
    super().__init__(id, type, position)
    self.config = config

  def execute_node(self, context):
    print(self.config)