from . import BaseNode

class ScriptNode(BaseNode.BaseNode):
    def __init__(self, id, type, position, config):
        super().__init__(id, type, position)
        self.config = config

    def execute_node(self, context):
        code = self.config["pythonScript"]

        env = {
            "input_data": context["input"],
            "logs": context["logs"],
            "result": None
        }

        SAFE_BUILTINS = {
            "len": len,
            "str": str,
            "int": int,
            "float": float,
            "bool": bool,
            "range": range,
            "enumerate": enumerate,
            "print": print,
        }

        try:
            exec(code, {"__builtins__": SAFE_BUILTINS}, env)
        except Exception as e:
            context["logs"].append({"node": self.id, "error": str(e)})
            return False

        if env.get("result") is not None:
            context["input"][self.id] = env["result"]

        return True

