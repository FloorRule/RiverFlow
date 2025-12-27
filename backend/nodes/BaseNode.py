class BaseNode():
    def __init__(self, id, type, position):
        self.id = id
        self.type = type
        self.positio = position
    
    def execute_node(self, context):
        raise NotImplementedError