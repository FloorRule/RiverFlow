import json
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .nodes import WebhookNode,WaitNode,ScriptNode,ConditionNode,ApiNode

from .workFlow import WorkFlow

TEST_MODE = True

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

def buildFlow(nodes: list[Node], edges: list[Edge]):
    river = WorkFlow()
    for node in nodes:
        if(node.type == "apiNode"):
            river.add_node(ApiNode(node.id, node.type, node.position, node.data))
        elif(node.type == "hookNode"):
            river.add_node(WebhookNode(node.id, node.type, node.position, node.data))
        elif(node.type == "conditionNode"):
            river.add_node(ConditionNode(node.id, node.type, node.position, node.data))
        elif(node.type == "scriptNode"):
            river.add_node(ScriptNode(node.id, node.type, node.position, node.data))
        elif(node.type == "waitNode"):
            river.add_node(WaitNode(node.id, node.type, node.position, node.data))
    
    for edge in edges:
        river.add_edge(edge.source,edge.target, edge.sourceHandle)
    return river

@app.post("/api/flow")
async def flowAnalysis(flow: FlowEntry):
    if(TEST_MODE): print("Received log:", flow)

    river = buildFlow(flow.nodes, flow.edges)
    context = {
        "input": {},
        "vars": {},
        "logs": []
    }

    river.execute(context)

    return {"result": flow}