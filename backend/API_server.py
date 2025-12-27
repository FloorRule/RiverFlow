import json
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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

@app.post("/api/flow")
async def flowAnalysis(flow: FlowEntry):
    if(TEST_MODE): print("Received log:", flow)

    for node in flow.nodes:
        print(node.type)

    return {"result": flow}