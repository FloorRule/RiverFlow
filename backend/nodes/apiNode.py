import json
import re
import requests
from .BaseNode import BaseNode

class ApiNode(BaseNode):
    def __init__(self, id, type, position, config):
        super().__init__(id, type, position)
        self.config = config

    def render_body_template(self, template: str, data: dict) -> str:
        def replacer(match):
            key = match.group(1)
            return str(data.get(key, ""))

        return re.sub(r"\{\{(\w+)\}\}", replacer, template)

    def execute_node(self, context):
        method = self.config["method"]
        url = self.config["url"]
        body_template = self.config.get("body", "")

        try:
            rendered_body = None
            headers = {}

            if body_template:
                rendered = self.render_body_template(body_template, context["input"])
                rendered_body = json.loads(rendered)
                headers["Content-Type"] = "application/json"

            response = requests.request(
                method=method,
                url=url,
                json=rendered_body,
                headers=headers,
                timeout=10
            )

            response.raise_for_status()

            context["input"][self.id] = {
                "status": response.status_code,
                "body": response.json() if response.content else None
            }

            return True

        except Exception as e:
            context["logs"].append({
                "node": self.id,
                "error": str(e)
            })
            return False

