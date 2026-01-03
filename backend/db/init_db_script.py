import json
import sqlite3
from typing import Optional

from pydantic import BaseModel

DB_PATH = "ocean.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS workflow (
    id TEXT PRIMARY KEY,
    name TEXT,
    edges TEXT
);

CREATE TABLE IF NOT EXISTS nodes (
    id TEXT PRIMARY KEY,
    workflow_id TEXT NOT NULL,
    type TEXT NOT NULL,
    position_x REAL NOT NULL,
    position_y REAL NOT NULL,
    FOREIGN KEY(workflow_id) REFERENCES workflow(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS api_node (
    id TEXT PRIMARY KEY,
    method TEXT NOT NULL,
    url TEXT NOT NULL,
    body TEXT,
    FOREIGN KEY(id) REFERENCES nodes(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS script_node (
    id TEXT PRIMARY KEY,
    python_script TEXT,
    FOREIGN KEY(id) REFERENCES nodes(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS wait_node (
    id TEXT PRIMARY KEY,
    delay TEXT NOT NULL,
    FOREIGN KEY(id) REFERENCES nodes(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS webhook_node (
    id TEXT PRIMARY KEY,
    url TEXT NOT NULL,
    FOREIGN KEY(id) REFERENCES nodes(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS condition_node (
    id TEXT PRIMARY KEY,
    expression TEXT NOT NULL,
    FOREIGN KEY(id) REFERENCES nodes(id) ON DELETE CASCADE
);
"""

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)
    conn.close()
    
def get_connection():
    return sqlite3.connect(DB_PATH)

class Position(BaseModel):
    x: float
    y: float

class Node(BaseModel):
    id: str
    type: str
    position: Position
    data: dict

class Edge(BaseModel):
    id: str
    source: str
    target: str
    sourceHandle: Optional[str]
    targetHandle: Optional[str]

class FlowEntry(BaseModel):
    nodes: list[Node]
    edges: list[Edge]

def save_flow_to_db(workflow_id: str, nodes: list[Node], edges: list[Edge]):
    """Parses the Pydantic models and saves them to SQLite."""
    edges_json = json.dumps([edge.dict() for edge in edges])

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        cursor.execute("INSERT OR REPLACE INTO workflow (id, edges) VALUES (?, ?)", (workflow_id, edges_json))

        cursor.execute("DELETE FROM nodes WHERE workflow_id = ?", (workflow_id,))

        for node in nodes:
            cursor.execute(
                "INSERT INTO nodes (id, workflow_id, type, position_x, position_y) VALUES (?, ?, ?, ?, ?)",
                (node.id, workflow_id, node.type, node.position.x, node.position.y)
            )

            if node.type == "apiNode":
                cursor.execute(
                    "INSERT INTO api_node (id, method, url, body) VALUES (?, ?, ?, ?)",
                    (node.id, node.data.get('method', 'GET'), node.data.get('url', ''), node.data.get('body', ''))
                )
            elif node.type == "scriptNode":
                cursor.execute(
                    "INSERT INTO script_node (id, python_script) VALUES (?, ?)",
                    (node.id, node.data.get('pythonScript', ''))
                )
            elif node.type == "waitNode":
                cursor.execute(
                    "INSERT INTO wait_node (id, delay) VALUES (?, ?)",
                    (node.id, node.data.get('delay', '0'))
                )
            elif node.type == "webhookNode" or node.type == "hookNode":
                cursor.execute(
                    "INSERT INTO webhook_node (id, url) VALUES (?, ?)",
                    (node.id, node.data.get('url', ''))
                )
            elif node.type == "conditionNode":
                cursor.execute(
                    "INSERT INTO condition_node (id, expression) VALUES (?, ?)",
                    (node.id, node.data.get('expression', ''))
                )
        conn.commit()

def load_flow_from_db(workflow_id: str):
    """Reconstructs nodes and edges from SQLite."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        row = cursor.execute("SELECT * FROM workflow WHERE id = ?", (workflow_id,)).fetchone()
        if not row:
            return None, None
        
        edges_data = json.loads(row['edges'])
        edges = [Edge(**e) for e in edges_data]

        node_rows = cursor.execute("SELECT * FROM nodes WHERE workflow_id = ?", (workflow_id,)).fetchall()
        
        nodes = []
        for n_row in node_rows:
            node_id = n_row['id']
            node_type = n_row['type']
            position = Position(x=n_row['position_x'], y=n_row['position_y'])
            data = {}

            if node_type == "apiNode":
                detail = cursor.execute("SELECT * FROM api_node WHERE id=?", (node_id,)).fetchone()
                if detail: data = {"method": detail['method'], "url": detail['url'], "body": detail['body']}
            
            elif node_type == "scriptNode":
                detail = cursor.execute("SELECT * FROM script_node WHERE id=?", (node_id,)).fetchone()
                if detail: data = {"pythonScript": detail['python_script']} 

            elif node_type == "waitNode":
                detail = cursor.execute("SELECT * FROM wait_node WHERE id=?", (node_id,)).fetchone()
                if detail: data = {"delay": detail['delay']}

            elif node_type in ["webhookNode", "hookNode"]:
                detail = cursor.execute("SELECT * FROM webhook_node WHERE id=?", (node_id,)).fetchone()
                if detail: data = {"url": detail['url']}

            elif node_type == "conditionNode":
                detail = cursor.execute("SELECT * FROM condition_node WHERE id=?", (node_id,)).fetchone()
                if detail: data = {"expression": detail['expression']}

            nodes.append(Node(id=node_id, type=node_type, position=position, data=data))
            
        return nodes, edges