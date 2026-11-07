import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { AgentStatus as AgentType } from '../types';
import { AgentStatus } from '../components/AgentStatus';

export const Agents: React.FC = () => {
  const [agents, setAgents] = useState<AgentType[]>([]);
  const [objective, setObjective] = useState('');
  const [log, setLog] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    api.getAgents().then((res) => setAgents(res.agents)).catch(() => {});
  }, []);

  const handleRunWorkflow = async () => {
    if (!objective || loading) return;
    setLoading(true);
    setLog(['Initiating Planner Agent DAG deconstruction...']);

    try {
      const res = await api.runWorkflow(objective);
      const steps = res.execution_log.map(
        (s: any) => `Step ${s.step} [${s.agent}]: ${s.output.substring(0, 150)}...`
      );
      setLog(steps);
    } catch (e: any) {
      setLog([`Error: ${e.message}`]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-5 h-full">
      <div className="lg:col-span-2 bg-[#0c172d]/75 border border-[#00f0ff]/25 rounded-lg p-5 flex flex-col gap-4 backdrop-blur-md">
        <h3 className="hud-font text-sm text-[#00f0ff] tracking-wider border-b border-[#00f0ff]/15 pb-2.5">
          MULTI-AGENT COLLABORATION DAG
        </h3>
        <div className="flex gap-2">
          <input
            type="text"
            value={objective}
            onChange={(e) => setObjective(e.target.value)}
            placeholder="Enter goal (e.g., 'Compare Python ML frameworks and generate study guide')"
            className="flex-1 bg-[#00f0ff]/5 border border-[#00f0ff]/20 rounded p-2 text-sm text-white"
          />
          <button
            onClick={handleRunWorkflow}
            disabled={loading}
            className="bg-[#00f0ff] text-black font-extrabold px-4 rounded hud-font text-xs"
          >
            {loading ? 'EXECUTING...' : 'DISPATCH DAG'}
          </button>
        </div>
        <div className="flex-1 bg-[#020610] border border-[#00f0ff]/15 rounded p-3 font-mono text-xs overflow-y-auto text-[#93c5fd]">
          {log.length === 0 ? 'Agent execution telemetry will stream here.' : log.map((line, i) => <div key={i} className="mb-1">{line}</div>)}
        </div>
      </div>

      <div className="bg-[#0c172d]/75 border border-[#00f0ff]/25 rounded-lg p-5 flex flex-col gap-3 backdrop-blur-md">
        <h3 className="hud-font text-sm text-[#00f0ff] tracking-wider border-b border-[#00f0ff]/15 pb-2.5">
          SPECIALIZED AGENTS
        </h3>
        <div className="flex flex-col gap-2.5 overflow-y-auto">
          {agents.map((a) => (
            <AgentStatus key={a.name} agent={a} />
          ))}
        </div>
      </div>
    </div>
  );
};
