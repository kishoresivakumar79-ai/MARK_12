import React, { createContext, useContext, useState, useEffect } from 'react';
import { api } from '../services/api';
import { SystemTelemetry, Message } from '../types';

interface AssistantContextType {
  telemetry: SystemTelemetry | null;
  activeTab: string;
  setActiveTab: (tab: string) => void;
  messages: Message[];
  sendMessage: (text: string, voice?: boolean) => Promise<void>;
  isProcessing: boolean;
}

const AssistantContext = createContext<AssistantContextType | null>(null);

export const AssistantProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [telemetry, setTelemetry] = useState<SystemTelemetry | null>(null);
  const [activeTab, setActiveTab] = useState<string>('dashboard');
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome-01',
      sender: 'assistant',
      content: 'MARK 12 system operational. All neural cores and automation subsystems online.',
      timestamp: new Date().toISOString(),
      agent_used: 'MARK 12'
    }
  ]);
  const [isProcessing, setIsProcessing] = useState<boolean>(false);

  useEffect(() => {
    const fetchTelemetry = async () => {
      try {
        const data = await api.getTelemetry();
        setTelemetry(data);
      } catch (e) {}
    };
    fetchTelemetry();
    const interval = setInterval(fetchTelemetry, 3500);
    return () => clearInterval(interval);
  }, []);

  const sendMessage = async (text: string, voice = false) => {
    const userMsg: Message = {
      id: `usr_${Date.now()}`,
      sender: 'user',
      content: text,
      timestamp: new Date().toISOString()
    };
    setMessages((prev) => [...prev, userMsg]);
    setIsProcessing(true);

    try {
      const resp = await api.sendMessage(text, 'default', voice);
      const jarvisMsg: Message = {
        id: `jar_${Date.now()}`,
        sender: 'assistant',
        content: resp.response,
        timestamp: new Date().toISOString(),
        agent_used: resp.agent_used,
        intent: resp.intent,
        audio_url: resp.audio_url
      };
      setMessages((prev) => [...prev, jarvisMsg]);
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          id: `err_${Date.now()}`,
          sender: 'system',
          content: `Error: ${err.message}`,
          timestamp: new Date().toISOString()
        }
      ]);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <AssistantContext.Provider
      value={{ telemetry, activeTab, setActiveTab, messages, sendMessage, isProcessing }}
    >
      {children}
    </AssistantContext.Provider>
  );
};

export const useAssistant = () => {
  const context = useContext(AssistantContext);
  if (!context) throw new Error('useAssistant must be used within an AssistantProvider');
  return context;
};
