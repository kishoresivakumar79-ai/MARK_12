import React from 'react';

export const Settings: React.FC = () => {
  return (
    <div className="bg-[#0c172d]/75 border border-[#00f0ff]/25 rounded-lg p-6 max-w-2xl backdrop-blur-md">
      <h3 className="hud-font text-sm text-[#00f0ff] tracking-wider border-b border-[#00f0ff]/15 pb-2.5 mb-4">
        SYSTEM & SECURITY CONFIGURATION
      </h3>
      <div className="flex flex-col gap-4 text-sm">
        <div>
          <label className="text-xs text-[#00f0ff] hud-font block mb-1">AI Reasoning Provider</label>
          <select className="w-full bg-[#00f0ff]/5 border border-[#00f0ff]/20 rounded p-2 text-white">
            <option value="offline">Smart Offline Core (Built-in)</option>
            <option value="gemini">Google Gemini 1.5</option>
            <option value="openai">OpenAI GPT-4o</option>
            <option value="ollama">Local Ollama Llama-3</option>
          </select>
        </div>

        <div>
          <label className="text-xs text-[#00f0ff] hud-font block mb-1">Voice Synthesizer Engine</label>
          <select className="w-full bg-[#00f0ff]/5 border border-[#00f0ff]/20 rounded p-2 text-white">
            <option value="edge_tts">Edge Neural TTS (Christopher)</option>
            <option value="system_tts">Native System SAPI5 / pyttsx3</option>
            <option value="web_speech">Browser Web Speech API</option>
          </select>
        </div>

        <div className="flex items-center gap-2 mt-2">
          <input type="checkbox" id="chk-safety" defaultChecked />
          <label htmlFor="chk-safety">Require Confirmation for Destructive File Operations</label>
        </div>

        <div className="flex items-center gap-2">
          <input type="checkbox" id="chk-auto-open" defaultChecked />
          <label htmlFor="chk-auto-open">Allow Whitelisted Desktop App Launching</label>
        </div>
      </div>
    </div>
  );
};
