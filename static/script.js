/* ============================================================
   LEXAI — AI Legislative Analyzer · script.js
   Connects to Flask backend at /api/search
   ============================================================ */

// ---- Config ----
const API_BASE = 'http://127.0.0.1:5000';  // Set to your deployed URL e.g. 'https://your-app.railway.app'
const API_URL  = `${API_BASE}/api/search`;

// ---- Elements ----
const queryInput     = document.getElementById('queryInput');
const searchBtn      = document.getElementById('searchBtn');
const loaderWrap     = document.getElementById('loaderWrap');
const resultsSection = document.getElementById('resultsSection');
const resultsGrid    = document.getElementById('resultsGrid');
const resultCount    = document.getElementById('resultCount');
const displayQuery   = document.getElementById('displayQuery');
const emptyState     = document.getElementById('emptyState');
const featuresSection= document.getElementById('featuresSection');

// ---- Enter key support ----
queryInput.addEventListener('keydown', e => {
  if (e.key === 'Enter') runSearch();
});

// ---- Suggestion chip fill ----
function fillQuery(text) {
  queryInput.value = text;
  queryInput.focus();
}

// ---- Main search function ----
async function runSearch() {
  const query = queryInput.value.trim();
  if (!query) {
    shakeInput();
    return;
  }

  // UI state: show loader
  setLoading(true);
  clearResults();
  featuresSection.style.display = 'none';

  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query })
    });

    if (!response.ok) throw new Error(`Server responded with ${response.status}`);

    const data = await response.json();
    renderResults(data.results || [], query);

  } catch (err) {
    console.error('Search error:', err);
    renderError(err.message);
  } finally {
    setLoading(false);
  }
}

// ---- Render results ----
function renderResults(results, query) {
  displayQuery.textContent = query;

  if (!results.length) {
    emptyState.style.display = 'block';
    resultsSection.style.display = 'none';
    return;
  }

  emptyState.style.display = 'none';
  resultsSection.style.display = 'block';
  resultCount.textContent = `${results.length} result${results.length !== 1 ? 's' : ''}`;

  resultsGrid.innerHTML = '';

  results.forEach((r, i) => {
    const card = document.createElement('div');
    card.className = 'result-card';
    card.style.animationDelay = `${i * 0.08}s`;

    card.innerHTML = `
      <div class="card-header">
        <span class="section-badge">📚 ${escHtml(r.section || 'Section')}</span>
        <span class="card-number">#${i + 1}</span>
      </div>

      ${buildBlock('summary',  '🧠 Summary',          r.summary,  'Summary not available.')}
      ${r.penalty ? buildBlock('penalty', '🚨 Penalty',   r.penalty,  '') : ''}
      ${r.info    ? buildBlock('info',    '💡 What to Know', r.info,  '') : ''}
      ${r.rights  ? buildBlock('rights',  '🛡️ Rights',    r.rights,   '') : ''}
      ${buildKeywords(r.keywords)}
    `;

    resultsGrid.appendChild(card);
  });
}

// ---- Build a colored info block ----
function buildBlock(type, label, text, fallback) {
  const content = text || fallback;
  if (!content) return '';
  return `
    <div class="block block-${type}">
      <div class="block-label">
        <span class="dot"></span>
        ${escHtml(label)}
      </div>
      <div class="block-body">${escHtml(content)}</div>
    </div>
  `;
}

// ---- Build keywords row ----
function buildKeywords(keywords) {
  if (!keywords) return '';
  const tags = keywords.split(',').map(k => k.trim()).filter(Boolean);
  if (!tags.length) return '';
  return `
    <div class="block">
      <div class="block-label" style="color:#9ca3af;">
        <span class="dot" style="background:#9ca3af;"></span>
        🏷️ Keywords
      </div>
      <div class="keywords-wrap">
        ${tags.map(t => `<span class="kw-tag">${escHtml(t)}</span>`).join('')}
      </div>
    </div>
  `;
}

// ---- Error card ----
function renderError(msg) {
  resultsSection.style.display = 'none';
  emptyState.style.display = 'block';
  emptyState.innerHTML = `
    <div class="empty-icon">⚠️</div>
    <p style="color:#f87171;">Could not reach the server.</p>
    <p style="font-size:12px;color:#3d4464;margin-top:8px;font-family:'DM Mono',monospace;">${escHtml(msg)}</p>
    <p style="font-size:13px;color:#7a82a6;margin-top:16px;">Make sure your Flask backend is running at <code style="color:#c6a352;">${API_URL}</code></p>
  `;
}

// ---- UI helpers ----
function setLoading(on) {
  loaderWrap.style.display = on ? 'block' : 'none';
  searchBtn.disabled = on;
  searchBtn.style.opacity = on ? '0.6' : '1';
}

function clearResults() {
  resultsGrid.innerHTML = '';
  resultsSection.style.display = 'none';
  emptyState.style.display = 'none';
  emptyState.innerHTML = `
    <div class="empty-icon">🔍</div>
    <p>No results found. Try rephrasing your query.</p>
  `;
}

function shakeInput() {
  const box = queryInput.closest('.search-box');
  box.style.animation = 'shake 0.4s ease';
  setTimeout(() => box.style.animation = '', 400);
}

function escHtml(str) {
  if (!str) return '';
  return str.toString()
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// ---- Inject shake keyframes dynamically ----
const shakeStyle = document.createElement('style');
shakeStyle.textContent = `
  @keyframes shake {
    0%,100%{transform:translateX(0)}
    20%{transform:translateX(-6px)}
    40%{transform:translateX(6px)}
    60%{transform:translateX(-4px)}
    80%{transform:translateX(4px)}
  }
`;
document.head.appendChild(shakeStyle);
