class WorkFlow:
    def __init__(self):
        self.graph: dict[BaseNode, list[BaseNode]] = {}
        self.node_map: dict[str, BaseNode] = {}
        self.incoming_count: dict[BaseNode, int] = {}

    def add_node(self, node: BaseNode):
        self.node_map[node.id] = node
        self.graph.setdefault(node, [])
        self.incoming_count.setdefault(node, 0)

    def add_edge(self, source_id: str, target_id: str, source_handle: str | None = None):
        u = self.node_map[source_id]
        v = self.node_map[target_id]

        # condition routing
        if u.type == "conditionNode" and source_handle:
            if source_handle == "a":
                u.set_condition_true(v)
            elif source_handle == "b":
                u.set_condition_false(v)
            return

        self.graph[u].append(v)
        self.incoming_count[v] += 1

    def find_start_node(self):
        for node, count in self.incoming_count.items():
            if count == 0:
                return node
        raise RuntimeError("No start node found")
    
    def find_webhook_node(self):
        for node in self.node_map.values():
            if node.type == "webhookNode":
                return node
        raise RuntimeError("Webhook node not found")

    def execute(self, context: dict):
        start = self.find_start_node()
        visited = set()
        self._dfs_execute(start, context, visited)

    def execute_from_trigger(self, trigger_node, context):
        visited = set()
        for neighbor in self.graph.get(trigger_node, []):
            self._dfs_execute(neighbor, context, visited)

    def _dfs_execute(self, node, context, visited):
        if node in visited:
            return

        visited.add(node)

        result = node.execute_node(context)

        # condition node routing
        if node.type == "conditionNode":
            next_node = node.trueNode if result else node.falseNode
            if next_node:
                self._dfs_execute(next_node, context, visited)
            return

        for neighbor in self.graph.get(node, []):
            self._dfs_execute(neighbor, context, visited)


