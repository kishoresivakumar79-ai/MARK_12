import React, { useState } from 'react';

export const Documents: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState('');
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');

  const handleUpload = async () => {
    if (!file) return;
    setStatus(`Ingesting ${file.name}...`);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch('/api/files/upload', { method: 'POST', body: formData });
      const data = await res.json();
      setStatus(`Ingested ${data.file_name} successfully (${data.chunk_count} chunks).`);
    } catch (e: any) {
      setStatus(`Upload failed: ${e.message}`);
    }
  };

  const handleAsk = async () => {
    if (!file || !question) return;
    setAnswer('Searching semantic document chunks...');
    const formData = new FormData();
    formData.append('file_name', file.name);
    formData.append('question', question);

    try {
      const res = await fetch('/api/files/qa', { method: 'POST', body: formData });
      const data = await res.json();
      setAnswer(data.answer);
    } catch (e: any) {
      setAnswer(`Error: ${e.message}`);
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 h-full">
      <div className="bg-[#0c172d]/75 border border-[#00f0ff]/25 rounded-lg p-5 flex flex-col gap-3 backdrop-blur-md">
        <h3 className="hud-font text-sm text-[#00f0ff] tracking-wider border-b border-[#00f0ff]/15 pb-2.5">
          DOCUMENT INGESTION
        </h3>
        <input
          type="file"
          accept=".pdf,.docx,.txt,.md"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
          className="bg-[#00f0ff]/5 border border-[#00f0ff]/20 rounded p-2 text-sm text-white"
        />
        <button
          onClick={handleUpload}
          className="bg-[#00f0ff] text-black font-extrabold p-2 rounded hud-font text-xs"
        >
          INDEX DOCUMENT
        </button>
        {status && <div className="text-xs text-[#00ff88] font-mono mt-2">{status}</div>}
      </div>

      <div className="bg-[#0c172d]/75 border border-[#00f0ff]/25 rounded-lg p-5 flex flex-col gap-3 backdrop-blur-md">
        <h3 className="hud-font text-sm text-[#00f0ff] tracking-wider border-b border-[#00f0ff]/15 pb-2.5">
          GROUNDED DOCUMENT Q&A
        </h3>
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a question about the uploaded document..."
          className="bg-[#00f0ff]/5 border border-[#00f0ff]/20 rounded p-2 text-sm text-white"
        />
        <button
          onClick={handleAsk}
          className="bg-[#0077fe] text-white font-extrabold p-2 rounded hud-font text-xs"
        >
          QUERY INTELLIGENCE
        </button>
        {answer && <div className="bg-[#020610] p-3 rounded text-sm text-[#e2f1ff] whitespace-pre-wrap">{answer}</div>}
      </div>
    </div>
  );
};
