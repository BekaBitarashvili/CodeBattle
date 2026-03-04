/* ═══════════════════════════════════════
   CodeMama — main.js
═══════════════════════════════════════ */

/* ── LOADER ── */
const loader     = document.getElementById('loader');
const loaderText = document.getElementById('loaderText');
const loadMsgs   = { ka: ['იტვირთება...','კომპილირება...','მომზადება...'], en: ['Loading...','Compiling...','Preparing...'] };
let   loadIdx    = 0;
const loadLang   = typeof APP_LANG !== 'undefined' ? APP_LANG : 'ka';
const loadTimer  = setInterval(() => {
  loadIdx++;
  const msgs = loadMsgs[loadLang] || loadMsgs.ka;
  if (loadIdx < msgs.length && loaderText) loaderText.textContent = msgs[loadIdx];
}, 500);
window.addEventListener('load', () => {
  clearInterval(loadTimer);
  setTimeout(() => loader && loader.classList.add('hidden'), 700);
});

/* ── CUSTOM CURSOR ── */
const cur = document.getElementById('cursor');
const dot = document.getElementById('cursor-dot');
if (cur && dot) {
  document.addEventListener('mousemove', e => {
    cur.style.left = e.clientX + 'px'; cur.style.top = e.clientY + 'px';
    dot.style.left = e.clientX + 'px'; dot.style.top = e.clientY + 'px';
  });
  document.addEventListener('mouseover', e => {
    if (e.target.matches('a,button,[role="button"]')) cur.classList.add('hover');
    else cur.classList.remove('hover');
  });
}

/* ── THEME ── */
const themeToggle = document.getElementById('themeToggle');
const htmlRoot    = document.getElementById('htmlRoot') || document.documentElement;
const knob        = themeToggle ? themeToggle.querySelector('.theme-toggle-knob') : null;

const savedTheme = localStorage.getItem('cq_theme');
if (savedTheme) {
  htmlRoot.dataset.theme = savedTheme;
  if (knob) knob.textContent = savedTheme === 'dark' ? '🌙' : '☀️';
}
if (themeToggle) {
  themeToggle.addEventListener('click', () => {
    const isDark = htmlRoot.dataset.theme === 'dark';
    htmlRoot.dataset.theme = isDark ? 'light' : 'dark';
    if (knob) knob.textContent = isDark ? '☀️' : '🌙';
    localStorage.setItem('cq_theme', isDark ? 'light' : 'dark');
  });
}

/* ── HAMBURGER ── */
const hamburger = document.getElementById('hamburger');
const mobileNav = document.getElementById('mobileNav');
if (hamburger && mobileNav) {
  hamburger.addEventListener('click', () => mobileNav.classList.toggle('open'));
}
function closeMobile() { mobileNav && mobileNav.classList.remove('open'); }

/* ── SCROLL REVEAL ── */
const revealObserver = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
}, { threshold: 0.08 });
document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

/* ── XP TOAST ── */
function showXP(amount = '+50 XP') {
  const t   = document.getElementById('xpToast');
  const amt = document.getElementById('xpAmount');
  if (!t) return;
  if (amt) amt.textContent = amount;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 2800);
}

/* ── AUTH MODAL ── */
function openModal(tab = 'login') {
  const m = document.getElementById('authModal');
  if (!m) { window.location.href = URLS.login; return; }
  m.classList.add('open');
  switchTab(tab);
}
function closeModal() {
  const m = document.getElementById('authModal');
  if (m) m.classList.remove('open');
}
function switchTab(tab) {
  const lf = document.getElementById('loginForm');
  const rf = document.getElementById('registerForm');
  const tl = document.getElementById('tabLogin');
  const tr = document.getElementById('tabRegister');
  if (lf) lf.style.display    = tab === 'login'    ? '' : 'none';
  if (rf) rf.style.display    = tab === 'register' ? '' : 'none';
  if (tl) tl.classList.toggle('active', tab === 'login');
  if (tr) tr.classList.toggle('active', tab === 'register');
}
const overlay = document.getElementById('authModal');
if (overlay) overlay.addEventListener('click', e => { if (e.target === overlay) closeModal(); });

/* ── AJAX LOGIN ── */
async function submitLogin() {
  const email    = document.getElementById('loginEmail')?.value;
  const password = document.getElementById('loginPassword')?.value;
  const errEl    = document.getElementById('loginError');
  if (!email || !password) { if (errEl) errEl.textContent = 'ყველა ველი სავალდებულოა.'; return; }
  try {
    const r    = await fetch(URLS.login, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({email,password}) });
    const data = await r.json();
    if (data.ok) window.location.href = data.redirect;
    else if (errEl) errEl.textContent = data.error || 'შეცდომა.';
  } catch { if (errEl) errEl.textContent = 'კავშირის შეცდომა.'; }
}
async function submitRegister() {
  const username = document.getElementById('regUsername')?.value;
  const email    = document.getElementById('regEmail')?.value;
  const password = document.getElementById('regPassword')?.value;
  const errEl    = document.getElementById('registerError');
  if (!username || !email || !password) { if (errEl) errEl.textContent = 'ყველა ველი სავალდებულოა.'; return; }
  try {
    const r    = await fetch(URLS.register, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({username,email,password}) });
    const data = await r.json();
    if (data.ok) window.location.href = data.redirect;
    else if (errEl) errEl.textContent = data.error || 'შეცდომა.';
  } catch { if (errEl) errEl.textContent = 'კავშირის შეცდომა.'; }
}

/* ── FLASH AUTO DISMISS ── */
setTimeout(() => {
  document.querySelectorAll('.flash').forEach(f => f.style.opacity = '0');
}, 4000);

