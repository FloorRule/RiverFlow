# RiverFlow

**Visual Workflow Orchestration Engine**

RiverFlow is a **Full-Stack Automation Platform** (similar to n8n or Zapier) designed to visually architect and execute complex logical pipelines. It allows users to drag-and-drop nodes to create logic flows, saves them to a structured database, and executes them in real-time via webhook triggers with live visual feedback.

https://github.com/user-attachments/assets/ee1d64fa-54e9-459b-b36e-520872e82d1d

---

## Overview

The system bridges the gap between visual design and backend execution. The architecture follows a strict separation between the designer and the execution engine:

*   **Designer:** A React Flow-based canvas for constructing Directed Acyclic Graphs (DAGs).
*   **Engine:** A Python-based graph traversal system that interprets JSON schemas and executes nodes.
*   **State:** Persistent storage of flow configurations via SQLite.
*   **Real-Time:** WebSocket integration to animate the active node on the canvas during execution.

---

## Features

### Implemented

*   **Visual Editor:** Drag-and-drop interface with custom nodes using React Flow.
*   **Node Library:**
    *   **Webhook:** Event-driven entry points for workflows.
    *   **API Request:** Dynamic HTTP client (GET/POST/PUT/DELETE) with templating.
    *   **Python Script:** Sandboxed code execution for custom logic.
    *   **Condition:** Logic branching (True/False paths) using `simpleeval`.
    *   **Wait:** Async execution delays.
*   **Live Execution:** WebSocket feedback loops that highlight nodes as they run.
*   **Serialization:** Complete save/load system mapping graph coordinates and data to a Relational DB.
*   **Persistent Storage:** SQLite integration with foreign key constraints.

### Roadmap

*   Containerization via Docker Compose.
*   Drag-and-drop connection cutting logic.
*   Detailed execution history logs.

---

## Backend (Python/FastAPI)

The backend acts as both an API gateway and a graph interpreter.

1.  **Workflow Engine:** A DFS (Depth-First Search) implementation that traverses the graph starting from the Webhook.
2.  **Sandbox:** A secure execution environment for the "Python Script" node, allowing safe evaluation of user code.
3.  **WebSocket Manager:** Broadcasts `NODE_ACTIVE` events to the frontend.

### Execution Logic
The engine routes execution dynamically based on node results (e.g., Condition Nodes).

```python
# Simplified Graph Traversal
async def _dfs_execute(self, node, context, visited, callback=None):
    result = node.execute_node(context)
    
    if callback:
        await callback(node.id) # Trigger Frontend Animation

    # Handle Branching
    if node.type == "conditionNode":
        next_node = node.trueNode if result else node.falseNode
        await self._dfs_execute(next_node, context, ...)
```
---
# Frontend (React + React Flow)

The designer (`App.tsx`) handles state complexity and real-time visualization.

---

## Key Technologies

- **UI Library:** React Flow + Tailwind CSS
- **Architecture:** Custom Node Components for specific logic configuration (Inspector Panels)
- **Live Feedback:** Listens to WebSocket events to inject CSS styles into running nodes

---

## Backend Execution Connection

The frontend connects to the backend execution loop using WebSockets.

```ts
const ws = new WebSocket(`ws://localhost:8000/ws/${currentWorkflowId}`);

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);

  if (data.type === 'NODE_ACTIVE') {
    executionQueue.current.push(data.node_id);
    processQueue();
  }
};
```
---

## Communication Protocol

- **REST:** Saving and loading workflows
- **Webhooks / WebSockets:** Workflow execution and live updates

---

## Workflow Definition (Frontend → API)

**Endpoint:** `POST /api/flow`

```json
{
  "nodes": [
    {
      "id": "1",
      "type": "apiNode",
      "data": { "url": "https://api.co" },
      "position": { "x": 100, "y": 100 }
    }
  ],
  "edges": [
    { "source": "1", "target": "2" }
  ]
}
```

---

## Execution Trigger (External → API)

**Endpoint:** `POST /hooks/{workflow_id}`

```json
{
  "email": "test@example.com",
  "data": "Anything passed here is accessible in the workflow context"
}
```

---

## How to Run

The system is currently designed for **local development only**.  
Docker support will be added in future updates.

---

## Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

```bash
python -m backend.main
```

Server address:

```text
http://0.0.0.0:8000
```

---

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

```text
http://localhost:5173
```

---

## Triggering a Workflow

1. Open the UI.
2. Drag a **Webhook Node** and connect it to other nodes.
3. Click **Save** and copy the **Workflow ID**.
4. Trigger the workflow using:

```bash
python test_flow.py
```

Nodes will light up **green** as execution progresses.
