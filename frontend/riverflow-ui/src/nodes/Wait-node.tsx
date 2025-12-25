import { Position, Handle, type NodeProps , type Node} from "@xyflow/react";
import { Settings } from 'lucide-react';

//! Types
export type WaitNodeData = {
  onOpen: (id: string) => void;
  delay: string;
};

//! Wait Node

export function WaitNode({ id, data }: NodeProps<Node<WaitNodeData>['data']>) {
  return (
    <div>
      <button
        onClick={() => data.onOpen(id)}
        className="nodrag flex h-8 w-8 items-center justify-center rounded-full border border-border bg-card text-foreground transition hover:bg-muted"
      >
        <Settings size={14} />
      </button>
      <div className="relative flex h-20 w-20 items-center justify-center rounded-full border-2 border-pink-500 bg-card shadow-md">
        <span className="text-sm font-semibold text-pink-600 dark:text-pink-300">
          Wait
        </span>

        <Handle
          type="target"
          position={Position.Left}
          className="!h-3 !w-3 !bg-pink-500"
        />

        <Handle
          type="source"
          position={Position.Right}
          className="!h-3 !w-3 !bg-pink-500"
        />

      </div>
    </div>
  );
}
