export interface Message {
  id: string;
  sender: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
  intent?: string;
  agent_used?: string;
  audio_url?: string;
}

export interface Task {
  id: string;
  title: string;
  description?: string;
  priority: number;
  status: 'pending' | 'in_progress' | 'completed' | 'cancelled';
  parent_id?: string;
  due_date?: string;
  created_at: string;
}

export interface Memory {
  id: string;
  category: string;
  content: string;
  importance: number;
  tags?: string;
  created_at: string;
}

export interface AgentStatus {
  name: string;
  role: string;
  status: string;
  connections: string[];
}

export interface SystemTelemetry {
  os: string;
  cpu_percent: number;
  memory_percent: number;
  disk_percent: number;
  uptime_seconds: number;
  status: string;
  active_agents: string[];
}
