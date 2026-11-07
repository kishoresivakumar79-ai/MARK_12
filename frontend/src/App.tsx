import React from 'react';
import { AssistantProvider, useAssistant } from './context/AssistantContext';
import { Sidebar } from './components/Sidebar';
import { Dashboard } from './pages/Dashboard';
import { Chat } from './pages/Chat';
import { Tasks } from './pages/Tasks';
import { Memory } from './pages/Memory';
import { Documents } from './pages/Documents';
import { Agents } from './pages/Agents';
import { Settings } from './pages/Settings';

const MainLayout: React.FC = () => {
  const { activeTab, telemetry } = useAssistant();

  const renderPage = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard />;
      case 'chat':
        return <Chat />;
      case 'tasks':
        return <Tasks />;
      case 'memory':
        return <Memory />;
      case 'documents':
        return <Documents />;
      case 'agents':
        return <Agents />;
      case 'settings':
        return <Settings />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="flex flex-col h-screen w-screen overflow-hidden bg-[#050a14] text-[#e2f1ff]">
      {/* Top HUD Header */}
      <header className="h-16 border-b border-[#00f0ff]/20 bg-[#081020]/85 backdrop-blur-md flex items-center justify-between px-6">
        <div className="flex items-center gap-3">
          <div className="w-6 h-6 rounded-full border-2 border-[#00f0ff] shadow-[0_0_10px_#00f0ff] animate-pulse"></div>
          <div>
            <h1 className="hud-font text-lg font-bold text-[#00f0ff] tracking-widest drop-shadow-[0_0_12px_#00f0ff]">
              MARK 12
            </h1>
            <span className="text-[10px] text-[#829ab1] tracking-wider font-mono">
              SYSTEM OS v2.4 // REACT TS CORE
            </span>
          </div>
        </div>

        <div className="flex gap-3 text-xs font-mono">
          <div className="bg-[#00f0ff]/10 border border-[#00f0ff]/25 px-3 py-1 rounded">
            CPU: <span className="text-[#00f0ff] font-bold">{telemetry?.cpu_percent || 12}%</span>
          </div>
          <div className="bg-[#00f0ff]/10 border border-[#00f0ff]/25 px-3 py-1 rounded">
            RAM: <span className="text-[#00f0ff] font-bold">{telemetry?.memory_percent || 38}%</span>
          </div>
          <div className="bg-[#00f0ff]/10 border border-[#00f0ff]/25 px-3 py-1 rounded">
            STATUS: <span className="text-[#00ff88] font-bold">OPERATIONAL</span>
          </div>
        </div>
      </header>

      {/* Main Content Workspace */}
      <div className="flex flex-1 overflow-hidden">
        <Sidebar />
        <main className="flex-1 p-6 overflow-y-auto">{renderPage()}</main>
      </div>
    </div>
  );
};

export const App: React.FC = () => {
  return (
    <AssistantProvider>
      <MainLayout />
    </AssistantProvider>
  );
};

export default App;
