import React, { useState } from 'react';
import { useAssistant } from '../context/AssistantContext';
import { MessageBubble } from './MessageBubble';
import { useVoice } from '../hooks/useVoice';

export const ChatWindow: React.FC = () => {
  const { messages, sendMessage, isProcessing } = useAssistant();
  const [input, setInput] = useState('');
  const { isListening, startListening, speak } = useVoice((transcript) => {
    sendMessage(transcript, true);
  });

  const handleSend = () => {
    if (!input.trim() || isProcessing) return;
    sendMessage(input.trim());
    setInput('');
  };

  return (
    <div className="flex flex-col h-full bg-[#0c172d]/75 border border-[#00f0ff]/25 rounded-lg overflow-hidden backdrop-blur-md">
      <div className="flex justify-between items-center p-3 px-5 border-b border-[#00f0ff]/15 bg-[#050a14]/50 hud-font text-xs">
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-[#00ff88] shadow-[0_0_8px_#00ff88]"></span>
          <span>MARK 12 CONVERSATIONAL CORE</span>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-5 flex flex-col gap-4">
        {messages.map((m) => (
          <MessageBubble key={m.id} message={m} />
        ))}
      </div>

      <div className="p-3.5 px-5 bg-[#050a14]/80 border-t border-[#00f0ff]/20 flex gap-2.5">
        <button
          onClick={startListening}
          className={`px-4 rounded-md border border-[#00f0ff]/30 text-[#00f0ff] ${
            isListening ? 'bg-[#ff0055] text-white animate-pulse' : 'bg-[#00f0ff]/10'
          }`}
        >
          🎙
        </button>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Transmit directive or query... (e.g. 'Compare python web frameworks and save to doc')"
          className="flex-1 bg-[#00f0ff]/5 border border-[#00f0ff]/20 rounded-md px-4 py-2.5 text-white outline-none focus:border-[#00f0ff]"
        />
        <button
          onClick={handleSend}
          disabled={isProcessing}
          className="bg-[#00f0ff] text-black font-extrabold px-6 rounded-md hud-font text-xs hover:shadow-[0_0_16px_#00f0ff]"
        >
          {isProcessing ? 'TRANSMITTING...' : 'TRANSMIT'}
        </button>
      </div>
    </div>
  );
};
