import React from 'react';
import { useAssistant } from '../context/AssistantContext';

const navItems = [
  { id: 'dashboard', label: 'COMMAND CENTER', icon: '⬡' },
  { id: 'chat', label: 'AI CONVERSATION', icon: '◈' },
  { id: 'agents', label: 'MULTI-AGENT GRAPH', icon: '❖' },
  { id: 'tasks', label: 'TASK PRIORITY', icon: '▤' },
  { id: 'memory', label: 'SEMANTIC MEMORY', icon: '◎' },
  { id: 'documents', label: 'DOCUMENT INTEL', icon: '📄' },
  { id: 'vision', label: 'COMPUTER VISION', icon: '👁' },
  { id: 'automation', label: 'AUTOMATION SUITE', icon: '⚙' },
  { id: 'settings', label: 'SETTINGS', icon: '🔧' }
];

export const Sidebar: React.FC = () => {
  const { activeTab, setActiveTab } = useAssistant();

  return (
    <aside className="w-60 bg-[#060c18]/90 border-r border-[#00f0ff]/20 flex flex-col p-4 gap-2">
      {navItems.map((item) => {
        const isActive = activeTab === item.id;
        return (
          <button
            key={item.id}
            onClick={() => setActiveTab(item.id)}
            className={`flex items-center gap-3 px-3 py-3 rounded-md text-xs font-bold tracking-wider transition-all hud-font text-left ${
              isActive
                ? 'bg-[#00f0ff]/15 text-[#00f0ff] border border-[#00f0ff] shadow-[0_0_12px_rgba(0,240,255,0.25)]'
                : 'text-[#829ab1] hover:text-white hover:bg-[#00f0ff]/5'
            }`}
          >
            <span className="text-base text-[#00f0ff]">{item.icon}</span>
            <span>{item.label}</span>
          </button>
        );
      })}
    </aside>
  );
};
