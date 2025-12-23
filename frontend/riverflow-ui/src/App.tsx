import { applyEdgeChanges, applyNodeChanges, Position, Handle,Background, Controls, ReactFlow, useEdgesState, useNodesState, type Node, type Edge, addEdge, Panel } from "@xyflow/react";
 
import "@xyflow/react/dist/style.css";

import { useCallback, useState } from 'react';
import { Settings } from 'lucide-react';
 
const colors: string[] = [
    "mb-2 flex w-full items-center justify-center rounded-md border border-blue-500 bg-blue-50 px-3 py-2 text-sm font-semibold text-blue-600 transition hover:bg-blue-100",
    "mb-2 flex w-full items-center justify-center rounded-md border border-red-500 bg-red-50 px-3 py-2 text-sm font-semibold text-red-600 transition hover:bg-red-100",
    "mb-2 flex w-full items-center justify-center rounded-md border border-green-500 bg-green-50 px-3 py-2 text-sm font-semibold text-green-600 transition hover:bg-green-100",
    "mb-2 flex w-full items-center justify-center rounded-md border border-yellow-500 bg-yellow-50 px-3 py-2 text-sm font-semibold text-yellow-600 transition hover:bg-yellow-100",
    "mb-2 flex w-full items-center justify-center rounded-md border border-pink-500 bg-pink-50 px-3 py-2 text-sm font-semibold text-pink-600 transition hover:bg-pink-100",
];

function NodeButton({ label, onClick, colorIndex }: {
  label: string;
  onClick: () => void;
  colorIndex: number;
}) {
  return (
    <button
      onClick={onClick}
      className={colors[colorIndex]}>
      {label}
    </button>
  );
}

export function APINode() {
  const test = () => {alert('Something magical just happened. ✨')};


  return (
    <div>
      <button onClick={test} className="p-3 w-8 h-8 flex items-center justify-center rounded-full border border-gray-500 bg-gray-50 px-1 py-1 text-sm font-semibold text-gray-600 transition hover:bg-gray-100">
        <Settings size={14} />
      </button>
    
      <div className="relative flex h-20 w-20 items-center justify-center rounded-full border-2 border-blue-500 bg-white shadow-md">
        <span className="text-sm font-semibold text-blue-600">API</span>

        <Handle
          type="target"
          position={Position.Left}
          className="!bg-blue-500 !w-3 !h-3"
        />

        <Handle
          type="source"
          position={Position.Right}
          className="!bg-blue-500 !w-3 !h-3"
        />
      </div>
    </div>
  );
}

const nodeTypes = {
  apiNode: APINode,
};

const initialNodes: Node[] = [
  {
    id: "1",
    position: { x: 0, y: 0 },
    data: { },
    type: 'apiNode'
  },
  {
    id: "2",
    position: { x: 10, y: 0 },
    data: { },
    type: 'apiNode'
  },
];
const initialEdges: Edge[] = [];

function Flow() {
  const [nodes, setNodes] = useState(initialNodes);
  const [edges, setEdges] = useState(initialEdges);

  const handleNodesChange = useCallback(
    (changes) => setNodes((nodesSnapshot) => applyNodeChanges(changes, nodesSnapshot)),
    [],
  );

  const handleEdgesChange = useCallback(
    (changes) => setEdges((edgesSnapshot) => applyEdgeChanges(changes, edgesSnapshot)),
    [],
  );

  const onConnect = useCallback(
    (params) => setEdges((edgesSnapshot) => addEdge(params, edgesSnapshot)),
    [],
  );

  const addAPINode = useCallback(() => {
    setNodes((nds) => [
      ...nds,
      {
        id: crypto.randomUUID(),
        type: 'apiNode',
        position: {
          x: 0,
          y: 0,
        },
        data: {},
      },
    ]);
  }, []);

  return (
    <div style={{ height: '100vh', width: '100vw' }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={handleNodesChange}
        onEdgesChange={handleEdgesChange}
        onConnect={onConnect}
        nodeTypes={nodeTypes}
        fitView
      >
        <Panel position="center-right">
          <div className="w-48 max-h-[70vh] overflow-y-auto rounded-lg border bg-white p-2 shadow-md">
            <NodeButton label="API Node" onClick={addAPINode} colorIndex={0} />
            <NodeButton label="API Node" onClick={addAPINode} colorIndex={1} />
            <NodeButton label="API Node" onClick={addAPINode} colorIndex={2} />
            <NodeButton label="API Node" onClick={addAPINode} colorIndex={3} />
            <NodeButton label="API Node" onClick={addAPINode} colorIndex={4} />
          </div>
        </Panel>
        <Background />
        <Controls />
      </ReactFlow>
    </div>
  );
}

export default function App() {
  return <Flow />;
}