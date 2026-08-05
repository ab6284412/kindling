"use strict";

async function post(url, body) {
  const resp = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!resp.ok) {
    let detail = "request failed";
    try {
      detail = (await resp.json()).detail || detail;
    } catch (_) {
      detail = detail + " (" + resp.status + ")";
    }
    throw new Error(detail);
  }
  return resp.json();
}

document.querySelectorAll(".toggle").forEach((box) => {
  box.addEventListener("change", async () => {
    try {
      await post("/api/toggle", {
        kind: box.dataset.kind,
        path: box.dataset.path,
      });
    } catch (e) {
      box.checked = !box.checked;
      alert(e.message);
    }
  });
});

document.querySelectorAll(".reveal").forEach((btn) => {
  btn.addEventListener("click", () => {
    const target = document.getElementById(btn.dataset.target);
    if (!target) return;
    target.hidden = !target.hidden;
    btn.textContent = target.hidden ? "Reveal self-check" : "Hide self-check";
  });
});

const saveBtn = document.querySelector(".save-note");
if (saveBtn) {
  saveBtn.addEventListener("click", async () => {
    const text = document.getElementById("note-text").value;
    try {
      await post("/api/note", { path: saveBtn.dataset.path, text });
      document.querySelector(".note-status").textContent = text.trim() ? "saved" : "note cleared";
    } catch (e) {
      alert(e.message);
    }
  });
}

const QUOTES = [
  { q: "The mind is not a vessel to be filled, but a fire to be kindled.", a: "Plutarch" },
  { q: "Live as if you were to die tomorrow. Learn as if you were to live forever.", a: "Mahatma Gandhi" },
  { q: "It always seems impossible until it’s done.", a: "Nelson Mandela" },
  { q: "We are what we repeatedly do. Excellence, then, is not an act, but a habit.", a: "Will Durant" },
  { q: "Do the hard jobs first. The easy jobs will take care of themselves.", a: "Dale Carnegie" },
  { q: "Learning never exhausts the mind.", a: "Leonardo da Vinci" },
];

const quoteText = document.getElementById("quote-text");
const quoteAttr = document.getElementById("quote-attr");
if (quoteText && quoteAttr) {
  const start = new Date(new Date().getFullYear(), 0, 0);
  const day = Math.floor((Date.now() - start) / 864e5);
  const pick = QUOTES[day % QUOTES.length];
  quoteText.textContent = "“" + pick.q + "”";
  quoteAttr.textContent = "— " + pick.a;
}

const fig = document.querySelector(".stat-hero .figure");
if (fig && fig.dataset.count !== undefined) {
  const target = parseInt(fig.dataset.count, 10);
  const num = fig.querySelector(".num");
  if (num && !Number.isNaN(target)) {
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduce || target === 0) {
      num.textContent = String(target);
    } else {
      const dur = 1400;
      const start = performance.now();
      function tick(now) {
        const t = Math.min((now - start) / dur, 1);
        const eased = 1 - Math.pow(1 - t, 3);
        num.textContent = String(Math.round(eased * target));
        if (t < 1) requestAnimationFrame(tick);
        else num.textContent = String(target);
      }
      requestAnimationFrame(tick);
    }
  }
}
