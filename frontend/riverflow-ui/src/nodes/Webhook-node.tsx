import { Position, Handle, type NodeProps , type Node} from "@xyflow/react";
import { Settings } from 'lucide-react';

//! Types
export type HookNodeData = {
  onOpen: (id: string) => void;
  url: string;
};

//! Hook Node

export function HookNode({ id, data }: NodeProps<Node<HookNodeData>['data']>) {
  return (
    <div>
      <button
        onClick={() => data.onOpen(id)}
        className="nodrag flex h-8 w-8 items-center justify-center rounded-full border border-border bg-card text-foreground transition hover:bg-muted"
      >
        <Settings size={14} />
      </button>
      <div className="relative flex h-20 w-20 items-center justify-center rounded-full border-2 border-green-500 bg-card shadow-md">
        <span className="text-sm font-semibold text-green-600 dark:text-green-300">
          Webhook
        </span>

        <Handle
          type="source"
          position={Position.Right}
          className="!h-3 !w-3 !bg-green-500"
        />

      </div>
    </div>
  );
}
