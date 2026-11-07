import React from 'react';
import { useAssistant } from '../context/AssistantContext';
import { VoiceButton } from '../components/VoiceButton';
import { useVoice } from '../hooks/useVoice';
import { api } from '../services/api';

export const Dashboard: React.FC = () => {
  const { telemetry, sendMessage, setActiveTab } = useAssistant();
  const { isListening, startListening } = useVoice((transcript) => {
    sendMessage(transcript, true);
  });

  const handleQuickAction = async (action: string, target: string) => {
    await api.executeAutomation(action, target);
    alert(`Automation initiated: ${action} ${target}`);
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 h-full">
      {/* 3D Arc Reactor Holographic Hub */}
      <div className="bg-[#0c172d]/75 border border-[#00f0ff]/25 rounded-lg p-5 flex flex-col justify-between backdrop-blur-md">
        <div>
          <div className="flex justify-between items-center border-b border-[#00f0ff]/15 pb-2.5 mb-4">
            <h3 className="hud-font text-sm text-[#00f0ff] tracking-wider">NEURAL CORE 3D VISUALIZER</h3>
            <span className="text-[10px] bg-[#00ff88]/20 text-[#00ff88] px-2 py-0.5 rounded font-mono">
              ONLINE
            </span>
          </div>
          <div className="h-64 rounded-md bg-radial from-[#00f0ff]/10 to-transparent flex items-center justify-center relative overflow-hidden">
            <div className="w-32 h-32 rounded-full border-2 border-[#00f0ff] shadow-[0_0_30px_#00f0ff] animate-spin flex items-center justify-center">
              <div className="w-20 h-20 rounded-full border border-[#0077fe] shadow-[0_0_20px_#0077fe]"></div>
            </div>
            <div className="absolute bottom-3 left-3 bg-[#030712]/80 p-2 px-3 rounded border-l-2 border-[#00f0ff] font-mono text-xs">
              <div>QUANTUM BRAIN: <span className="text-[#00f0ff]">ACTIVE</span></div>
              <div>MULTI-AGENT: <span className="text-[#00ff88]">SYNCHRONIZED</span></div>
            </div>
          </div>
        </div>

        <div className="mt-4">
          <VoiceButton isListening={isListening} onClick={startListening} />
        </div>
      </div>

      {/* Quick Directives & Telemetry */}
      <div className="flex flex-col gap-5">
        <div className="bg-[#0c172d]/75 border border-[#00f0ff]/25 rounded-lg p-5 backdrop-blur-md">
          <h3 className="hud-font text-sm text-[#00f0ff] tracking-wider border-b border-[#00f0ff]/15 pb-2.5 mb-3">
            QUICK DESKTOP DIRECTIVES
          </h3>
          <div className="grid grid-cols-2 gap-2.5">
            <button
              onClick={() => handleQuickAction('launch', 'notepad')}
              className="p-3 bg-[#00f0ff]/5 border border-[#00f0ff]/20 rounded-md text-left hover:bg-[#00f0ff]/15"
            >
              📝 Open Notepad
            </button>
            <button
              onClick={() => handleQuickAction('launch', 'calculator')}
              className="p-3 bg-[#00f0ff]/5 border border-[#00f0ff]/20 rounded-md text-left hover:bg-[#00f0ff]/15"
            >
              🔢 Open Calculator
            </button>
            <button
              onClick={() => handleQuickAction('launch', 'browser')}
              className="p-3 bg-[#00f0ff]/5 border border-[#00f0ff]/20 rounded-md text-left hover:bg-[#00f0ff]/15"
            >
              🌐 Open Browser
            </button>
            <button
              onClick={() => handleQuickAction('screenshot', 'screen')}
              className="p-3 bg-[#00f0ff]/5 border border-[#00f0ff]/20 rounded-md text-left hover:bg-[#00f0ff]/15"
            >
              📸 Capture Screen
            </button>
          </div>
        </div>

        <div className="bg-[#0c172d]/75 border border-[#00f0ff]/25 rounded-lg p-5 backdrop-blur-md">
          <h3 className="hud-font text-sm text-[#00f0ff] tracking-wider border-b border-[#00f0ff]/15 pb-2.5 mb-3">
            HARDWARE & RUNTIME METRICS
          </h3>
          <div className="flex flex-col gap-2 text-sm">
            <div className="flex justify-between border-b border-white/5 py-1">
              <span className="text-[#829ab1]">HOST OS</span>
              <strong className="text-[#00f0ff] font-mono">{telemetry?.os || 'Windows 11'}</strong>
            </div>
            <div className="flex justify-between border-b border-white/5 py-1">
              <span className="text-[#829ab1]">CPU UTILIZATION</span>
              <strong className="text-[#00f0ff] font-mono">{telemetry?.cpu_percent || 14}%</strong>
            </div>
            <div className="flex justify-between border-b border-white/5 py-1">
              <span className="text-[#829ab1]">RAM CONSUMPTION</span>
              <strong className="text-[#00f0ff] font-mono">{telemetry?.memory_percent || 42}%</strong>
            </div>
            <div className="flex justify-between border-b border-white/5 py-1">
              <span className="text-[#829ab1]">ACTIVE AGENTS</span>
              <strong className="text-[#00ff88] font-mono">7 ONLINE</strong>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
