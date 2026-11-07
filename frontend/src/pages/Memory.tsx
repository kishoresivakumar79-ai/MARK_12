import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Memory as MemoryType } from '../types';
import { MemoryPanel } from '../components/MemoryPanel';

export const Memory: React.FC = () => {
  const [memories, setMemories] = useState<MemoryType[]>([]);
  const [query, setQuery] = useState('');
  const [newContent, setNewContent] = useState('');
  const [category, setCategory] = useState('user_preference');

  const loadMemories = async (q = '') => {
    try {
      const data = await api.getMemories(q);
      setMemories(data);
    } catch (e) {}
  };

  useEffect(() => {
    loadMemories();
  }, []);

  const handleSave = async () => {
    if (!newContent) return;
    await api.saveMemory({ category, content: newContent, importance: 4 });
    setNewContent('');
    loadMemories();
  };

  const handleDelete = async (id: string) => {
    await api.deleteMemory(id);
    loadMemories();
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-5 h-full">
      <div className="lg:col-span-2 bg-[#0c172d]/75 border border-[#00f0ff]/25 rounded-lg p-5 flex flex-col gap-3 backdrop-blur-md">
        <div className="flex justify-between items-center border-b border-[#00f0ff]/15 pb-2.5">
          <h3 className="hud-font text-sm text-[#00f0ff] tracking-wider">SEMANTIC MEMORY VAULT</h3>
          <input
            type="text"
            placeholder="Search vectors..."
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              loadMemories(e.target.value);
            }}
            className="bg-[#00f0ff]/5 border border-[#00f0ff]/20 rounded px-3 py-1 text-xs text-white"
          />
        </div>
        <MemoryPanel memories={memories} onDelete={handleDelete} />
      </div>

      <div className="bg-[#0c172d]/75 border border-[#00f0ff]/25 rounded-lg p-5 flex flex-col gap-3 backdrop-blur-md">
        <h3 className="hud-font text-sm text-[#00f0ff] tracking-wider border-b border-[#00f0ff]/15 pb-2.5">
          COMMIT NEW FACT
        </h3>
        <div>
          <label className="text-xs text-[#00f0ff] hud-font block mb-1">Category</label>
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="w-full bg-[#00f0ff]/5 border border-[#00f0ff]/20 rounded p-2 text-sm text-white"
          >
            <option value="user_preference">User Preference</option>
            <option value="project_fact">Project / Code Fact</option>
            <option value="life_schedule">Personal Schedule</option>
          </select>
        </div>
        <div>
          <label className="text-xs text-[#00f0ff] hud-font block mb-1">Memory Fact</label>
          <textarea
            value={newContent}
            onChange={(e) => setNewContent(e.target.value)}
            rows={4}
            className="w-full bg-[#00f0ff]/5 border border-[#00f0ff]/20 rounded p-2 text-sm text-white"
            placeholder="e.g. User prioritizes clean code with type annotations."
          />
        </div>
        <button
          onClick={handleSave}
          className="bg-[#00f0ff] text-black font-extrabold p-2.5 rounded hud-font text-xs hover:shadow-[0_0_16px_#00f0ff]"
        >
          SAVE MEMORY
        </button>
      </div>
    </div>
  );
};
