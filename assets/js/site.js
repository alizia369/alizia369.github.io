(function () {
  'use strict';
  var root = document.documentElement;

  // Theme switch, remembered per browser when storage is available
  var sw = document.getElementById('theme-switch');
  var mq = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : { matches: false };
  function current() { return root.getAttribute('data-theme') || (mq.matches ? 'dark' : 'light'); }
  function label() { if (sw) sw.textContent = current() === 'dark' ? 'Light theme' : 'Dark theme'; }
  try { var saved = localStorage.getItem('theme'); if (saved) root.setAttribute('data-theme', saved); } catch (e) {}
  label();
  if (sw) sw.addEventListener('click', function () {
    var next = current() === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('theme', next); } catch (e) {}
    label();
  });

  // Older news toggle
  var list = document.getElementById('news-list'), btn = document.getElementById('news-toggle');
  if (list && btn) btn.addEventListener('click', function () {
    var open = list.classList.toggle('open');
    btn.setAttribute('aria-expanded', open);
    btn.textContent = open ? 'Show less' : 'Show older news';
  });

  var reduceMotion = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  var canObserve = 'IntersectionObserver' in window;
  function onceVisible(el, threshold, fn) {
    if (!canObserve) { fn(); return; }
    var io = new IntersectionObserver(function (entries) {
      if (entries.some(function (e) { return e.isIntersecting; })) { io.disconnect(); fn(); }
    }, { threshold: threshold });
    io.observe(el);
  }

  // Stat tiles: count up from zero the first time they come into view
  Array.prototype.forEach.call(document.querySelectorAll('[data-count]'), function (el) {
    if (reduceMotion || !canObserve || !window.requestAnimationFrame) return;
    var to = parseFloat(el.dataset.count), dec = parseInt(el.dataset.decimals || '0', 10);
    var pre = el.dataset.prefix || '', suf = el.dataset.suffix || '', final = el.textContent;
    function show(v) { el.textContent = pre + v.toLocaleString('en-AU', { minimumFractionDigits: dec, maximumFractionDigits: dec }) + suf; }
    show(0);
    onceVisible(el, 0.6, function () {
      var t0 = null, dur = 1100;
      function step(t) {
        if (t0 === null) t0 = t;
        var k = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - k, 3);
        if (k < 1) { show(to * e); requestAnimationFrame(step); } else { el.textContent = final; }
      }
      requestAnimationFrame(step);
    });
  });

  // Home career strip: line and milestones reveal once when scrolled into view
  Array.prototype.forEach.call(document.querySelectorAll('[data-reveal]'), function (el) {
    if (reduceMotion || !canObserve) return;
    el.classList.add('pre');
    onceVisible(el, 0.4, function () { el.classList.remove('pre'); el.classList.add('in'); });
  });

  // Career pathway: connectors drawn between the cards, drawing themselves in once
  var flow = document.querySelector('[data-flow]');
  if (flow) {
    var NS = 'http://www.w3.org/2000/svg', lines = flow.querySelector('.flow-lines');
    var edges = JSON.parse(flow.getAttribute('data-edges'));
    // stage of each card along the longest path from the start, so arrows draw in career order
    var rank = {};
    edges.forEach(function (e) { rank[e[0]] = rank[e[0]] || 0; });
    for (var pass = 0; pass < edges.length; pass++) {
      edges.forEach(function (e) { rank[e[1]] = Math.max(rank[e[1]] || 0, rank[e[0]] + 1); });
    }
    function box(id, b) {
      var r = document.getElementById('cn-' + id).getBoundingClientRect();
      return { l: r.left - b.left, r: r.right - b.left, t: r.top - b.top, b: r.bottom - b.top,
               cx: (r.left + r.right) / 2 - b.left, cy: (r.top + r.bottom) / 2 - b.top };
    }
    function rounded(pts, rad) { // orthogonal polyline with rounded elbows
      var d = 'M' + pts[0][0] + ' ' + pts[0][1];
      for (var i = 1; i < pts.length - 1; i++) {
        var p = pts[i - 1], c = pts[i], n = pts[i + 1];
        var l1 = Math.hypot(c[0] - p[0], c[1] - p[1]), l2 = Math.hypot(n[0] - c[0], n[1] - c[1]);
        var r = Math.min(rad, l1 / 2, l2 / 2);
        d += ' L' + (c[0] - (c[0] - p[0]) / l1 * r) + ' ' + (c[1] - (c[1] - p[1]) / l1 * r) +
             ' Q' + c[0] + ' ' + c[1] + ' ' + (c[0] + (n[0] - c[0]) / l2 * r) + ' ' + (c[1] + (n[1] - c[1]) / l2 * r);
      }
      var z = pts[pts.length - 1];
      return d + ' L' + z[0] + ' ' + z[1];
    }
    function draw() {
      while (lines.firstChild) lines.removeChild(lines.firstChild);
      if (getComputedStyle(lines).display === 'none') return; // narrow layout: vertical timeline, no connectors
      var b = flow.getBoundingClientRect();
      lines.setAttribute('viewBox', '0 0 ' + b.width + ' ' + b.height);
      var b1 = flow.querySelector('.band1').getBoundingClientRect(), b2 = flow.querySelector('.band2').getBoundingClientRect();
      var chanY = (b1.bottom + b2.top) / 2 - b.top, busX = b2.left - b.left + 12, G = 2, H = 7;
      edges.forEach(function (e) {
        var s = box(e[0], b), t = box(e[1], b), pts;
        if (e[2] === 'wrap') pts = [[s.cx, s.b], [s.cx, chanY], [busX, chanY], [busX, t.cy], [t.l - G, t.cy]];
        else if (e[2] === 'up') pts = [[s.cx, s.t], [t.cx, t.b + G]];
        else if (Math.abs(s.cy - t.cy) < 1) pts = [[s.r, s.cy], [t.l - G, t.cy]];
        else { var mx = (s.r + t.l) / 2; pts = [[s.r, s.cy], [mx, s.cy], [mx, t.cy], [t.l - G, t.cy]]; }
        var path = document.createElementNS(NS, 'path');
        path.setAttribute('class', 'ln');
        path.setAttribute('d', rounded(pts, 9));
        path.style.transition = 'none'; // set its length without animating from the default offset
        lines.appendChild(path);
        var len = path.getTotalLength(), delay = rank[e[0]] * 0.28;
        path.style.setProperty('--len', len);
        path.style.setProperty('--d', delay + 's');
        getComputedStyle(path).strokeDashoffset; // apply the hidden starting state now
        path.style.transition = '';
        var a = pts[pts.length - 2], z = pts[pts.length - 1], ux = Math.sign(z[0] - a[0]), uy = Math.sign(z[1] - a[1]);
        var head = document.createElementNS(NS, 'path');
        head.setAttribute('class', 'hd');
        head.setAttribute('d', 'M' + z[0] + ' ' + z[1] + ' L' + (z[0] - ux * H - uy * H * 0.55) + ' ' + (z[1] - uy * H - ux * H * 0.55) +
                               ' L' + (z[0] - ux * H + uy * H * 0.55) + ' ' + (z[1] - uy * H + ux * H * 0.55) + 'Z');
        head.style.setProperty('--hd', (delay + 0.4) + 's');
        lines.appendChild(head);
      });
    }
    var drawnSize = '';
    function redrawIfResized() {
      var r = flow.getBoundingClientRect(), size = Math.round(r.width) + 'x' + Math.round(r.height);
      if (size !== drawnSize) { drawnSize = size; draw(); }
    }
    redrawIfResized();
    // start the draw-in only once web fonts have settled, so card sizes no longer change underneath it
    var fontsReady = document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve();
    fontsReady.then(function () {
      redrawIfResized();
      if (reduceMotion || !canObserve) flow.classList.add('drawn', 'static');
      else onceVisible(flow, 0.3, function () { flow.classList.add('drawn'); });
    });
    var timer;
    window.addEventListener('resize', function () { clearTimeout(timer); timer = setTimeout(redrawIfResized, 120); });
    window.addEventListener('load', redrawIfResized);
  }

  // Publications page: keep a paper opened from a link clear of the sticky filter bar
  var filters = document.querySelector('.filters');
  if (filters) {
    var setH = function () { root.style.setProperty('--filters-h', filters.offsetHeight + 'px'); };
    setH();
    window.addEventListener('resize', setH);
    if (location.hash && location.hash.indexOf('#p-') === 0) {
      var target = document.getElementById(location.hash.slice(1));
      if (target) setTimeout(function () { target.scrollIntoView({ block: 'start' }); }, 0);
    }
  }

  // Publication filters
  var pubs = Array.prototype.slice.call(document.querySelectorAll('.pub'));
  if (!pubs.length) return;
  var q = document.getElementById('pub-search'), count = document.getElementById('pub-count');
  var state = { type: 'all', topic: 'all', text: '' };
  function apply() {
    var shown = 0;
    pubs.forEach(function (li) {
      var ok = (state.type === 'all' || li.dataset.type === state.type) &&
               (state.topic === 'all' || (' ' + li.dataset.topics + ' ').indexOf(' ' + state.topic + ' ') > -1) &&
               (!state.text || li.dataset.search.indexOf(state.text) > -1);
      li.hidden = !ok; if (ok) shown++;
    });
    document.querySelectorAll('.year-block').forEach(function (b) {
      b.hidden = !b.querySelector('.pub:not([hidden])');
    });
    if (count) count.textContent = shown === pubs.length ? pubs.length + ' papers' : shown + ' of ' + pubs.length + ' papers';
  }
  document.querySelectorAll('.chips').forEach(function (group) {
    group.addEventListener('click', function (e) {
      var c = e.target.closest('.chip'); if (!c) return;
      group.querySelectorAll('.chip').forEach(function (x) { x.setAttribute('aria-pressed', x === c ? 'true' : 'false'); });
      state[group.dataset.key] = c.dataset.value; apply();
    });
  });
  if (q) q.addEventListener('input', function () { state.text = q.value.trim().toLowerCase(); apply(); });
  apply();
})();
