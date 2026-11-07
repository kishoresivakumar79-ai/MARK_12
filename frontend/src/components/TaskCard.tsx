import React from 'react';
import { Task } from '../types';

export const TaskCard: React.FC<{
  task: Task;
  onToggleStatus: (id: string, status: string) => void;
  onDelete: (id: string) => void;
}> = ({ task, onToggleStatus, onDelete }) => {
  const priorityColor =
    task.priority === 1
      ? 'border-l-[#ff0055]'
      : task.priority === 2
      ? 'border-l-[#ffb703]'
      : 'border-l-[#00f0ff]';

  return (
    <div
      className={`bg-[#060e1c]/60 border border-[#00f0ff]/15 border-l-4 ${priorityColor} p-3 rounded-md flex justify-between items-center`}
    >
      <div>
        <div className="font-semibold text-sm">{task.title}</div>
        <div className="text-xs text-[#829ab1] mt-1">
          Priority {task.priority} • Status: {task.status}
        </div>
      </div>
      <div className="flex gap-2">
        <button
          onClick={() =>
            onToggleStatus(task.id, task.status === 'completed' ? 'pending' : 'completed')
          }
          className="text-xs px-2.5 py-1 rounded border border-[#00f0ff]/30 text-[#00f0ff] hover:bg-[#00f0ff]/10"
        >
          {task.status === 'completed' ? 'REOPEN' : 'DONE'}
        </button>
        <button
          onClick={() => onDelete(task.id)}
          className="text-xs px-2.5 py-1 rounded border border-red-500/40 text-red-400 hover:bg-red-500/10"
        >
          ✕
        </button>
      </div>
    </div>
  );
};
