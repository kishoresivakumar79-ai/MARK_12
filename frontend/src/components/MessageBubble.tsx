import React from 'react';
import { Message } from '../types';

export const MessageBubble: React.FC<{ message: Message }> = ({ message }) => {
  const isUser = message.sender === 'user';

  return (
    <div
      className={`max-w-[80%] p-4 rounded-lg leading-relaxed text-sm ${
        isUser
          ? 'self-end bg-[#0077fe]/20 border border-[#0077fe]/40 text-white'
          : 'self-start bg-[#00f0ff]/10 border border-[#00f0ff]/25 border-l-4 border-l-[#00f0ff]'
      }`}
    >
      <div className="flex justify-between items-center text-[11px] hud-font text-[#00f0ff] mb-1.5">
        <span>{message.agent_used || (isUser ? 'USER' : 'MARK 12')}</span>
        <span className="bg-[#00f0ff]/20 px-1.5 py-0.5 rounded text-[10px]">
          {(message.intent || 'DIRECTIVE').toUpperCase()}
        </span>
      </div>
      <div className="whitespace-pre-wrap">{message.content}</div>
    </div>
  );
};
