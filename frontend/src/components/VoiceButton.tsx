import React from 'react';

interface VoiceButtonProps {
  isListening: boolean;
  onClick: () => void;
  label?: string;
}

export const VoiceButton: React.FC<VoiceButtonProps> = ({
  isListening,
  onClick,
  label = 'INITIALIZE VOICE PROTOCOL'
}) => {
  return (
    <button
      onClick={onClick}
      className={`w-full py-3.5 px-4 rounded-md font-extrabold text-xs tracking-wider transition-all flex items-center justify-center gap-2 hud-font ${
        isListening
          ? 'bg-gradient-to-r from-[#ff0055] to-[#ffb703] text-white shadow-[0_0_24px_rgba(255,0,85,0.8)] animate-pulse'
          : 'bg-gradient-to-r from-[#0077fe] to-[#00f0ff] text-black shadow-[0_0_20px_rgba(0,240,255,0.4)] hover:shadow-[0_0_30px_rgba(0,240,255,0.7)]'
      }`}
    >
      <span>🎙</span>
      <span>{isListening ? 'LISTENING... (SPEAK DIRECTIVE)' : label}</span>
    </button>
  );
};
