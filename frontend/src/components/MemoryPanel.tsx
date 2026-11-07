import React from 'react';
import { Memory } from '../types';

export const MemoryPanel: React.FC<{
  memories: Memory[];
  onDelete: (id: string) => void;
}> = ({ memories, onDelete }) => {
  return (
    <div className="flex flex-col gap-2.5 max-h-[460px] overflow-y-auto">
      {memories.map((m) => (
        <div
          key={m.id}
          className="bg-[#060e1c]/60 border border-[#00f0ff]/15 border-l-4 border-l-[#0077fe] p-3 rounded-md flex justify-between items-center"
        >
          <div>
            <div className="text-sm">{m.content}</div>
            <div className="text-xs text-[#829ab1] mt-1">
              Category: [{(m.category || 'general').toUpperCase()}] • Importance: {m.importance}
            </div>
          </div>
          <button
            onClick={() => onDelete(m.id)}
            className="text-xs px-2.5 py-1 rounded border border-red-500/40 text-red-400 hover:bg-red-500/10"
          >
            ✕
          </button>
        </div>
      ))}
    </div>
  );
};
