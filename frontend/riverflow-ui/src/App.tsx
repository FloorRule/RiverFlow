import { applyEdgeChanges, applyNodeChanges,Background, Controls, ReactFlow , type Node, type Edge, addEdge, Panel } from "@xyflow/react";
 
import "@xyflow/react/dist/style.css";

import { useCallback, useMemo, useState } from 'react';
import { APINode, type ApiNodeData } from "./nodes/API-node";
import { ConditionNode, type ConditionNodeData } from "./nodes/Condition-node";
 

//! API - Inspector 

function APINodeInspector({
  node,
  onClose,
  onUpdate,
}: {
  node: Node<ApiNodeData>;
  onClose: () => void;
  onUpdate: (patch: Partial<ApiNodeData>) => void;
}) {
  return (
    <div className="space-y-4 bg-card text-blue-400 transition">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold">HTTP Request : {node.id}</h2>
        <button
          onClick={onClose}
          className="h-5 w-5 text-sm text-muted-foreground hover:text-foreground"
        >
          ✕
        </button>
      </div>

      <div>
        <label className="block text-sm font-medium">Method</label>
        <select
          className="mt-1 w-full rounded border border-border bg-background px-2 py-1"
          value={node.data.method}
          onChange={(e) =>
            onUpdate({ method: e.target.value as ApiNodeData['method'] })
          }
        >
          <option>GET</option>
          <option>POST</option>
          <option>PUT</option>
          <option>DELETE</option>
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium">URL</label>
        <input
          className="mt-1 w-full rounded border border-border bg-background px-2 py-1"
          placeholder="https://api.example.com"
          value={node.data.url}
          onChange={(e) => onUpdate({ url: e.target.value })}
        />
      </div>

      <div>
        <label className="block text-sm font-medium">Body</label>
        <textarea
          rows={5}
          className="mt-1 w-full rounded border border-border bg-background px-2 py-1 font-mono text-sm"
          placeholder='{ "foo": "bar" }'
          value={node.data.body}
          onChange={(e) => onUpdate({ body: e.target.value })}
        />
      </div>
    </div>
  );
}

//! Condition - Inspector 

function ConditionNodeInspector({
  node,
  onClose,
  onUpdate,
}: {
  node: Node<ConditionNodeData>;
  onClose: () => void;
  onUpdate: (patch: Partial<ConditionNodeData>) => void;
}) {
  return (
    <div className="space-y-4 bg-card text-red-400 transition">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold">Condition : {node.id}</h2>
        <button
          onClick={onClose}
          className="h-5 w-5 text-sm text-muted-foreground hover:text-foreground"
        >
          ✕
        </button>
      </div>

      <div>
        <label className="block text-sm font-medium">Expression</label>
        <textarea
          rows={4}
          className="mt-1 w-full rounded border border-border bg-background px-2 py-1 font-mono text-sm"
          placeholder='x >= 5'
          value={node.data.expression}
          onChange={(e) => onUpdate({ expression: e.target.value })}
        />
      </div>
    </div>
  );
}

//! Node Button

const colors: string[] = [
  'mb-2 flex w-full items-center justify-center rounded-md border border-blue-500 bg-blue-50 px-3 py-2 text-sm font-semibold text-blue-600 transition hover:bg-blue-100 dark:border-blue-400 dark:bg-blue-900/30 dark:text-blue-300 dark:hover:bg-blue-900/50',
  'mb-2 flex w-full items-center justify-center rounded-md border border-red-500 bg-red-50 px-3 py-2 text-sm font-semibold text-red-600 transition hover:bg-red-100 dark:border-red-400 dark:bg-red-900/30 dark:text-red-300 dark:hover:bg-red-900/50',
  'mb-2 flex w-full items-center justify-center rounded-md border border-green-500 bg-green-50 px-3 py-2 text-sm font-semibold text-green-600 transition hover:bg-green-100 dark:border-green-400 dark:bg-green-900/30 dark:text-green-300 dark:hover:bg-green-900/50',
  'mb-2 flex w-full items-center justify-center rounded-md border border-yellow-500 bg-yellow-50 px-3 py-2 text-sm font-semibold text-yellow-600 transition hover:bg-yellow-100 dark:border-yellow-400 dark:bg-yellow-900/30 dark:text-yellow-300 dark:hover:bg-yellow-900/50',
  'mb-2 flex w-full items-center justify-center rounded-md border border-pink-500 bg-pink-50 px-3 py-2 text-sm font-semibold text-pink-600 transition hover:bg-pink-100 dark:border-pink-400 dark:bg-pink-900/30 dark:text-pink-300 dark:hover:bg-pink-900/50',
];

function NodeButton({
  label,
  onClick,
  colorIndex,
}: {
  label: string;
  onClick: () => void;
  colorIndex: number;
}) {
  return (
    <button onClick={onClick} className={colors[colorIndex]}>
      {label}
    </button>
  );
}

type NodeInspectorProps = {
  node: Node<NodeData>;
  onClose: () => void;
  onUpdate: (patch: Partial<NodeData>) => void;
};

const inspectorMap = {
  apiNode: APINodeInspector,
  conditionNode: ConditionNodeInspector,
} as const;

export function NodeInspector({ node, onClose, onUpdate }: NodeInspectorProps) {
  switch (node.type) {
    case 'apiNode':
      return (
        <APINodeInspector
          node={node as Node<ApiNodeData>}
          onClose={onClose}
          onUpdate={onUpdate as (p: Partial<ApiNodeData>) => void}
        />
      );

    case 'conditionNode':
      return (
        <ConditionNodeInspector
          node={node as Node<ConditionNodeData>}
          onClose={onClose}
          onUpdate={onUpdate as (p: Partial<ConditionNodeData>) => void}
        />
      );

    default:
      return null;
  }
}

export type NodeData = ApiNodeData | ConditionNodeData;
const nodeTypes = {
  apiNode: APINode,
  conditionNode: ConditionNode,
};


const initialNodes: Node<NodeData>[] = [];
const initialEdges: Edge[] = [];

//! Flow

function Flow() {
  const [activeNodeId, setActiveNodeId] = useState<string | null>(null);
  const [nodes, setNodes] = useState<Node<NodeData>[]>(initialNodes);
  const [edges, setEdges] = useState<Edge[]>(initialEdges);

  const activeNode = useMemo(
    () => nodes.find((n) => n.id === activeNodeId) ?? null,
    [nodes, activeNodeId]
  );

  const handleNodesChange = useCallback(
    (changes) =>
      setNodes((nodesSnapshot) =>
        applyNodeChanges(changes, nodesSnapshot)
      ),
    []
  );

  const handleEdgesChange = useCallback(
    (changes) =>
      setEdges((edgesSnapshot) =>
        applyEdgeChanges(changes, edgesSnapshot)
      ),
    []
  );

  const onConnect = useCallback((params) => {
    setEdges((edges) => {

      const sourceNode = nodes.find((n) => n.id === params.source);

      if (sourceNode) 
      {
          if (sourceNode.type === 'conditionNode') {
          const handleUsed = edges.some(
            (e) =>
              e.source === params.source &&
              e.sourceHandle === params.sourceHandle
          );

          if (handleUsed) 
            return edges;

          return addEdge(params, edges);
        }
      }


      const hasConnection = edges.some(
        (e) => e.source === params.source || e.target === params.target
      );

      if (hasConnection) return edges;

      return addEdge(params, edges);
    });
  }, []);

  const updateActiveNodeData = useCallback(
    (patch: Partial<NodeData>) => {
      if (!activeNodeId) return;

      setNodes((nds) =>
        nds.map((n) =>
          n.id === activeNodeId
            ? { ...n, data: { ...n.data, ...patch } }
            : n
        )
      );
    },
    [activeNodeId]
  );


  const addAPINode = useCallback(() => {
    const id = crypto.randomUUID();

    setNodes((nds) => [
      ...nds,
      {
        id,
        type: 'apiNode',
        position: { x: 100, y: 100 },
        data: {
          onOpen: (nodeId: string) => setActiveNodeId(nodeId),
          method: 'GET',
          url: '',
          body: '',
        },
      },
    ]);
  }, []);

  const addConditionNode = useCallback(() => {
    const id = crypto.randomUUID();

    setNodes((nds) => [
      ...nds,
      {
        id,
        type: 'conditionNode',
        position: { x: 100, y: 100 },
        data: {
          onOpen: (nodeId: string) => setActiveNodeId(nodeId),
          expression: '',
        },
      },
    ]);
  }, []);

  return (
    <div style={{ height: '100vh', width: '100vw' }}>
      <ReactFlow
        className="bg-background text-foreground"
        nodes={nodes}
        edges={edges}
        onNodesChange={handleNodesChange}
        onEdgesChange={handleEdgesChange}
        onConnect={onConnect}
        nodeTypes={nodeTypes}
        fitView
      >
        <Panel position="center-right">
          <div className="w-48 max-h-[70vh] overflow-y-auto rounded-lg border border-border bg-card p-2 shadow-md">
            <NodeButton label="API Node" onClick={addAPINode} colorIndex={0} />
            <NodeButton label="Condition Node" onClick={addConditionNode} colorIndex={1} />
            <NodeButton label="Webhook Node" onClick={addAPINode} colorIndex={2} />
            <NodeButton label="Python/JS Code Node" onClick={addAPINode} colorIndex={3} />
            <NodeButton label="Wait/Delay Node" onClick={addAPINode} colorIndex={4} />
          </div>
        </Panel>

        {activeNode && (
          <Panel position="center-left">
            <div className="w-80 max-h-[80vh] overflow-y-auto rounded-lg border border-border bg-card p-4 shadow-lg text-foreground">
              <NodeInspector
                node={activeNode}
                onClose={() => setActiveNodeId(null)}
                onUpdate={updateActiveNodeData}
              />
            </div>
          </Panel>
        )}

        <Background className="bg-background" />
        <Controls className="bg-card border-border text-foreground" />
      </ReactFlow>
    </div>
  );
}

export default function App() {
  return <Flow />;
}
