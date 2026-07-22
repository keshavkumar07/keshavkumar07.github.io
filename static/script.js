// ---------- Clock ----------
function tickClock() {
  const el = document.getElementById('clock');
  if (!el) return;
  el.textContent = new Date().toLocaleTimeString('en-GB', { hour12: false });
}
tickClock();
setInterval(tickClock, 1000);

// ---------- Elements ----------
const video = document.getElementById('camera-feed');
const canvas = document.getElementById('capture-canvas');
const startBtn = document.getElementById('start-camera');
const captureBtn = document.getElementById('capture-btn');
const nameInput = document.getElementById('enroll-name');
const nameField = document.getElementById('name-field');
const tabEnroll = document.getElementById('tab-enroll');
const tabRecognize = document.getElementById('tab-recognize');
const statusEl = document.getElementById('camera-status');
const sweepEl = document.querySelector('.sweep');
const readingEl = document.getElementById('reading');
const refreshBtn = document.getElementById('refresh-log');

let stream = null;
let mode = 'enroll';

// ---------- Mode switching ----------
function setMode(newMode) {
  mode = newMode;
  tabEnroll.classList.toggle('active', mode === 'enroll');
  tabRecognize.classList.toggle('active', mode === 'recognize');
  nameField.style.display = mode === 'enroll' ? 'block' : 'none';
  captureBtn.textContent = mode === 'enroll' ? 'Capture & Enroll' : 'Capture & Mark Attendance';
  hideStatus();
}
tabEnroll.addEventListener('click', () => setMode('enroll'));
tabRecognize.addEventListener('click', () => setMode('recognize'));

// ---------- Camera ----------
async function startCamera() {
  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    showStatus('error', 'Your browser does not support camera access.');
    return;
  }
  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' }, audio: false });
    video.srcObject = stream;
    await video.play();
    startBtn.textContent = 'Camera on';
    startBtn.disabled = true;
    captureBtn.disabled = false;
    readingEl.textContent = 'CAMERA LIVE';
  } catch (err) {
    showStatus('error', 'Could not access the camera. Check your browser permissions and try again.');
  }
}
startBtn.addEventListener('click', startCamera);

function grabFrame() {
  canvas.width = video.videoWidth || 320;
  canvas.height = video.videoHeight || 240;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  return canvas.toDataURL('image/jpeg', 0.85);
}

// ---------- Status banner ----------
function showStatus(type, text) {
  statusEl.style.display = 'flex';
  statusEl.className = 'terminal ' + type;
  const promptChar = type === 'success' ? '✔' : type === 'error' ? '✕' : 'i';
  statusEl.querySelector('.terminal-prompt').textContent = promptChar;
  statusEl.querySelector('.terminal-text').textContent = text;
}
function hideStatus() {
  statusEl.style.display = 'none';
}

// ---------- Capture + send ----------
async function captureAndSend() {
  if (!stream) {
    showStatus('error', 'Start the camera first.');
    return;
  }

  captureBtn.disabled = true;
  sweepEl.style.animationDuration = '0.6s';

  try {
    if (mode === 'enroll') {
      const name = nameInput.value.trim();
      if (!name) {
        showStatus('error', 'Enter a name first.');
        captureBtn.disabled = false;
        sweepEl.style.animationDuration = '3.2s';
        return;
      }

      readingEl.textContent = 'CAPTURING…';
      showStatus('info', 'Capturing face samples…');

      const images = [];
      for (let i = 0; i < 5; i++) {
        images.push(grabFrame());
        await new Promise((r) => setTimeout(r, 220));
      }

      const res = await fetch('/api/enroll', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, images }),
      });
      const data = await res.json();
      showStatus(data.ok ? 'success' : 'error', data.message);
      if (data.ok) {
        nameInput.value = '';
        updateStats(data.stats);
        refreshRecords();
      }
    } else {
      readingEl.textContent = 'MATCHING…';
      showStatus('info', 'Scanning face…');

      const image = grabFrame();
      const res = await fetch('/api/recognize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image }),
      });
      const data = await res.json();
      showStatus(data.ok ? (data.already_marked ? 'info' : 'success') : 'error', data.message);
      if (data.ok) {
        updateStats(data.stats);
        refreshRecords();
      }
    }
  } catch (err) {
    showStatus('error', 'Something went wrong reaching the server. Please try again.');
  } finally {
    readingEl.textContent = 'CAMERA LIVE';
    sweepEl.style.animationDuration = '3.2s';
    captureBtn.disabled = false;
  }
}
captureBtn.addEventListener('click', captureAndSend);

// ---------- Stats ----------
function updateStats(stats) {
  if (!stats) return;
  document.getElementById('stat-enrolled').textContent = stats.enrolled;
  document.getElementById('stat-today').textContent = stats.today;
  document.getElementById('stat-total').textContent = stats.total;
}

// ---------- Records table ----------
function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

function renderRecords(records) {
  const wrap = document.getElementById('log-body');
  const countEl = document.getElementById('log-count');
  countEl.textContent = `${records.length} record${records.length === 1 ? '' : 's'} found.`;

  if (records.length === 0) {
    wrap.innerHTML = `
      <div class="empty-state">
        <p>No attendance has been logged yet.</p>
        <span>Switch to <strong>02 · Verify</strong> above once someone is enrolled.</span>
      </div>`;
    return;
  }

  const rows = records.map((r) => `
    <tr>
      <td class="mono dim">#${String(r.id).padStart(4, '0')}</td>
      <td>${escapeHtml(r.name)}</td>
      <td class="mono">${r.date}</td>
      <td class="mono">${r.time}</td>
    </tr>`).join('');

  wrap.innerHTML = `
    <div class="table-wrap">
      <table>
        <thead><tr><th>ID</th><th>Name</th><th>Date</th><th>Time</th></tr></thead>
        <tbody>${rows}</tbody>
      </table>
    </div>`;
}

async function refreshRecords() {
  try {
    const res = await fetch('/api/records');
    const data = await res.json();
    renderRecords(data.records);
  } catch (err) {
    document.getElementById('log-count').textContent = 'Could not load records.';
  }
}
refreshBtn.addEventListener('click', refreshRecords);

// ---------- Init ----------
setMode('enroll');
refreshRecords();
