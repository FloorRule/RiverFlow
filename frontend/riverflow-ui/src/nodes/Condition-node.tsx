import { Position, Handle, type NodeProps , type Node} from "@xyflow/react";
import { Settings } from 'lucide-react';

//! Types
export type ConditionNodeData = {
  onOpen: (id: string) => void;
  expression: string;
};

//! Condition Node

export function ConditionNode({ id, data }: NodeProps<Node<ConditionNodeData>['data']>) {
  return (
    <div>
      <button
        onClick={() => data.onOpen(id)}
        className="nodrag flex h-8 w-8 items-center justify-center rounded-full border border-border bg-card text-foreground transition hover:bg-muted"
      >
        <Settings size={14} />
      </button>
      <div className="relative flex h-20 w-20 items-center justify-center rounded-full border-2 border-red-500 bg-card shadow-md">
        <span className="text-sm font-semibold text-red-600 dark:text-red-300">
          Condition
        </span>

        <Handle
          type="target"
          position={Position.Left}
          className="!h-3 !w-3 !bg-red-500"
        />

        <Handle
          type="source"
          position={Position.Top} id="a"
          className="!h-3 !w-3 !bg-red-500"
        />

        <Handle
          type="source"
          position={Position.Bottom} id="b"
          className="!h-3 !w-3 !bg-red-500"
        />
      </div>
    </div>
  );
}
