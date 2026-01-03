import json
import uuid
from typing import Optional
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.db.init_db_script import load_flow_from_db, save_flow_to_db

from .nodes import webhookNode,waitNode,scriptNode,conditionNode,apiNode

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
            river.add_node(apiNode.ApiNode(node.id, node.type, node.position, node.data))
        elif(node.type == "hookNode"):
            river.add_node(webhookNode.WebhookNode(node.id, node.type, node.position, node.data))
        elif(node.type == "conditionNode"):
            river.add_node(conditionNode.ConditionNode(node.id, node.type, node.position, node.data))
        elif(node.type == "scriptNode"):
            river.add_node(scriptNode.ScriptNode(node.id, node.type, node.position, node.data))
        elif(node.type == "waitNode"):
            river.add_node(waitNode.WaitNode(node.id, node.type, node.position, node.data))
    
    for edge in edges:
        river.add_edge(edge.source,edge.target, edge.sourceHandle)
    return river

WORKFLOWS = {}

@app.post("/api/flow")
async def flowAnalysis(flow: FlowEntry):
    if(TEST_MODE): print("Received log:", flow)

    river = buildFlow(flow.nodes, flow.edges)

    start_node = river.find_start_node()
    workflow_id = str(start_node.id) if start_node else str(uuid.uuid4())
    
    save_flow_to_db(workflow_id, flow.nodes, flow.edges)
    WORKFLOWS[workflow_id] = river

    webhook_url = f"/hooks/{workflow_id}"

    return {
        "workflow_id": workflow_id,
        "webhook_url": webhook_url
    }

@app.get("/api/flow/{workflow_id}")
async def get_flow(workflow_id: str):
    river = WORKFLOWS.get(workflow_id)
    
    if not river:
        nodes, edges = load_flow_from_db(workflow_id)
        if not nodes:
             raise HTTPException(status_code=404, detail="Workflow not found")
        
        return {"nodes": [n.dict() for n in nodes], "edges": [e.dict() for e in edges]}
    
    nodes, edges = load_flow_from_db(workflow_id)
    return {
        "nodes": [n.dict() for n in nodes],
        "edges": [e.dict() for e in edges]
    }

@app.post("/hooks/{workflow_id}")
async def webhook_handler(workflow_id: str, request: Request):
    river = WORKFLOWS.get(workflow_id)
    if not river:
        print(f"Workflow {workflow_id} not in memory, loading from DB...")
        nodes, edges = load_flow_from_db(workflow_id)
        
        if nodes and edges:
            river = buildFlow(nodes, edges)
            WORKFLOWS[workflow_id] = river
        else:
            raise HTTPException(status_code=404, detail="Workflow not found")

    payload = await request.json()

    context = {
        "input": payload,
        "logs": []
    }

    webhook_node = river.find_webhook_node()

    river.execute_from_trigger(webhook_node, context)

    return {
        "status": "executed",
        "context": context
    }