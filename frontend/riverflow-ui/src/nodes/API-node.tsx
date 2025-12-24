import { Position, Handle, type NodeProps , type Node} from "@xyflow/react";
import { Settings } from 'lucide-react';

//! Types

export type ApiNodeData = {
  onOpen: (id: string) => void;
  method: 'GET' | 'POST' | 'PUT' | 'DELETE';
  url: string;
  body: string;
};


//! API Node

export function APINode({ id, data }: NodeProps<Node<ApiNodeData>['data']>) {
  return (
    <div>
      <button
        onClick={() => data.onOpen(id)}
        className="nodrag flex h-8 w-8 items-center justify-center rounded-full border border-border bg-card text-foreground transition hover:bg-muted"
      >
        <Settings size={14} />
      </button>

      <div className="relative flex h-20 w-20 items-center justify-center rounded-full border-2 border-blue-500 bg-card shadow-md">
        <span className="text-sm font-semibold text-blue-600 dark:text-blue-300">
          API
        </span>

        <Handle
          type="target"
          position={Position.Left}
          className="!h-3 !w-3 !bg-blue-500"
        />

        <Handle
          type="source"
          position={Position.Right}
          className="!h-3 !w-3 !bg-blue-500"
        />
      </div>
    </div>
  );
}
