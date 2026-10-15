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
