import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Task } from '../types';
import { TaskCard } from '../components/TaskCard';

export const Tasks: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [title, setTitle] = useState('');
  const [priority, setPriority] = useState(3);
  const [desc, setDesc] = useState('');

  const loadTasks = async () => {
    try {
      const data = await api.getTasks('priority');
      setTasks(data);
    } catch (e) {}
  };

  useEffect(() => {
    loadTasks();
  }, []);

  const handleCreate = async () => {
    if (!title) return;
    await api.createTask({ title, priority, description: desc });
    setTitle('');
    setDesc('');
    loadTasks();
  };

  const handleToggle = async (id: string, status: string) => {
    await api.updateTask(id, { status: status as any });
    loadTasks();
  };

  const handleDelete = async (id: string) => {
    await api.deleteTask(id);
    loadTasks();
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-5 h-full">
      <div className="lg:col-span-2 bg-[#0c172d]/75 border border-[#00f0ff]/25 rounded-lg p-5 flex flex-col gap-3 backdrop-blur-md">
        <h3 className="hud-font text-sm text-[#00f0ff] tracking-wider border-b border-[#00f0ff]/15 pb-2.5">
          TASK PRIORITY QUEUE
        </h3>
        <div className="flex-1 overflow-y-auto flex flex-col gap-2.5">
          {tasks.map((t) => (
            <TaskCard key={t.id} task={t} onToggleStatus={handleToggle} onDelete={handleDelete} />
          ))}
        </div>
      </div>

      <div className="bg-[#0c172d]/75 border border-[#00f0ff]/25 rounded-lg p-5 flex flex-col gap-3 backdrop-blur-md">
        <h3 className="hud-font text-sm text-[#00f0ff] tracking-wider border-b border-[#00f0ff]/15 pb-2.5">
          DISPATCH NEW TASK
        </h3>
        <div>
          <label className="text-xs text-[#00f0ff] hud-font block mb-1">Task Title</label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full bg-[#00f0ff]/5 border border-[#00f0ff]/20 rounded p-2 text-sm text-white"
            placeholder="e.g. Implement ROS 2 Node"
          />
        </div>
        <div>
          <label className="text-xs text-[#00f0ff] hud-font block mb-1">Priority</label>
          <select
            value={priority}
            onChange={(e) => setPriority(parseInt(e.target.value))}
            className="w-full bg-[#00f0ff]/5 border border-[#00f0ff]/20 rounded p-2 text-sm text-white"
          >
            <option value="1">Priority 1 - Urgent</option>
            <option value="2">Priority 2 - High</option>
            <option value="3">Priority 3 - Medium</option>
            <option value="4">Priority 4 - Low</option>
          </select>
        </div>
        <div>
          <label className="text-xs text-[#00f0ff] hud-font block mb-1">Description</label>
          <textarea
            value={desc}
            onChange={(e) => setDesc(e.target.value)}
            rows={3}
            className="w-full bg-[#00f0ff]/5 border border-[#00f0ff]/20 rounded p-2 text-sm text-white"
          />
        </div>
        <button
          onClick={handleCreate}
          className="bg-[#00f0ff] text-black font-extrabold p-2.5 rounded hud-font text-xs hover:shadow-[0_0_16px_#00f0ff]"
        >
          ENQUEUE TASK
        </button>
      </div>
    </div>
  );
};
