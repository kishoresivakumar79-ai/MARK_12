import React from 'react';
import { AgentStatus as AgentType } from '../types';

export const AgentStatus: React.FC<{ agent: AgentType }> = ({ agent }) => {
  return (
    <div className="bg-[#00f0ff]/5 border border-[#00f0ff]/20 p-3 rounded-md flex justify-between items-center">
      <div>
        <div className="font-bold text-sm text-[#00f0ff]">{agent.name} Agent</div>
        <div className="text-xs text-[#829ab1] mt-0.5">{agent.role}</div>
      </div>
      <span className="text-[10px] bg-[#00ff88]/20 text-[#00ff88] px-2 py-0.5 rounded font-mono">
        ONLINE
      </span>
    </div>
  );
};
