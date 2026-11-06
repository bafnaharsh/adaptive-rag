'use strict';
// Adaptive RAG chat UI. Plain DOM, no build step. Every model/web-derived string reaches the page as a text node
// (via h()) or through DOMPurify (answer markdown); URLs pass safeUrl() before becoming links.

const $ = (id) => document.getElementById(id);
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
const mobileNav = matchMedia('(max-width: 860px)');

const ICONS = {
  search: '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
  globe: '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3a14 14 0 0 1 0 18 14 14 0 0 1 0-18"/>',
  layers: '<path d="m12 3 9 4.5-9 4.5-9-4.5z"/><path d="m3 16.5 9 4.5 9-4.5"/><path d="m3 12 9 4.5 9-4.5"/>',
  db: '<ellipse cx="12" cy="5.5" rx="8" ry="2.5"/><path d="M4 5.5v13c0 1.4 3.6 2.5 8 2.5s8-1.1 8-2.5v-13"/><path d="M4 12c0 1.4 3.6 2.5 8 2.5s8-1.1 8-2.5"/>',
  bulb: '<path d="M15 14c.2-1 .7-1.7 1.5-2.5A5.9 5.9 0 0 0 18 8 6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/>',
  split: '<path d="M16 3h5v5"/><path d="M8 3H3v5"/><path d="M12 22v-8.3a4 4 0 0 0-1.2-2.9L3 3"/><path d="m15 9 6-6"/>',
  pen: '<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/>',
  shield: '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
  check: '<path d="M20 6 9 17l-5-5"/>',
  alert: '<path d="m21.7 18-8-14a2 2 0 0 0-3.4 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.7-3z"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
  chevron: '<path d="m9 6 6 6-6 6"/>',
  file: '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M16 13H8"/><path d="M16 17H8"/>',
  external: '<path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>',
  refresh: '<path d="M3 12a9 9 0 0 1 15.5-6.2L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-15.5 6.2L3 16"/><path d="M8 16H3v5"/>',
  arrowUp: '<path d="M12 19V5"/><path d="m5 12 7-7 7 7"/>',
  dot: '<circle cx="12" cy="12" r="3"/>',
};

const TIERS = [
  { key: 'knowledge', name: 'Knowledge', icon: 'bulb', label: 'Tier 0 · knowledge' },
  { key: 'rag', name: 'RAG', icon: 'db', label: 'Tier 1 · RAG' },
  { key: 'hybrid', name: 'Hybrid', icon: 'layers', label: 'Tier 2 · hybrid' },
  { key: 'web', name: 'Web', icon: 'globe', label: 'Tier 3 · web' },
];
const TIER = Object.fromEntries(TIERS.map((t) => [t.key, t]));
const STATE_TEXT = { idle: 'not reached', active: 'in progress', passed: 'not enough evidence, escalated', reached: 'answered here', skipped: 'skipped' };
const WRITE = 'Writing a grounded answer';

// ---------- helpers ----------

/** Element builder: strings become text nodes, never HTML. */
function h(tag, props, ...kids) {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(props || {})) {
    if (v == null || v === false) continue;
    if (k === 'class') el.className = v;
    else if (k.startsWith('on')) el.addEventListener(k.slice(2), v);
    else el.setAttribute(k, v === true ? '' : String(v));
  }
  for (const kid of kids.flat(Infinity)) {
    if (kid == null || kid === false || kid === '') continue;
    el.append(kid instanceof Node ? kid : String(kid));
  }
  return el;
}

/** Inline SVG from the fixed ICONS table above (trusted markup only). */
function icon(name, cls = '') {
  const t = document.createElement('template');
  t.innerHTML = `<svg class="i ${cls}" viewBox="0 0 24 24" aria-hidden="true" focusable="false">${ICONS[name] || ''}</svg>`;
  return t.content.firstChild;
}

/** http(s) URL object, or null: blocks javascript:, data: and other schemes from untrusted links. */
function safeUrl(u) {
  if (!u) return null; // new URL('', base) would resolve to this page
  try {
    const url = new URL(String(u || ''), location.href);
    return url.protocol === 'http:' || url.protocol === 'https:' ? url : null;
  } catch { return null; }
}
const domain = (u) => (safeUrl(u)?.hostname || String(u || '')).replace(/^www\./, '');
const secs = (s) => `${Number(s || 0).toFixed(1)} s`;
const plural = (n, w) => `${n} ${w}${n === 1 ? '' : 's'}`;
const uuid = () => crypto.randomUUID?.()
  // randomUUID needs a secure context; plain-http LAN hosts get this RFC 4122 v4 fallback
  ?? '10000000-1000-4000-8000-100000000000'.replace(/[018]/g, (c) => (c ^ (crypto.getRandomValues(new Uint8Array(1))[0] & (15 >> (c / 4)))).toString(16));

function linkOut(url, ...kids) {
  return h('a', { href: url.href, target: '_blank', rel: 'noopener noreferrer', title: url.href }, ...kids);
}

/** "file.pdf · p. 42" for documents, the URL's domain for web hits. */
function where(item) {
  if (item.url) return domain(item.url);
  return item.page ? `${item.source} · p. ${item.page}` : (item.source || item.label || '');
}

async function apiError(res) {
  let detail = '';
  try {
    const body = await res.json();
    detail = typeof body.detail === 'string' ? body.detail : Array.isArray(body.detail) ? body.detail.map((d) => d.msg).join('; ') : '';
  } catch { /* not JSON */ }
  if (res.status === 404 && !detail) return `The API endpoint ${new URL(res.url).pathname} was not found (404).`;
  return detail || `The API answered ${res.status} ${res.statusText}.`;
}

async function getJSON(url, opts) {
  const res = await fetch(url, opts);
  if (!res.ok) throw new Error(await apiError(res));
  return res.json();
}

function friendly(err) {
  return err instanceof TypeError ? 'Could not reach the API. Check that the server is running, then retry.' : (err?.message || String(err));
}

function announce(text) { $('announcer').textContent = text; }

/** Run fn, keeping the thread pinned to the bottom if the reader was already there. */
function follow(fn) {
  const sc = $('scroller');
  const pinned = sc.scrollHeight - sc.scrollTop - sc.clientHeight < 160;
  fn();
  if (pinned) sc.scrollTop = sc.scrollHeight;
}

// ---------- server-sent events over fetch (EventSource cannot POST) ----------

function parseEvent(block) {
  let event = 'message';
  const data = [];
  for (const line of block.split(/\r?\n/)) {
    if (!line || line.startsWith(':')) continue; // comments / keep-alive pings
    const i = line.indexOf(':');
    const field = i < 0 ? line : line.slice(0, i);
    let value = i < 0 ? '' : line.slice(i + 1);
    if (value.startsWith(' ')) value = value.slice(1);
    if (field === 'event') event = value;
    else if (field === 'data') data.push(value);
  }
  if (!data.length) return null;
  try { return { event, data: JSON.parse(data.join('\n')) }; } catch {
    console.warn('Skipping a malformed stream event', block);
    return null;
  }
}

async function* readEvents(body) {
  const reader = body.pipeThrough(new TextDecoderStream()).getReader();
  let buf = '';
  try {
    for (;;) {
      const { value, done } = await reader.read();
      if (done) break;
      buf += value;
      for (let m; (m = /\r?\n\r?\n/.exec(buf));) { // a blank line ends an event (LF or CRLF servers)
        const ev = parseEvent(buf.slice(0, m.index));
        buf = buf.slice(m.index + m[0].length);
        if (ev) yield ev;
      }
    }
    const last = parseEvent(buf);
    if (last) yield last;
  } finally {
    reader.cancel().catch(() => {});
  }
}

// ---------- markdown + citations ----------

const PURIFY = {
  FORBID_TAGS: ['style', 'img', 'svg', 'math', 'form', 'input', 'button', 'textarea', 'select', 'iframe', 'video', 'audio'],
  FORBID_ATTR: ['style', 'class', 'id'],
  RETURN_DOM_FRAGMENT: true,
};

const escapeHtml = (s) => String(s).replace(/[&<>"']/g, (c) => `&#${c.charCodeAt(0)};`);
let markedReady = false;

function markdown(md) {
  if (window.marked && window.DOMPurify) {
    if (!markedReady) {
      // answers are markdown: show raw HTML from the model as text (DOMPurify stays as the second layer)
      marked.use({ renderer: { html: (x) => escapeHtml(typeof x === 'string' ? x : x?.text ?? '') } });
      markedReady = true;
    }
    return DOMPurify.sanitize(marked.parse(String(md || ''), { gfm: true, breaks: false }), PURIFY);
  }
  // CDN unreachable: plain paragraphs, still readable
  return h('div', {}, String(md || '').split(/\n{2,}/).map((p) => h('p', {}, p)));
}

const CITE_RE = /\[(\d+(?:\s*,\s*\d+)*)\]/g;

/** Replace [n] / [1, 2] markers in rendered text (not code or links) with citation buttons. */
function linkCitations(root, makeChip) {
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
    acceptNode: (n) => (n.parentElement.closest('code, pre, a') ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT),
  });
  const nodes = [];
  for (let n; (n = walker.nextNode());) if (n.nodeValue.includes('[')) nodes.push(n);
  for (const node of nodes) {
    const text = node.nodeValue;
    const parts = [];
    let last = 0;
    for (const m of text.matchAll(CITE_RE)) {
      const before = text.slice(last, m.index);
      const word = before.match(/\S*\s*$/)[0]; // keep the chip on the same line as the word it supports
      parts.push(before.slice(0, before.length - word.length), h('span', { class: 'nobr' }, word, m[1].split(',').map((n) => makeChip(Number(n)))));
      last = m.index + m[0].length;
    }
    if (!last) continue;
    parts.push(text.slice(last));
    node.replaceWith(...parts.filter((p) => p !== ''));
  }
}

// ---------- citation popover (one shared tooltip) ----------

const pop = $('cite-pop');

function citeSource(c) {
  const url = safeUrl(c.url);
  if (url) return [icon('globe'), h('span', { class: 'pop-src' }, c.title || domain(url), h('span', { class: 'muted' }, ` · ${domain(url)}`))];
  return [icon('file'), h('span', { class: 'pop-src' }, where(c))];
}

function statusBadge(c) {
  return c.verified
    ? h('span', { class: 'status status--ok' }, icon('check'), 'Verified')
    : h('span', { class: 'status status--warn' }, icon('alert'), 'Unverified');
}

function showPop(chip, n, c) {
  pop.replaceChildren(...(c
    ? [h('div', { class: 'pop-head' }, h('span', { class: 'num' }, n), ...citeSource(c), statusBadge(c)),
      h('blockquote', {}, `“${c.quote || ''}”`),
      !c.verified && c.reason && h('p', { class: 'pop-reason' }, icon('alert'), c.reason)]
    : [h('p', { class: 'pop-reason' }, icon('alert'), `The answer cites [${n}], but no citation ${n} was returned.`)]).filter(Boolean));
  pop.hidden = false;
  const r = chip.getBoundingClientRect();
  const left = Math.max(8, Math.min(r.left + r.width / 2 - pop.offsetWidth / 2, innerWidth - pop.offsetWidth - 8));
  const below = r.bottom + 8 + pop.offsetHeight <= innerHeight - 8;
  pop.style.left = `${left}px`;
  pop.style.top = `${below ? r.bottom + 8 : Math.max(8, r.top - pop.offsetHeight - 8)}px`;
}
const hidePop = () => { pop.hidden = true; };
addEventListener('keydown', (e) => { if (e.key === 'Escape') hidePop(); });
addEventListener('resize', hidePop);

// ---------- research block components ----------

function Ladder() {
  const pills = {};
  const conns = [];
  const el = h('div', { class: 'ladder', role: 'list', 'aria-label': 'Escalation ladder' });
  TIERS.forEach((t, i) => {
    if (i) { const c = h('span', { class: 'conn', 'aria-hidden': 'true' }); conns.push(c); el.append(c); }
    const sr = h('span', { class: 'sr-only' }, `: ${STATE_TEXT.idle}`);
    const li = h('div', { class: 'tier', role: 'listitem', 'data-state': 'idle' }, icon(t.icon), h('span', {}, t.name), sr);
    pills[t.key] = { li, sr };
    el.append(li);
  });
  const LIT = ['active', 'passed', 'reached'];
  const get = (k) => pills[k].li.dataset.state;
  function set(k, s) {
    if (!pills[k] || get(k) === s) return;
    pills[k].li.dataset.state = s;
    pills[k].sr.textContent = `: ${STATE_TEXT[s]}`;
    TIERS.slice(1).forEach((t, i) => conns[i].classList.toggle('on', LIT.includes(get(TIERS[i].key)) && LIT.includes(get(t.key))));
  }
  return {
    el,
    step(ev) {
      if (ev.node === 'plan') {
        const target = { knowledge: 'knowledge', documents: 'rag', web: 'web' }[ev.route];
        if (!target) return;
        for (const t of TIERS) set(t.key, t.key === target ? 'active' : TIERS.indexOf(t) < TIERS.indexOf(TIER[target]) ? 'skipped' : 'idle');
      } else if (ev.node === 'rag' || ev.node === 'hybrid') {
        const next = ev.node === 'rag' ? 'hybrid' : 'web';
        if (ev.verdict === 'sufficient') {
          set(ev.node, 'reached');
          for (const t of TIERS.slice(TIERS.indexOf(TIER[ev.node]) + 1)) set(t.key, 'skipped');
        } else { set(ev.node, 'passed'); set(next, 'active'); }
      } else if (ev.node === 'web') set('web', 'reached');
    },
    final(tier) {
      for (const t of TIERS) {
        const s = get(t.key);
        if (t.key === tier) set(t.key, 'reached');
        else if (s === 'reached' || s === 'active') set(t.key, TIERS.indexOf(t) < TIERS.indexOf(TIER[tier] || TIER.web) ? 'passed' : 'skipped');
        else if (s === 'idle') set(t.key, 'skipped');
      }
    },
    stop() { for (const t of TIERS) if (get(t.key) === 'active') set(t.key, 'idle'); },
  };
}

/** What the pipeline is doing now, inferred from the last finished step (steps arrive only when a node ends). */
function nextLabel(ev) {
  if (!ev) return 'Planning';
  switch (ev.node) {
    case 'plan': return { documents: 'Searching documents (Tier 1 · RAG)', web: 'Searching the web (Tier 3)', knowledge: 'Answering from model knowledge' }[ev.route] || 'Working';
    case 'rag': return ev.verdict === 'sufficient' ? WRITE : 'Hybrid search: BM25 + dense + rerank';
    case 'hybrid': return ev.verdict === 'sufficient' ? WRITE : 'Searching the web (Tier 3)';
    case 'web': return WRITE;
    case 'generate': return 'Verifying citations';
    case 'verify': return ev.retry ? 'Rewriting with verification feedback' : 'Finishing up';
    default: return 'Working';
  }
}

function card(ev, iconName, title, sub, ...body) {
  return h('li', { class: `step step--${ev.node}` },
    h('span', { class: 'rail-dot' }, icon(iconName)),
    h('div', { class: 'card' },
      h('div', { class: 'card-head' },
        h('span', { class: 'card-title' }, title),
        sub && h('span', { class: 'card-sub' }, sub),
        h('span', { class: 't mono', title: 'Seconds since the question was sent' }, `+${secs(ev.t)}`)),
      ...body));
}

const block = (label, ...kids) => h('div', { class: 'block' }, h('div', { class: 'block-label' }, label), ...kids);
const chips = (items, iconName) => h('ul', { class: 'chips' }, items.map((q) => h('li', { class: 'chip' }, iconName && icon(iconName), q)));

function hitList(hits) {
  const scores = hits.map((x) => Number(x.score) || 0);
  const max = Math.max(...scores);
  const min = Math.min(...scores);
  return h('ul', { class: 'hits' }, hits.map((x, i) => {
    const url = safeUrl(x.url);
    const fill = h('span', { class: 'bar-fill' });
    // tier 1 scores are cosines (0..1, shown as is); rerank logits are only comparable within one list: scale to it
    const w = min >= 0 && max <= 1 ? scores[i] : max > min ? 0.12 + 0.88 * (scores[i] - min) / (max - min) : 1;
    fill.style.setProperty('--w', w.toFixed(3));
    return h('li', {}, h('details', { class: 'hit' },
      h('summary', {},
        icon(url ? 'globe' : 'file'),
        h('span', { class: 'hit-label', title: x.label || where(x) }, where(x)),
        h('span', { class: 'bar', 'aria-hidden': 'true' }, fill),
        h('span', { class: 'score mono', title: 'Retrieval score (relative within this list)' }, scores[i].toFixed(2))),
      h('p', { class: 'snippet' }, x.snippet || '(no preview)'),
      url && h('p', { class: 'hit-link' }, linkOut(url, 'Open page', icon('external')))));
  }));
}

function verdictBadge(v) {
  if (v === 'sufficient') return h('span', { class: 'badge badge--ok' }, icon('check'), 'Sufficient');
  if (v === 'insufficient') return h('span', { class: 'badge badge--warn' }, icon('arrowUp'), 'Not enough · escalate');
  return h('span', { class: 'badge' }, v || 'No verdict');
}

const sameText = (a, b) => String(a || '').trim().toLowerCase() === String(b || '').trim().toLowerCase();

const STEPS = {
  plan(ev, query) {
    const route = { knowledge: 'Answer from own knowledge', documents: 'Search the documents', web: 'Search the web' }[ev.route] || ev.route;
    return card(ev, 'split', 'Plan', 'route the question',
      h('div', { class: 'row' }, h('span', { class: 'chip chip--accent' }, icon(ev.route === 'web' ? 'globe' : ev.route === 'knowledge' ? 'bulb' : 'db'), route)),
      ev.reasoning && h('p', { class: 'reason' }, ev.reasoning),
      ev.standalone && !sameText(ev.standalone, query) && block('Rewritten as a standalone question', h('p', { class: 'standalone' }, ev.standalone)),
      ev.note && h('p', { class: 'note' }, ev.note));
  },
  rag(ev) {
    const hybrid = ev.node === 'hybrid';
    const hits = ev.chunks || [];
    return card(ev, hybrid ? 'layers' : 'db', hybrid ? 'Tier 2 · Hybrid search' : 'Tier 1 · RAG', hybrid ? 'BM25 + dense · fusion · rerank' : 'dense embedding search',
      ev.queries?.length > 0 && block(hybrid ? 'Queries' : 'Query', chips(ev.queries, 'search')),
      block(h('span', {}, `Retrieved ${plural(hits.length, 'chunk')}`, hybrid && ev.new != null && h('span', { class: 'badge badge--soft' }, `${ev.new} new`)),
        hits.length ? hitList(hits) : h('p', { class: 'muted' }, 'Nothing relevant above the threshold.')),
      block('Judge', h('div', { class: 'judge' }, verdictBadge(ev.verdict), ev.reasoning && h('p', { class: 'reason' }, ev.reasoning)),
        ev.verdict !== 'sufficient' && ev.missing && h('p', { class: 'missing' }, h('strong', {}, 'Missing: '), ev.missing),
        ev.verdict !== 'sufficient' && ev.next_queries?.length > 0 && h('div', { class: 'next' }, h('span', { class: 'muted' }, 'Next queries'), chips(ev.next_queries, 'search'))));
  },
  web(ev) {
    const hits = ev.chunks || [];
    const pages = [...new Map(hits.map((x) => [x.url, safeUrl(x.url)]).filter(([, u]) => u)).values()];
    return card(ev, 'globe', 'Tier 3 · Web search', `${plural(pages.length, 'page')} read`,
      ev.query && block('Query', chips([ev.query], 'search')),
      pages.length
        ? block('Sources found', h('ul', { class: 'chips' }, pages.map((u) => h('li', {}, linkOut(u, icon('globe'), domain(u), icon('external', 'i--xs'))))))
        : h('p', { class: 'muted' }, 'No usable pages found.'),
      hits.length > 0 && h('details', { class: 'more' }, h('summary', {}, icon('chevron'), `Show ${plural(hits.length, 'passage')}`), hitList(hits)));
  },
  generate(ev) {
    const rewrite = ev.retry || ev.attempt > 1;
    return card(ev, 'pen', rewrite ? 'Rewrote the answer' : 'Drafted a grounded answer', ev.attempt ? `attempt ${ev.attempt}` : '',
      h('p', { class: 'reason' }, `${plural(ev.citations ?? 0, 'citation')}, each with a verbatim quote from its source.`));
  },
  verify(ev) {
    const ok = ev.total ? ev.verified === ev.total : true;
    const meter = h('span', { class: 'bar bar--wide', 'aria-hidden': 'true' }, h('span', { class: `bar-fill${ok ? ' ok' : ' warn'}` }));
    meter.firstChild.style.setProperty('--w', ev.total ? String(ev.verified / ev.total) : '1');
    return card(ev, 'shield', 'Citation check', 'deterministic quote match',
      h('div', { class: 'verify' },
        h('span', { class: `badge ${ok ? 'badge--ok' : 'badge--warn'}` }, icon(ok ? 'check' : 'alert'), `${ev.verified}/${ev.total} verified`), meter),
      ev.problems?.length > 0 && h('ul', { class: 'problems' }, ev.problems.map((p) => h('li', {}, icon('alert'), p))),
      ev.retry && h('p', { class: 'note' }, 'Regenerating once with these problems as feedback.'));
  },
};
STEPS.hybrid = STEPS.rag;

function renderStep(ev, query) {
  const make = STEPS[ev.node];
  return make ? make(ev, query) : card(ev, 'dot', String(ev.node || 'Step'), '');
}

function errorBox(message, retry) {
  return h('div', { class: 'error', role: 'alert' }, icon('alert'),
    h('div', { class: 'error-body' }, h('strong', {}, 'This answer could not be completed'), h('p', {}, message)),
    retry && h('button', { class: 'btn btn--sm', type: 'button', onclick: retry }, icon('refresh'), 'Retry'));
}

/** Final answer: markdown, citation chips, badge row, source cards. */
function renderAnswer(res, turnId) {
  const cites = new Map((res.citations || []).map((c) => [Number(c.n), c]));
  const srcId = (n) => `src-${turnId}-${n}`;
  const prose = h('div', { class: 'prose' }, markdown(res.answer));
  linkCitations(prose, (n) => {
    const c = cites.get(n);
    const chip = h('button', {
      type: 'button',
      class: `cite${!c ? ' cite--missing' : c.verified ? '' : ' cite--warn'}`,
      'aria-label': `Citation ${n}${c ? `, ${c.verified ? 'verified' : 'not verified'}, ${where(c)}` : ', missing'}`,
      'aria-describedby': 'cite-pop',
    }, String(n));
    chip.addEventListener('mouseenter', () => showPop(chip, n, c));
    chip.addEventListener('focus', () => showPop(chip, n, c));
    chip.addEventListener('mouseleave', hidePop);
    chip.addEventListener('blur', hidePop);
    chip.addEventListener('click', () => {
      const card = document.getElementById(srcId(n));
      if (!card) return;
      hidePop();
      card.scrollIntoView({ behavior: reducedMotion.matches ? 'auto' : 'smooth', block: 'center' });
      card.focus({ preventScroll: true });
      card.classList.remove('flash');
      void card.offsetWidth; // restart the highlight animation
      card.classList.add('flash');
    });
    return chip;
  });

  const all = res.citations || [];
  const bad = all.filter((c) => !c.verified).length;
  const knowledge = res.tier === 'knowledge';
  const t = TIER[res.tier];
  const badges = h('div', { class: 'badges' },
    h('span', { class: 'badge badge--tier' }, icon(t?.icon || 'dot'), t?.label || res.tier || 'unknown tier'),
    all.length > 0 && !bad && res.verified !== false && h('span', { class: 'badge badge--ok' }, icon('check'), 'All citations verified'),
    bad > 0 && h('span', { class: 'badge badge--warn' }, icon('alert'), `${bad} of ${all.length} citations unverified`),
    knowledge && !all.length && h('span', { class: 'badge' }, 'Not verified'),
    res.seconds != null && h('span', { class: 'badge badge--plain mono' }, secs(res.seconds)));

  return h('div', { class: 'answer' },
    h('h3', { class: 'label-h' }, 'Answer'),
    knowledge && h('div', { class: 'callout' }, icon('bulb'),
      h('p', {}, h('strong', {}, 'Model knowledge — not verified against sources. '), 'The planner judged this a general question, so no documents or web pages were searched.')),
    prose,
    badges,
    all.length > 0 && h('section', { class: 'sources', 'aria-label': 'Sources' },
      h('h3', { class: 'label-h' }, 'Sources ', h('span', { class: 'count' }, all.length)),
      h('ol', {}, all.map((c) => {
        const url = safeUrl(c.url);
        const title = url
          ? linkOut(url, h('span', { class: 'src-name' }, c.title || domain(url)), icon('external', 'i--xs'))
          : h('span', { class: 'src-name', title: c.title || '' }, c.source || c.label || c.source_id);
        return h('li', { class: `source${c.verified ? '' : ' source--warn'}`, id: srcId(c.n), tabindex: '-1' },
          h('div', { class: 'src-head' },
            h('span', { class: 'num' }, c.n),
            icon(url ? 'globe' : 'file'),
            h('span', { class: 'src-title' }, title, h('span', { class: 'src-meta' }, url ? domain(url) : c.page ? `p. ${c.page}` : '')),
            statusBadge(c)),
          h('blockquote', { class: 'quote' }, `“${c.quote || ''}”`),
          !c.verified && c.reason && h('p', { class: 'src-reason' }, icon('alert'), c.reason));
      }))));
}

// ---------- a chat turn ----------

let turnSeq = 0;

function Turn(query, retry) {
  const id = ++turnSeq;
  const ladder = Ladder();
  const label = h('span', { class: 'working-label' }, 'Planning');
  const clock = h('span', { class: 'working-time mono', 'aria-hidden': 'true' }, '0.0 s');
  const working = h('li', { class: 'step step--working' },
    h('span', { class: 'rail-dot' }, h('span', { class: 'spinner' })),
    h('div', { class: 'working' }, label, clock));
  const steps = h('ol', { class: 'steps' }, working);
  const summary = h('span', { class: 'summary-text' }, 'Researching…');
  const timeline = h('details', { class: 'timeline', open: true },
    h('summary', {}, icon('chevron', 'chev'), summary), steps);
  const body = h('div', { class: 'turn-body' });
  const el = h('article', { class: 'turn', 'aria-labelledby': `q-${id}`, 'aria-busy': 'true' },
    h('h2', { class: 'q', id: `q-${id}` }, query),
    h('section', { class: 'research', 'aria-label': 'Research steps' }, ladder.el, timeline),
    body);

  const t0 = performance.now();
  const timer = setInterval(() => { clock.textContent = secs((performance.now() - t0) / 1000); }, 100);
  let count = 0;
  let lastT = 0;
  announce('Planning');

  function settle() {
    clearInterval(timer);
    working.remove();
    el.removeAttribute('aria-busy');
  }

  return {
    el,
    step(ev) {
      count++;
      lastT = Number(ev.t) || lastT;
      follow(() => {
        steps.insertBefore(renderStep(ev, query), working);
        ladder.step(ev);
        label.textContent = nextLabel(ev);
        summary.textContent = `Researching… · ${plural(count, 'step')}`;
      });
      announce(label.textContent);
    },
    final(res) {
      settle();
      const failed = (res.trace || []).some((s) => String(s).startsWith('Error:'));
      if (failed) return this.fail(res.answer || 'The pipeline failed.');
      if (!count && res.trace?.length) { // backend sent no steps: show its text trace instead
        steps.append(h('li', { class: 'step' }, h('span', { class: 'rail-dot' }, icon('dot')),
          h('div', { class: 'card' }, h('ul', { class: 'trace' }, res.trace.map((s) => h('li', {}, s))))));
      }
      ladder.final(res.tier);
      const tier = TIER[res.tier]?.label || res.tier;
      summary.textContent = `${plural(count, 'step')} · ${secs(res.seconds ?? lastT)} · ${tier}`;
      timeline.open = false;
      const answer = renderAnswer(res, id);
      const sc = $('scroller');
      const pinned = sc.scrollHeight - sc.scrollTop - sc.clientHeight < 160;
      body.append(answer);
      if (pinned) el.scrollIntoView({ behavior: reducedMotion.matches ? 'auto' : 'smooth', block: 'start' });
      announce(`Answer ready. ${tier}. ${res.verified ? 'All citations verified.' : res.tier === 'knowledge' ? 'From model knowledge, not verified.' : 'Some citations unverified.'}`);
    },
    fail(message) {
      settle();
      ladder.stop();
      summary.textContent = count ? `${plural(count, 'step')} · stopped` : 'No steps completed';
      follow(() => body.append(errorBox(message, retry)));
      announce(`Error: ${message}`);
    },
  };
}

// ---------- chat ----------

const state = { session: uuid(), ctrl: null };
const thread = $('thread');
const input = $('q');

function setBusy(busy) {
  input.disabled = busy;
  $('composer').classList.toggle('busy', busy);
  $('send').setAttribute('aria-label', busy ? 'Stop answering' : 'Send question');
  for (const b of document.querySelectorAll('.example')) b.disabled = busy;
}

async function ask(raw) {
  const query = String(raw || '').trim();
  if (!query || state.ctrl) return;
  $('empty').hidden = true;
  const turn = Turn(query, () => { if (state.ctrl) return; turn.el.remove(); ask(query); });
  thread.append(turn.el);
  $('scroller').scrollTop = $('scroller').scrollHeight;
  const ctrl = state.ctrl = new AbortController();
  setBusy(true);
  let ended = false;
  try {
    const res = await fetch('/rag/query/stream', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'text/event-stream' },
      body: JSON.stringify({ query, session_id: state.session }),
      signal: ctrl.signal,
    });
    if (!res.ok || !res.body) throw new Error(await apiError(res));
    for await (const { event, data } of readEvents(res.body)) {
      if (event === 'step') turn.step(data);
      else if (event === 'final') { ended = true; turn.final(data); break; }
      else if (event === 'error') { ended = true; turn.fail(data?.message || 'The server reported an error.'); break; }
    }
    if (!ended) turn.fail('The connection closed before the answer was finished.');
  } catch (err) {
    if (!ended && turn.el.isConnected) turn.fail(ctrl.signal.aborted ? 'You stopped this answer.' : friendly(err));
  } finally {
    if (state.ctrl === ctrl) {
      state.ctrl = null;
      setBusy(false);
      if (!document.activeElement || document.activeElement === document.body || document.activeElement.id === 'send') input.focus();
    }
  }
}

function newChat() {
  state.ctrl?.abort();
  state.ctrl = null;
  setBusy(false);
  state.session = uuid();
  hidePop();
  thread.querySelectorAll('.turn').forEach((t) => t.remove());
  $('empty').hidden = false;
  input.value = '';
  autosize();
  setNav(false);
  if (!mobileNav.matches) input.focus(); // no surprise keyboard on phones
  announce('New chat started');
}

function autosize() {
  input.style.height = 'auto';
  input.style.height = `${Math.min(input.scrollHeight, 200)}px`;
}

$('composer').addEventListener('submit', (e) => {
  e.preventDefault();
  if (state.ctrl) { state.ctrl.abort(); return; }
  const q = input.value;
  if (!q.trim()) return;
  input.value = '';
  autosize();
  ask(q);
});
input.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey && !e.isComposing) { e.preventDefault(); $('composer').requestSubmit(); }
});
input.addEventListener('input', autosize);
$('examples').addEventListener('click', (e) => { const b = e.target.closest('.example'); if (b) ask(b.textContent); });
$('new-chat').addEventListener('click', newChat);
$('new-chat-m').addEventListener('click', newChat);
$('scroller').addEventListener('scroll', hidePop, { passive: true });

// ---------- sidebar: backend info, documents, upload ----------

function setNav(open) {
  const drawer = mobileNav.matches;
  document.body.classList.toggle('nav-open', drawer && open);
  $('sidebar').inert = drawer && !open;
  $('scrim').hidden = !(drawer && open);
  $('nav-open').setAttribute('aria-expanded', String(drawer && open));
  if (drawer && open) $('new-chat').focus();
}
$('nav-open').addEventListener('click', () => setNav(true));
$('nav-close').addEventListener('click', () => { setNav(false); $('nav-open').focus(); });
$('scrim').addEventListener('click', () => setNav(false));
addEventListener('keydown', (e) => { if (e.key === 'Escape' && document.body.classList.contains('nav-open')) { setNav(false); $('nav-open').focus(); } });
mobileNav.addEventListener('change', () => setNav(false));
setNav(false);

const WEB_NAMES = { duckduckgo: 'DuckDuckGo', tavily: 'Tavily' };

async function loadInfo() {
  const env = $('env');
  try {
    const info = await getJSON('/rag/info');
    env.replaceChildren(
      h('li', { class: 'env-chip', title: 'Language model backend' }, h('span', { class: 'dot dot--ok' }), h('span', { class: 'muted' }, 'LLM'), info.llm || '?'),
      h('li', { class: 'env-chip', title: 'Web search provider (Tier 3)' }, h('span', { class: 'dot dot--ok' }), h('span', { class: 'muted' }, 'Web'), WEB_NAMES[info.web] || info.web || '?'));
  } catch (err) {
    env.replaceChildren(h('li', { class: 'env-chip env-chip--err' }, h('span', { class: 'dot dot--err' }), 'API offline',
      h('button', { class: 'link-btn', type: 'button', onclick: () => { loadInfo(); loadDocs(); } }, 'Retry')));
    console.warn('GET /rag/info failed:', friendly(err));
  }
}

async function loadDocs() {
  const list = $('docs');
  try {
    const docs = await getJSON('/rag/documents');
    $('docs-count').textContent = docs.length ? String(docs.length) : '';
    list.replaceChildren(...(docs.length ? docs.map((d) => h('li', { class: 'doc', title: d.description || d.name },
      icon('file'),
      h('div', { class: 'doc-text' },
        h('span', { class: 'doc-name' }, d.name),
        h('span', { class: 'doc-meta' }, [d.pages && plural(d.pages, 'page'), `${Number(d.chunks || 0).toLocaleString()} chunks`].filter(Boolean).join(' · ')))))
      : [h('li', { class: 'docs-empty muted' }, 'No documents yet. Add a PDF below and questions about it will be answered from its pages.')]));
  } catch (err) {
    list.replaceChildren(h('li', { class: 'docs-empty' }, h('span', { class: 'muted' }, `Could not load documents. ${friendly(err)} `),
      h('button', { class: 'link-btn', type: 'button', onclick: loadDocs }, 'Retry')));
  }
}

const upload = { file: null, timer: null };
const fileInput = $('file');
const drop = $('drop');
const ALLOWED = /\.(pdf|txt|md)$/i;

function pickFile(file) {
  const status = $('upload-status');
  status.replaceChildren();
  if (file && !ALLOWED.test(file.name)) {
    status.replaceChildren(h('p', { class: 'msg msg--err' }, icon('alert'), `${file.name} is not a PDF, TXT or MD file.`));
    file = null;
  }
  upload.file = file || null;
  drop.classList.toggle('has-file', !!upload.file);
  $('drop-title').textContent = upload.file ? upload.file.name : 'Drop a PDF, TXT or MD';
  $('drop-sub').replaceChildren(...(upload.file
    ? [`${(upload.file.size / 1048576).toFixed(1)} MB · `, h('u', {}, 'change')]
    : ['or ', h('u', {}, 'browse files')]));
}

fileInput.addEventListener('change', () => pickFile(fileInput.files[0]));
drop.addEventListener('dragover', (e) => { e.preventDefault(); drop.classList.add('over'); });
drop.addEventListener('dragleave', () => drop.classList.remove('over'));
drop.addEventListener('drop', (e) => { e.preventDefault(); drop.classList.remove('over'); pickFile(e.dataTransfer.files[0]); });
// a file dropped outside the zone must not navigate away from the chat
addEventListener('dragover', (e) => e.preventDefault());
addEventListener('drop', (e) => e.preventDefault());

$('upload').addEventListener('submit', async (e) => {
  e.preventDefault();
  const file = upload.file;
  const status = $('upload-status');
  if (upload.timer) return;
  if (!file) {
    status.replaceChildren(h('p', { class: 'msg msg--err' }, icon('alert'), 'Choose or drop a PDF, TXT or MD file first.'));
    return;
  }
  const desc = $('desc').value.trim();
  if (!/^[\x20-\x7e\xa0-\xff]*$/.test(desc)) { // HTTP header values must be Latin-1
    status.replaceChildren(h('p', { class: 'msg msg--err' }, icon('alert'), 'The description can only use Latin characters (it is sent as a header).'));
    return;
  }
  const clock = h('span', { class: 'mono' }, '0 s');
  status.replaceChildren(h('div', { class: 'indexing' },
    h('p', {}, h('span', { class: 'spinner' }), h('span', {}, `Indexing ${file.name}…`), clock),
    h('div', { class: 'progress', 'aria-hidden': 'true' }),
    h('p', { class: 'muted small' }, 'Reading pages, chunking and embedding. A 200-page PDF takes 1–2 minutes.')));
  const t0 = performance.now();
  upload.timer = setInterval(() => { clock.textContent = `${Math.round((performance.now() - t0) / 1000)} s`; }, 500);
  $('upload-btn').disabled = true;
  fileInput.disabled = true;
  const form = new FormData();
  form.append('file', file);
  try {
    const { document: doc } = await getJSON('/rag/documents/upload', { method: 'POST', body: form, headers: desc ? { 'X-Description': desc } : {} });
    const exists = doc.status === 'exists';
    $('desc').value = '';
    fileInput.value = '';
    pickFile(null); // clears the status line, so the result is written after it
    status.replaceChildren(h('p', { class: `msg ${exists ? '' : 'msg--ok'}` }, icon('check'),
      `${exists ? 'Already indexed' : 'Indexed'}: ${doc.name} · ${plural(doc.pages || 0, 'page')} · ${plural(doc.chunks || 0, 'chunk')}`));
    loadDocs();
  } catch (err) {
    status.replaceChildren(h('p', { class: 'msg msg--err' }, icon('alert'), friendly(err)));
  } finally {
    $('upload-btn').disabled = false;
    clearInterval(upload.timer);
    upload.timer = null;
    fileInput.disabled = false;
  }
});

if (window.DOMPurify) {
  DOMPurify.addHook('afterSanitizeAttributes', (node) => {
    if (node.tagName === 'A') { node.setAttribute('target', '_blank'); node.setAttribute('rel', 'noopener noreferrer'); }
  });
}

loadInfo();
loadDocs();
if (!mobileNav.matches) input.focus();
