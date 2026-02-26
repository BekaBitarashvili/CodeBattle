/* ═══════════════════════════════════════
   CodeQuest — home.js
   Landing page: countdown, terminal anim
═══════════════════════════════════════ */

/* ── OLYMPIAD COUNTDOWN ───────────────── */
(function () {
  const el = document.getElementById('countdown');
  if (!el) return;
  const target = new Date('2025-03-10T23:59:00');
  function tick() {
    let diff = (target - new Date()) / 1000;
    if (diff < 0) diff = 0;
    const d = Math.floor(diff / 86400);
    const h = Math.floor((diff % 86400) / 3600);
    const m = Math.floor((diff % 3600) / 60);
    const s = Math.floor(diff % 60);
    el.textContent = `⏱ ${pad(d)}:${pad(h)}:${pad(m)}:${pad(s)}`;
  }
  function pad(n) { return String(n).padStart(2, '0'); }
  tick();
  setInterval(tick, 1000);
})();
