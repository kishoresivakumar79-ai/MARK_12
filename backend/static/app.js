/**
 * MARK 12 - Frontend Master Controller
 * Integrates Three.js 3D Neural Arc Core, Web Speech STT/TTS, Telemetry, and Subsystems.
 */

// Global State
let currentTab = 'dashboard';
let isListening = false;
let speechRecognizer = null;
let speechSynth = window.speechSynthesis;
let threeScene, threeCamera, threeRenderer, coreSphere, outerRings = [];

// Initialize on DOM Load
document.addEventListener('DOMContentLoaded', () => {
  initNavigation();
  initThreeJSCore();
  initSpeechRecognition();
  initChat();
  initDocUpload();
  initVisionUpload();
  pollSystemTelemetry();
  setInterval(pollSystemTelemetry, 3000);
  loadTasks('priority');
  loadMemories();
  loadAgentRoster();
  loadAutomationLogs();
});

/* ==========================================================================
   1. NAVIGATION & TABS
   ========================================================================== */
function initNavigation() {
  const navBtns = document.querySelectorAll('.nav-item');
  navBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const tabTarget = btn.getAttribute('data-tab');
      switchTab(tabTarget);
    });
  });
}

function switchTab(tabId) {
  currentTab = tabId;
  document.querySelectorAll('.nav-item').forEach(b => {
    b.classList.toggle('active', b.getAttribute('data-tab') === tabId);
  });
  document.querySelectorAll('.hud-section').forEach(s => {
    s.classList.toggle('active', s.id === `tab-${tabId}`);
  });
  if (tabId === 'tasks') loadTasks('priority');
  if (tabId === 'memory') loadMemories();
  if (tabId === 'agents') loadAgentRoster();
  if (tabId === 'automation') loadAutomationLogs();
}

/* ==========================================================================
   2. THREE.JS 3D NEURAL CORE VISUALIZER
   ========================================================================== */
function initThreeJSCore() {
  const canvas = document.getElementById('three-core-canvas');
  if (!canvas || !window.THREE) return;

  const width = canvas.parentElement.clientWidth;
  const height = canvas.parentElement.clientHeight;

  threeScene = new THREE.Scene();
  threeCamera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
  threeCamera.position.z = 8;

  threeRenderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
  threeRenderer.setSize(width, height);
  threeRenderer.setPixelRatio(window.devicePixelRatio);

  // Core Glowing Sphere
  const coreGeo = new THREE.IcosahedronGeometry(1.6, 2);
  const coreMat = new THREE.MeshBasicMaterial({
    color: 0x00f0ff,
    wireframe: true,
    transparent: true,
    opacity: 0.8
  });
  coreSphere = new THREE.Mesh(coreGeo, coreMat);
  threeScene.add(coreSphere);

  // Concentric Holographic Gyro Rings
  for (let i = 0; i < 3; i++) {
    const ringGeo = new THREE.TorusGeometry(2.2 + i * 0.45, 0.02, 16, 100);
    const ringMat = new THREE.MeshBasicMaterial({
      color: i === 1 ? 0x0077fe : 0x00f0ff,
      transparent: true,
      opacity: 0.5 + i * 0.15
    });
    const ring = new THREE.Mesh(ringGeo, ringMat);
    ring.rotation.x = Math.PI / (i + 2);
    ring.rotation.y = Math.PI / (i + 3);
    threeScene.add(ring);
    outerRings.push(ring);
  }

  // Animation Loop
  function animate() {
    requestAnimationFrame(animate);
    if (coreSphere) {
      coreSphere.rotation.x += 0.005;
      coreSphere.rotation.y += 0.008;
    }
    outerRings.forEach((ring, idx) => {
      ring.rotation.x += 0.003 * (idx + 1);
      ring.rotation.y += 0.004 * (idx + 1);
    });
    threeRenderer.render(threeScene, threeCamera);
  }
  animate();

  window.addEventListener('resize', () => {
    if (!canvas.parentElement) return;
    const w = canvas.parentElement.clientWidth;
    const h = canvas.parentElement.clientHeight;
    threeCamera.aspect = w / h;
    threeCamera.updateProjectionMatrix();
    threeRenderer.setSize(w, h);
  });
}

/* ==========================================================================
   3. SPEECH RECOGNITION & SYNTHESIS (VOICE PROTOCOL)
   ========================================================================== */
function initSpeechRecognition() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const voiceBtn = document.getElementById('btn-voice-toggle');
  const chatMicBtn = document.getElementById('chat-mic-button');
  const statusLabel = document.getElementById('voice-status-indicator');

  if (!SpeechRecognition) {
    if (statusLabel) statusLabel.innerText = "Web Speech API not supported in this browser. Use text input.";
    return;
  }

  speechRecognizer = new SpeechRecognition();
  speechRecognizer.continuous = false;
  speechRecognizer.interimResults = false;
  speechRecognizer.lang = 'en-US';

  speechRecognizer.onstart = () => {
    isListening = true;
    if (voiceBtn) {
      voiceBtn.classList.add('listening');
      document.getElementById('voice-btn-text').innerText = "LISTENING... (SPEAK DIRECTIVE)";
    }
    if (statusLabel) statusLabel.innerText = "Listening to voice input...";
  };

  speechRecognizer.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    if (statusLabel) statusLabel.innerText = `Interpreted: "${transcript}"`;
    sendChatMessage(transcript, true);
  };

  speechRecognizer.onerror = (event) => {
    isListening = false;
    resetVoiceBtn();
    if (statusLabel) statusLabel.innerText = `Voice error: ${event.error}`;
  };

  speechRecognizer.onend = () => {
    isListening = false;
    resetVoiceBtn();
  };

  if (voiceBtn) {
    voiceBtn.addEventListener('click', toggleVoiceListening);
  }
  if (chatMicBtn) {
    chatMicBtn.addEventListener('click', toggleVoiceListening);
  }
}

function toggleVoiceListening() {
  if (!speechRecognizer) return;
  if (isListening) {
    speechRecognizer.stop();
  } else {
    speechRecognizer.start();
  }
}

function resetVoiceBtn() {
  const voiceBtn = document.getElementById('btn-voice-toggle');
  if (voiceBtn) {
    voiceBtn.classList.remove('listening');
    document.getElementById('voice-btn-text').innerText = "INITIALIZE VOICE PROTOCOL";
  }
}

function speakText(text) {
  const audioFeedbackEnabled = document.getElementById('chk-speech-output')?.checked;
  if (!audioFeedbackEnabled || !speechSynth) return;

  speechSynth.cancel();
  // Strip code blocks and special characters
  const clean = text.replace(/```[\s\S]*?```/g, "Code block generated.").replace(/[*#_]/g, "");
  const utterance = new SpeechSynthesisUtterance(clean);
  utterance.rate = 1.05;
  utterance.pitch = 0.95;

  const voices = speechSynth.getVoices();
  const maleVoice = voices.find(v => v.name.includes("David") || v.name.includes("Christopher") || v.name.includes("Male") || v.lang.startsWith("en"));
  if (maleVoice) utterance.voice = maleVoice;

  speechSynth.speak(utterance);
}

/* ==========================================================================
   4. CHAT INTERACTION & REST API
   ========================================================================== */
function initChat() {
  const sendBtn = document.getElementById('chat-send-button');
  const chatInput = document.getElementById('chat-input');

  if (sendBtn && chatInput) {
    sendBtn.addEventListener('click', () => {
      const msg = chatInput.value.trim();
      if (msg) {
        sendChatMessage(msg, false);
        chatInput.value = '';
      }
    });

    chatInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        const msg = chatInput.value.trim();
        if (msg) {
          sendChatMessage(msg, false);
          chatInput.value = '';
        }
      }
    });
  }
}

async function sendChatMessage(messageText, isVoiceTriggered = false) {
  appendMessage('user', messageText, 'USER');

  // Pulse reactor
  if (coreSphere) {
    coreSphere.scale.set(1.2, 1.2, 1.2);
    setTimeout(() => coreSphere.scale.set(1, 1, 1), 600);
  }

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: messageText,
        conversation_id: 'default',
        enable_voice_response: isVoiceTriggered
      })
    });
    const data = await res.json();
    appendMessage('assistant', data.response, data.agent_used || 'MARK 12', data.intent);

    if (data.audio_url) {
      const audio = new Audio(data.audio_url);
      audio.play().catch(() => speakText(data.response));
    } else if (isVoiceTriggered) {
      speakText(data.response);
    }
  } catch (err) {
    appendMessage('assistant', `Connection error: ${err.message}`, 'SYSTEM', 'error');
  }
}

function appendMessage(sender, text, senderName, tag = 'DIRECTIVE') {
  const stream = document.getElementById('chat-stream');
  if (!stream) return;

  const bubble = document.createElement('div');
  bubble.className = `message-bubble ${sender === 'user' ? 'user-msg' : 'jarvis-msg'}`;

  // Formatter for markdown code blocks
  const formattedText = text.replace(/```([a-zA-Z]*)\n([\s\S]*?)```/g, (match, lang, code) => {
    return `<pre style="background:#020610; padding:10px; border-radius:6px; margin:8px 0; overflow-x:auto;"><code>${escapeHtml(code.trim())}</code></pre>`;
  });

  bubble.innerHTML = `
    <div class="msg-meta">
      <span class="msg-sender">${senderName}</span>
      <span class="msg-tag">${tag.toUpperCase()}</span>
    </div>
    <div class="msg-text">${formattedText}</div>
  `;

  stream.appendChild(bubble);
  stream.scrollTop = stream.scrollHeight;
}

function escapeHtml(str) {
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

/* ==========================================================================
   5. TELEMETRY & HARDWARE MONITORING
   ========================================================================== */
async function pollSystemTelemetry() {
  try {
    const res = await fetch('/api/system/status');
    const data = await res.json();
    
    document.getElementById('hud-cpu').innerText = `${Math.round(data.cpu_percent)}%`;
    document.getElementById('hud-ram').innerText = `${Math.round(data.memory_percent)}%`;
    
    const metricOs = document.getElementById('metric-os');
    const metricCpu = document.getElementById('metric-cpu');
    const metricRam = document.getElementById('metric-ram');
    const metricUptime = document.getElementById('metric-uptime');

    if (metricOs) metricOs.innerText = data.os;
    if (metricCpu) metricCpu.innerText = `${data.cpu_percent}%`;
    if (metricRam) metricRam.innerText = `${data.memory_percent}% (${data.memory_used_gb || 0}GB / ${data.memory_total_gb || 0}GB)`;
    if (metricUptime) metricUptime.innerText = `${Math.floor(data.uptime_seconds)}s`;
  } catch (e) {
    // Silently continue
  }
}

/* ==========================================================================
   6. TASK PRIORITY QUEUE & TREE
   ========================================================================== */
async function loadTasks(viewType = 'priority') {
  const container = document.getElementById('task-items-list');
  if (!container) return;

  try {
    const res = await fetch(`/api/tasks?view=${viewType}`);
    const tasks = await res.json();
    container.innerHTML = '';

    if (!tasks || tasks.length === 0) {
      container.innerHTML = `<p style="color:var(--text-muted); text-align:center; padding:20px;">No pending tasks in queue.</p>`;
      return;
    }

    tasks.forEach(t => {
      const card = document.createElement('div');
      card.className = `task-card-item priority-${t.priority}`;
      card.innerHTML = `
        <div>
          <div class="task-title">${escapeHtml(t.title)}</div>
          <div class="task-meta">Priority ${t.priority} • Status: ${t.status} ${t.due_date ? '• Due: ' + t.due_date : ''}</div>
        </div>
        <div style="display:flex; gap:6px;">
          <button class="btn-secondary" onclick="toggleTaskStatus('${t.id}', '${t.status === 'completed' ? 'pending' : 'completed'}')">${t.status === 'completed' ? 'REOPEN' : 'COMPLETE'}</button>
          <button class="btn-secondary" style="border-color:var(--red-alert); color:var(--red-alert);" onclick="deleteTask('${t.id}')">✕</button>
        </div>
      `;
      container.appendChild(card);
    });
  } catch (err) {
    container.innerHTML = `<p style="color:var(--red-alert);">Failed to load tasks: ${err.message}</p>`;
  }
}

async function submitCreateTask() {
  const title = document.getElementById('new-task-title').value.trim();
  const priority = parseInt(document.getElementById('new-task-priority').value);
  const desc = document.getElementById('new-task-desc').value.trim();

  if (!title) return alert("Please specify a task title.");

  await fetch('/api/tasks', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, priority, description: desc })
  });

  document.getElementById('new-task-title').value = '';
  document.getElementById('new-task-desc').value = '';
  loadTasks('priority');
}

async function toggleTaskStatus(taskId, newStatus) {
  await fetch(`/api/tasks/${taskId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ status: newStatus })
  });
  loadTasks('priority');
}

async function deleteTask(taskId) {
  await fetch(`/api/tasks/${taskId}`, { method: 'DELETE' });
  loadTasks('priority');
}

/* ==========================================================================
   7. SEMANTIC MEMORY MANAGEMENT
   ========================================================================== */
async function loadMemories(query = '') {
  const container = document.getElementById('memory-items-list');
  if (!container) return;

  try {
    const res = await fetch(`/api/memory?query=${encodeURIComponent(query)}`);
    const memories = await res.json();
    container.innerHTML = '';

    if (!memories || memories.length === 0) {
      container.innerHTML = `<p style="color:var(--text-muted); text-align:center; padding:20px;">No memories stored.</p>`;
      return;
    }

    memories.forEach(m => {
      const card = document.createElement('div');
      card.className = 'task-card-item priority-3';
      card.innerHTML = `
        <div>
          <div class="task-title">${escapeHtml(m.content || m.text || '')}</div>
          <div class="task-meta">Category: [${(m.category || 'general').toUpperCase()}] • Importance: ${m.importance || 3}</div>
        </div>
        <button class="btn-secondary" style="border-color:var(--red-alert); color:var(--red-alert);" onclick="deleteMemoryItem('${m.id}')">✕</button>
      `;
      container.appendChild(card);
    });
  } catch (err) {
    container.innerHTML = `<p style="color:var(--red-alert);">Failed to load memories: ${err.message}</p>`;
  }
}

function searchMemories(q) {
  loadMemories(q);
}

async function submitSaveMemory() {
  const cat = document.getElementById('new-mem-category').value;
  const content = document.getElementById('new-mem-content').value.trim();
  if (!content) return alert("Please enter memory content.");

  await fetch('/api/memory', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ category: cat, content: content, importance: 4 })
  });

  document.getElementById('new-mem-content').value = '';
  loadMemories();
}

async function deleteMemoryItem(memId) {
  await fetch(`/api/memory/${memId}`, { method: 'DELETE' });
  loadMemories();
}

/* ==========================================================================
   8. MULTI-AGENT WORKFLOW EXECUTION
   ========================================================================== */
async function loadAgentRoster() {
  const container = document.getElementById('agent-roster-list');
  if (!container) return;

  try {
    const res = await fetch('/api/agents');
    const data = await res.json();
    container.innerHTML = '';

    data.agents.forEach(a => {
      const row = document.createElement('div');
      row.className = 'auto-row';
      row.innerHTML = `
        <div>
          <strong>${a.name} Agent</strong>
          <p>${a.role}</p>
        </div>
        <span class="badge-pulse">ACTIVE</span>
      `;
      container.appendChild(row);
    });
  } catch (e) {}
}

async function triggerWorkflowExecution() {
  const input = document.getElementById('workflow-objective-input');
  const logBox = document.getElementById('workflow-execution-log');
  const objective = input.value.trim();
  if (!objective) return alert("Please specify a workflow objective.");

  logBox.style.display = 'block';
  logBox.innerHTML = `<div>[PLANNER] Architecting multi-agent DAG for: "${objective}"...</div>`;

  // Animate nodes
  const nodes = ['node-Planner', 'node-Research', 'node-Coding', 'node-Document'];
  nodes.forEach(n => document.getElementById(n)?.classList.add('active-executing'));

  try {
    const res = await fetch('/api/agents/workflow', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ objective })
    });
    const result = await res.json();

    let logHtml = `<div><strong>[SUCCESS] Multi-Agent Workflow Completed</strong></div>`;
    result.execution_log.forEach(step => {
      logHtml += `<div style="margin-top:6px;">⚡ <strong>Step ${step.step} (${step.agent})</strong>: ${escapeHtml(step.output.substring(0, 160))}...</div>`;
    });
    logBox.innerHTML = logHtml;
  } catch (err) {
    logBox.innerHTML = `<div style="color:var(--red-alert);">Workflow error: ${err.message}</div>`;
  } finally {
    nodes.forEach(n => document.getElementById(n)?.classList.remove('active-executing'));
  }
}

function executeQuickWorkflow() {
  switchTab('agents');
  document.getElementById('workflow-objective-input').value = "Compare top Python web frameworks (FastAPI vs Flask vs Django) and generate recommendation document";
  triggerWorkflowExecution();
}

/* ==========================================================================
   9. DOCUMENT INTELLIGENCE (INGESTION & RAG QA)
   ========================================================================== */
function initDocUpload() {
  const fileInput = document.getElementById('doc-file-input');
  if (fileInput) {
    fileInput.addEventListener('change', async (e) => {
      const file = e.target.files[0];
      if (!file) return;

      const formData = new FormData();
      formData.append('file', file);

      const statusEl = document.getElementById('doc-upload-status');
      statusEl.innerText = `Ingesting & chunking ${file.name}...`;

      try {
        const res = await fetch('/api/files/upload', { method: 'POST', body: formData });
        const data = await res.json();
        statusEl.innerText = `Document '${data.file_name}' indexed successfully (${data.chunk_count} chunks).`;

        // Update select
        const sel = document.getElementById('doc-select-active');
        sel.innerHTML = `<option value="${data.file_name}">${data.file_name} (${data.chunk_count} chunks)</option>`;
      } catch (err) {
        statusEl.innerText = `Upload failed: ${err.message}`;
      }
    });
  }
}

async function submitDocQA() {
  const sel = document.getElementById('doc-select-active').value;
  const q = document.getElementById('doc-question-input').value.trim();
  const resBox = document.getElementById('doc-qa-result');

  if (!sel || !q) return alert("Select an ingested document and enter a question.");

  resBox.style.display = 'block';
  resBox.innerText = "Analyzing semantic chunks...";

  const formData = new FormData();
  formData.append('file_name', sel);
  formData.append('question', q);

  try {
    const res = await fetch('/api/files/qa', { method: 'POST', body: formData });
    const data = await res.json();
    resBox.innerHTML = `<strong>Answer:</strong><p style="margin-top:6px;">${escapeHtml(data.answer)}</p>`;
  } catch (err) {
    resBox.innerText = `QA Query error: ${err.message}`;
  }
}

/* ==========================================================================
   10. COMPUTER VISION & OPTICAL DETECTION
   ========================================================================== */
function initVisionUpload() {
  const imgInput = document.getElementById('img-file-input');
  if (imgInput) {
    imgInput.addEventListener('change', async (e) => {
      const file = e.target.files[0];
      if (!file) return;

      const preview = document.getElementById('vision-img-element');
      preview.src = URL.createObjectURL(file);
      preview.style.display = 'block';

      const formData = new FormData();
      formData.append('file', file);

      const resContent = document.getElementById('vision-results-content');
      resContent.innerText = "Running optical detection & entity analysis...";

      try {
        const res = await fetch('/api/vision/analyze', { method: 'POST', body: formData });
        const data = await res.json();
        resContent.innerHTML = `
          <div><strong>File:</strong> ${data.file_name}</div>
          <div><strong>Resolution:</strong> ${data.metadata.width}x${data.metadata.height} (${data.metadata.format})</div>
          <div><strong>Entities Detected:</strong> ${data.detections.count}</div>
          <div style="margin-top:8px;">${escapeHtml(data.metadata.description)}</div>
        `;
      } catch (err) {
        resContent.innerText = `Vision analysis error: ${err.message}`;
      }
    });
  }
}

async function captureWebcamSnapshot() {
  const resContent = document.getElementById('vision-results-content');
  resContent.innerText = "Accessing camera frame...";
  try {
    const res = await fetch('/api/vision/snapshot', { method: 'POST' });
    const data = await res.json();
    if (data.success) {
      resContent.innerText = `Snapshot captured: ${data.path}`;
    } else {
      resContent.innerText = data.message;
    }
  } catch (e) {
    resContent.innerText = `Webcam error: ${e.message}`;
  }
}

/* ==========================================================================
   11. AUTOMATION & DESKTOP CONTROLS
   ========================================================================== */
async function executeQuickAction(action, target) {
  try {
    const res = await fetch('/api/automation/execute', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action, target })
    });
    const data = await res.json();
    alert(`Automation Response: ${data.message || 'Action executed successfully.'}`);
    loadAutomationLogs();
  } catch (err) {
    alert(`Automation error: ${err.message}`);
  }
}

async function loadAutomationLogs() {
  const container = document.getElementById('automation-audit-logs');
  if (!container) return;

  try {
    const res = await fetch('/api/automation/logs');
    const logs = await res.json();
    container.innerHTML = '';

    if (!logs || logs.length === 0) {
      container.innerHTML = `<p style="color:var(--text-muted); text-align:center; padding:10px;">Audit log clear.</p>`;
      return;
    }

    logs.forEach(l => {
      const row = document.createElement('div');
      row.className = 'auto-row';
      row.innerHTML = `
        <div>
          <strong>${l.action.toUpperCase()} : ${l.target || 'System'}</strong>
          <p>${l.details || ''} • ${l.timestamp}</p>
        </div>
        <span class="badge-cyan">${l.status}</span>
      `;
      container.appendChild(row);
    });
  } catch (e) {}
}
