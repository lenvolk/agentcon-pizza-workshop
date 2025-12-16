const STORAGE_KEY = 'volkPizzaChatState';

function nowIso() {
  return new Date().toISOString();
}

function uuid() {
  // Browser-safe UUID (fallback if crypto.randomUUID is unavailable)
  if (globalThis.crypto && typeof globalThis.crypto.randomUUID === 'function') {
    return globalThis.crypto.randomUUID();
  }
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0;
    const v = c === 'x' ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
}

function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

function saveState(state) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

function clearState() {
  localStorage.removeItem(STORAGE_KEY);
}

function el(id) {
  return document.getElementById(id);
}

const landing = el('landing');
const chat = el('chat');
const welcomeBtn = el('welcomeBtn');
const welcomeStatus = el('welcomeStatus');
const sessionStatus = el('sessionStatus');
const messagesEl = el('messages');
const chatForm = el('chatForm');
const chatInput = el('chatInput');
const endChatBtn = el('endChatBtn');
const errorPanel = el('errorPanel');
const errorMessage = el('errorMessage');
const errorHint = el('errorHint');

let state = loadState() || {
  sessionId: null,
  status: 'idle',
  messages: [],
  lastError: null,
};

let starting = false;

function setView(view) {
  if (view === 'landing') {
    landing.hidden = false;
    chat.hidden = true;
  } else {
    landing.hidden = true;
    chat.hidden = false;
  }
}

function setStatus(status) {
  state.status = status;
  if (status === 'idle') {
    welcomeStatus.textContent = '';
  }
  sessionStatus.textContent = status === 'idle' ? 'starting' : status;
  saveState(state);
}

function showError(err) {
  errorPanel.hidden = false;
  const message = err?.error?.message || 'Unknown error';
  const hint = err?.error?.hint || '';
  errorMessage.textContent = message;
  errorHint.textContent = hint;
  errorHint.style.display = hint ? 'block' : 'none';

  state.lastError = { message, hint };
  saveState(state);
}

function hideError() {
  errorPanel.hidden = true;
  errorMessage.textContent = '';
  errorHint.textContent = '';

  if (state.lastError) {
    state.lastError = null;
    saveState(state);
  }
}

function renderMessages() {
  messagesEl.innerHTML = '';
  for (const m of state.messages) {
    const li = document.createElement('li');
    li.className = 'message';

    const meta = document.createElement('div');
    meta.className = 'message__meta';

    const left = document.createElement('div');
    left.textContent = m.role === 'user' ? 'You' : 'Agent';

    const right = document.createElement('div');
    right.textContent = new Date(m.createdAt).toLocaleTimeString();

    meta.appendChild(left);
    meta.appendChild(right);

    const bubble = document.createElement('div');
    bubble.className = 'message__bubble';
    bubble.textContent = m.content;

    li.appendChild(meta);
    li.appendChild(bubble);
    messagesEl.appendChild(li);
  }
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

async function apiPost(path, body) {
  const res = await fetch(path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });

  const json = await res.json().catch(() => null);
  if (!res.ok) {
    throw json || { error: { message: `Request failed (${res.status})` } };
  }
  return json;
}

async function startSession() {
  if (starting) return;
  starting = true;
  hideError();

  welcomeBtn.disabled = true;
  welcomeStatus.textContent = 'Starting…';

  if (!state.sessionId) {
    state.sessionId = uuid();
  }

  setView('chat');
  setStatus('starting');
  renderMessages();

  try {
    await apiPost('/api/session/start', { sessionId: state.sessionId });
    setStatus('ready');
    welcomeStatus.textContent = '';
  } catch (err) {
    setStatus('failed');
    showError(err);
    welcomeStatus.textContent = 'Failed to start.';
  } finally {
    welcomeBtn.disabled = false;
    starting = false;
  }
}

async function sendMessage(text) {
  hideError();

  if (text.length > 5000) {
    setStatus('failed');
    showError({ error: { message: 'Message too long (max 5000 characters).' } });
    return;
  }

  state.messages.push({
    id: uuid(),
    role: 'user',
    content: text,
    createdAt: nowIso(),
  });
  saveState(state);
  renderMessages();

  try {
    const resp = await apiPost('/api/session/message', {
      sessionId: state.sessionId,
      message: text,
    });

    state.messages.push({
      id: uuid(),
      role: 'agent',
      content: resp.reply || '',
      createdAt: nowIso(),
    });

    setStatus('ready');
    saveState(state);
    renderMessages();
  } catch (err) {
    setStatus('failed');
    showError(err);
  }
}

async function endSession() {
  hideError();
  const sid = state.sessionId;

  try {
    if (sid) {
      await apiPost('/api/session/end', { sessionId: sid });
    }
  } catch {
    // Best-effort.
  }

  clearState();
  state = { sessionId: null, status: 'idle', messages: [] };
  welcomeStatus.textContent = '';
  welcomeBtn.disabled = false;
  setView('landing');
}

welcomeBtn.addEventListener('click', () => {
  startSession();
});

chatForm.addEventListener('submit', (e) => {
  e.preventDefault();
  const value = chatInput.value.trim();
  if (!value) return;
  chatInput.value = '';
  sendMessage(value);
});

endChatBtn.addEventListener('click', () => {
  endSession();
});

window.addEventListener('beforeunload', () => {
  // Best-effort cleanup on page unload.
  // Using sendBeacon keeps it simple and doesn't block unload.
  try {
    if (state?.sessionId) {
      navigator.sendBeacon(
        '/api/session/end',
        new Blob([JSON.stringify({ sessionId: state.sessionId })], {
          type: 'application/json',
        })
      );
    }
  } catch {
    // Ignore.
  }
});

// Initial render
if (state.sessionId && (state.status === 'ready' || state.status === 'starting')) {
  setView('chat');
  sessionStatus.textContent = state.status;
  renderMessages();
} else {
  // If a previous attempt failed, don't trap users on the chat screen.
  // Show the landing page so they can retry cleanly.
  setView('landing');
  if (state.status === 'failed') {
    const msg = state.lastError?.message || 'Previous session failed. Click Welcome to retry.';
    welcomeStatus.textContent = msg;
  }
}
