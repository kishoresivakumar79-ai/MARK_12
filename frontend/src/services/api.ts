import { Message, Task, Memory, AgentStatus, SystemTelemetry } from '../types';

const API_BASE = '/api';

export const api = {
  // Chat
  sendMessage: async (message: string, convId = 'default', voice = false) => {
    const res = await fetch(`${API_BASE}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, conversation_id: convId, enable_voice_response: voice })
    });
    return res.json();
  },
  getChatHistory: async (convId = 'default') => {
    const res = await fetch(`${API_BASE}/chat/history?conversation_id=${convId}`);
    return res.json();
  },

  // Tasks
  getTasks: async (view = 'priority'): Promise<Task[]> => {
    const res = await fetch(`${API_BASE}/tasks?view=${view}`);
    return res.json();
  },
  createTask: async (task: Partial<Task>) => {
    const res = await fetch(`${API_BASE}/tasks`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(task)
    });
    return res.json();
  },
  updateTask: async (id: string, updates: Partial<Task>) => {
    const res = await fetch(`${API_BASE}/tasks/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updates)
    });
    return res.json();
  },
  deleteTask: async (id: string) => {
    const res = await fetch(`${API_BASE}/tasks/${id}`, { method: 'DELETE' });
    return res.json();
  },

  // Memories
  getMemories: async (query = ''): Promise<Memory[]> => {
    const res = await fetch(`${API_BASE}/memory?query=${encodeURIComponent(query)}`);
    return res.json();
  },
  saveMemory: async (memory: Partial<Memory>) => {
    const res = await fetch(`${API_BASE}/memory`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(memory)
    });
    return res.json();
  },
  deleteMemory: async (id: string) => {
    const res = await fetch(`${API_BASE}/memory/${id}`, { method: 'DELETE' });
    return res.json();
  },

  // Agents
  getAgents: async (): Promise<{ agents: AgentStatus[]; graph_topology: any }> => {
    const res = await fetch(`${API_BASE}/agents`);
    return res.json();
  },
  runWorkflow: async (objective: string) => {
    const res = await fetch(`${API_BASE}/agents/workflow`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ objective })
    });
    return res.json();
  },

  // System
  getTelemetry: async (): Promise<SystemTelemetry> => {
    const res = await fetch(`${API_BASE}/system/status`);
    return res.json();
  },

  // Automation
  executeAutomation: async (action: string, target = '') => {
    const res = await fetch(`${API_BASE}/automation/execute`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action, target })
    });
    return res.json();
  }
};
