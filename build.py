#!/usr/bin/env python3
"""Build the static site for ali-zia.me (and its mirror alizia369.github.io).

Edit the files in data/ (news, publications, projects, grants) or the page text below, then run:

    python3 build.py

It writes index.html, research/, publications/, teaching/, grants/ and resume/ in place.
Standard library only; Python 3.12 or newer.
"""
import html
import json
import os
import pathlib
import re
from datetime import date

ROOT = pathlib.Path(__file__).resolve().parent
SITE = "https://ali-zia.me"
# Optional base path for a preview copy served below a domain root, e.g. SITE_BASE=/site-staging
# for https://alizia369.github.io/site-staging/. Leave unset for production: output is unchanged.
BASE = os.environ.get("SITE_BASE", "").rstrip("/")


def rebase(text):
    """Prefix root-relative links with BASE and mark the preview so search engines skip it."""
    if not BASE:
        return text
    text = re.sub(r'(href|src)="/(?!/)', rf'\1="{BASE}/', text)
    text = text.replace("; url=/", f"; url={BASE}/")
    text = text.replace("<head>\n", '<head>\n<meta name="robots" content="noindex, nofollow">\n', 1)
    text = text.replace("<body>\n", '<body>\n<div style="background:#b7650e;color:#fff;text-align:center;'
                        'font:600 13px/2.2 system-ui,sans-serif">Staging preview, not the live site</div>\n', 1)
    return text
ME = re.compile(r"\b(A\.\s?Zia)\b")
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
TOPICS = [("topology", "Topology"), ("hyperspectral", "Hyperspectral"), ("anomaly", "Anomaly detection"),
          ("agriculture", "Agriculture & food"), ("health", "Health"), ("sensing", "Radar & sensing"),
          ("3d", "3D vision"), ("robustness", "Robustness"), ("generative", "Generative"), ("other", "Other")]
TYPES = [("journal", "Journal"), ("conference", "Conference"), ("workshop", "Workshop"),
         ("preprint", "Preprint"), ("editorial", "Editorial"), ("dataset", "Dataset"), ("book", "Book chapter"), ("thesis", "Thesis")]


def data(name):
    return json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))


def esc(s):
    return html.escape(str(s), quote=True)


def bold_me(authors):
    return ME.sub(r'<b class="me">\1</b>', esc(authors))


def nice_date(d):
    parts = d.split("-")
    return f"{MONTHS[int(parts[1]) - 1]} {parts[0]}" if len(parts) > 1 else parts[0]


def _scholar():
    p = ROOT / "data" / "scholar.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"citations": 0, "h_index": 0, "updated": ""}


SCHOLAR = _scholar()
OV = data("overview.json")  # career, stats, themes and applications


def scholar_date():
    d = SCHOLAR.get("updated", "")
    return f"{MONTHS[int(d[5:7]) - 1]} {d[:4]}" if len(d) >= 7 else ""


def svg(name):
    return (ROOT / "assets" / "svg" / name).read_text(encoding="utf-8")


# ---------------------------------------------------------------- layout
MENU = [("/", "About"), ("/research/", "Research"), ("/publications/", "Publications"),
        ("/code/", "Code"), ("/teaching/", "Teaching"), ("/grants/", "Grants"), ("/resume/", "Resume")]

ICONS = {
    "mail": '<path d="M3 5h18a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1Zm1 2.3V17h16V7.3l-8 5.4-8-5.4ZM5.6 7 12 11.3 18.4 7H5.6Z"/>',
    "scholar": '<path d="M12 3 1 9l11 6 9-4.9V17h2V9L12 3Zm-6 9.7V16c0 1.7 2.7 3 6 3s6-1.3 6-3v-3.3l-6 3.3-6-3.3Z"/>',
    "github": '<path d="M12 2a10 10 0 0 0-3.2 19.5c.5.1.7-.2.7-.5v-1.7c-2.8.6-3.4-1.3-3.4-1.3-.5-1.2-1.1-1.5-1.1-1.5-.9-.6.1-.6.1-.6 1 .1 1.5 1 1.5 1 .9 1.6 2.4 1.1 3 .9.1-.7.4-1.1.6-1.4-2.2-.3-4.6-1.1-4.6-5a3.9 3.9 0 0 1 1-2.7 3.6 3.6 0 0 1 .1-2.7s.8-.3 2.8 1a9.6 9.6 0 0 1 5 0c1.9-1.3 2.8-1 2.8-1 .5 1.4.2 2.4.1 2.7a3.9 3.9 0 0 1 1 2.7c0 3.9-2.3 4.7-4.6 5 .4.3.7.9.7 1.9V21c0 .3.2.6.7.5A10 10 0 0 0 12 2Z"/>',
    "orcid": '<path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20ZM8.3 17H6.9V9.4h1.4V17Zm-.7-8.6a.9.9 0 1 1 0-1.8.9.9 0 0 1 0 1.8ZM17.3 13.2c0 2.2-1.6 3.8-4 3.8h-3V9.4h3c2.4 0 4 1.6 4 3.8Zm-1.4 0c0-1.5-1-2.5-2.7-2.5h-1.5v5h1.5c1.7 0 2.7-1 2.7-2.5Z"/>',
    "linkedin": '<path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5ZM3 9.5h4V21H3V9.5Zm6.5 0h3.8v1.6h.1c.5-1 1.8-2 3.8-2 4 0 4.8 2.6 4.8 6V21h-4v-5.2c0-1.2 0-2.8-1.7-2.8s-2 1.3-2 2.7V21h-4V9.5Z"/>',
}
LINKS = [("mail", "mailto:alizia369@gmail.com", "Email"),
         ("scholar", "https://scholar.google.com/citations?user=BVBJ06QAAAAJ", "Google Scholar"),
         ("github", "https://github.com/alizia369", "GitHub"),
         ("orcid", "https://orcid.org/0000-0003-4819-6666", "ORCID"),
         ("linkedin", "https://www.linkedin.com/in/ali-zia-0411b123/", "LinkedIn")]


def page(path, title, description, body):
    menu = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if h == path else ""}>{l}</a></li>' for h, l in MENU)
    links = "".join(f'<li><a href="{u}"><svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[i]}</svg>{l}</a></li>' for i, u, l in LINKS)
    full_title = "Ali Zia, machine learning researcher" if path == "/" else f"{title} | Ali Zia"
    updated = date.today().strftime("%B %Y")
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{SITE}{path}">
<meta property="og:title" content="{esc(full_title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:image" content="{SITE}/assets/img/profile.jpg">
<meta property="og:url" content="{SITE}{path}">
<meta name="theme-color" content="#f5f7fa">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%2314202e'/%3E%3Ccircle cx='10' cy='21' r='3' fill='%235daa3a'/%3E%3Ccircle cx='16' cy='10' r='3' fill='%232f6fd0'/%3E%3Ccircle cx='23' cy='20' r='3' fill='%23e2792e'/%3E%3Cpath d='M10 21 16 10 23 20Z' fill='none' stroke='%23cfd8e3' stroke-width='1.5'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&family=Public+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css">
</head>
<body>
<a class="skip" href="#content">Skip to content</a>
<div class="shell">
  <aside class="id" aria-label="Profile">
    <div class="id-top">
      <div class="portrait"><img src="/assets/img/profile.jpg" alt="Ali Zia" width="239" height="239"></div>
      <div>
        <a class="name" href="/">Ali Zia</a>
        <p class="role"><strong>Research Fellow in Machine Learning</strong><br>School of Computing, Engineering and Mathematical Sciences, La Trobe University<br>Adjunct, CSIRO and the Australian National University</p>
      </div>
    </div>
    <nav aria-label="Site"><ul class="menu">{menu}</ul></nav>
    <ul class="links">{links}</ul>
    <div class="metrics">
      <p><b>{SCHOLAR["citations"]:,}</b> citations, h-index <b>{SCHOLAR["h_index"]}</b></p>
      <p>Google Scholar, {scholar_date()}</p>
    </div>
  </aside>
  <main id="content">
{body}
    <footer>
      <p>Get in touch at <a href="mailto:alizia369@gmail.com">alizia369@gmail.com</a> or <a href="mailto:ali.zia@anu.edu.au">ali.zia@anu.edu.au</a>.</p>
      <p>Code on <a href="https://github.com/alizia369">GitHub</a>, papers on <a href="https://scholar.google.com/citations?user=BVBJ06QAAAAJ">Google Scholar</a>, and <a href="https://orcid.org/0000-0003-4819-6666">ORCID</a> and <a href="https://www.linkedin.com/in/ali-zia-0411b123/">LinkedIn</a> profiles.</p>
      <p>Last updated {updated}.</p>
      <button class="theme-switch" type="button" id="theme-switch">Dark theme</button>
    </footer>
  </main>
</div>
<script src="/assets/js/site.js" defer></script>
</body>
</html>
"""


def write(path, title, description, body):
    out = ROOT / (path.strip("/") or ".") / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(rebase(page(path, title, description, body)), encoding="utf-8")
    print("wrote", out.relative_to(ROOT))


def redirect(old, new):
    out = ROOT / old.strip("/") / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(rebase(f'<!doctype html><meta charset="utf-8"><title>Moved</title><link rel="canonical" href="{SITE}{new}">'
                          f'<meta http-equiv="refresh" content="0; url={new}"><p>This page moved to <a href="{new}">{new}</a>.</p>\n'), encoding="utf-8")
    print("wrote", out.relative_to(ROOT), "->", new)


def link_buttons(links):
    out = []
    for key, label in (("paper", "Paper"), ("arxiv", "arXiv"), ("project", "Project page"), ("code", "Code")):
        if links.get(key):
            out.append(f'<a{" class=\"code\"" if key == "code" else ""} href="{esc(links[key])}">{label}</a>')
    return "".join(out)


# ---------------------------------------------------------------- home
FEATURED_COPY = {
    "Test-Time Adaptation for Anomaly Segmentation via": ("svg:topoot-chain.svg", "TopoOT chains optimal transport across persistence diagrams from different thresholds and filtrations, then trains a light head online on the features that stay stable. Up to +24.1% mean F1 over the next best method on 2D benchmarks."),
    "Learning Topology-Aware Representations": ("topotta-arch.jpg", "TopoTTA replaces threshold heuristics with persistent homology on anomaly maps, producing pseudo-labels that keep defects connected. About 15% higher F1 on average across five 2D and 3D benchmarks."),
    "Hypergraph Contrastive Sensor Fusion": ("mmhcan.jpg", "MM-HCAN builds hypergraphs within and across sensor modalities and trains them contrastively, diagnosing bearing, stator and rotor faults together. Up to 99.82% accuracy with strong cross-domain transfer."),
    "2D–3D Feature Fusion": ("mafr.jpg", "MAFR fuses RGB and point clouds in one latent space and finds anomalies by how badly each modality restores. Mean I-AUROC of 0.972 on MVTec 3D-AD."),
}


def compact_pub(p):
    links = " ".join(f'<a href="{esc(p["links"][k])}">{lab}</a>' for k, lab in
                     (("paper", "paper"), ("arxiv", "arXiv"), ("code", "code")) if p["links"].get(k))
    note = f' <span class="award">{esc(p["note"])}</span>' if p.get("note") else ""
    venue = p.get("short") or p["venue"]
    return (f'<li class="pub"><span class="t">{esc(p["title"])}</span>'
            f'<span class="a">{bold_me(p["authors"])}</span>'
            f'<span class="meta"><span class="v">{esc(venue)}</span>{links}{note}</span></li>')


def repo_row(r):
    site = f' <a href="{esc(r["site"])}">site</a>' if r.get("site") else ""
    return (f'<div class="repo"><a class="name" href="{esc(r["url"])}">{esc(r["name"])}</a><span class="tag2">{esc(r["venue"])}</span>'
            f'<p>{esc(r["text"])}{site}</p></div>')


def build_home(news, pubs, code):
    items = "".join(
        f'<li{" class=\"more\"" if i >= 6 else ""}><time datetime="{esc(n["date"])}">{nice_date(n["date"])}</time><span>{n["text"]}</span></li>'
        for i, n in enumerate(news))
    toggle = ('<button class="toggle" type="button" aria-expanded="false" aria-controls="news-list" id="news-toggle">Show older news</button>'
              if len(news) > 6 else "")

    order = ["Test-Time Adaptation for Anomaly Segmentation via", "Learning Topology-Aware Representations", "Hypergraph Contrastive Sensor Fusion", "2D–3D Feature Fusion"]
    feats = []
    for key in order:
        p = next((x for x in pubs if x["title"].startswith(key)), None)
        if not p:
            continue
        fig, what = FEATURED_COPY[key]
        if fig.startswith("svg:"):
            figure = f'<div class="feat-fig drawn" aria-hidden="true">{svg(fig[4:])}</div>'
        else:
            figure = f'<div class="feat-fig"><img src="/assets/img/{fig}" alt="Overview figure for {esc(p["title"])}" loading="lazy"></div>'
        feats.append(f'<article class="feat">{figure}<div><span class="venue">{esc(p.get("short", p["venue"]))} {p["year"]}</span>'
                     f'<h3>{esc(p["title"])}</h3><p class="authors">{bold_me(p["authors"])}</p>'
                     f'<p class="what">{what}</p><div class="actions">{link_buttons(p["links"])}</div></div></article>')

    selected = [p for p in pubs if p.get("selected")]
    groups, seen = [], []
    for p in selected:
        label = str(p["year"]) if p["year"] >= 2023 else "Earlier"
        if label not in seen:
            seen.append(label)
            groups.append((label, []))
        groups[-1][1].append(p)
    repos_html = "".join(repo_row(r) for r in code["groups"][0]["items"])
    n_hsi = len(code["groups"][1]["items"])
    sel_html = "".join(f'<h3 class="year">{lab}</h3><ul class="pubs">{"".join(compact_pub(p) for p in ps)}</ul>' for lab, ps in groups)

    n_journal, n_conf, _ = counts(pubs, code)
    glance_tiles = tiles([
        tile(len(pubs), "publications", f"{n_journal} journal articles, {n_conf} conference and workshop papers and {len(pubs) - n_journal - n_conf} preprints and other works. {top_venues_line(pubs)}"),
        tile(SCHOLAR.get("citations", 0), "citations", f"h-index {SCHOLAR.get('h_index', 0)} and i10-index {SCHOLAR.get('i10_index', 0)} on Google Scholar, {scholar_date()}"),
        fixed_tile("funding"),
        fixed_tile("offerings"),
        fixed_tile("students"),
        fixed_tile("years"),
    ], 3, "Research and teaching in numbers")
    body = f"""
    <section id="about" aria-label="About">
      <p class="lede">I build machine learning models that keep working when data is scarce, noisy or shifted.</p>
      <div class="measure">
        <p>Much of my work brings topology into deep learning: persistent homology, cell and simplicial complexes and hypergraphs give a network structure it can rely on when pixel-level cues fail. I pair this with hyperspectral and multimodal sensing, where I started, and apply it to crops and food, medical imaging, industrial inspection and radar.</p>
        <p>I am a Research Fellow at La Trobe University with adjunct appointments at CSIRO and the Australian National University. I co-lead the CSIRO ML Workshop Series, supervise PhD and honours students, and received my PhD from Griffith University for work on 3D computer vision from hyperspectral images.</p>
      </div>
      <figure class="fig-hero">
        <div class="filtration-wrap">{svg("filtration.svg")}</div>
        <figcaption>One point cloud at four scales. As ε grows, edges and triangles fill in; small loops die quickly while the large one persists. That persistence is the signal topological deep learning keeps. Colour follows the visible spectrum, a nod to hyperspectral imaging.</figcaption>
      </figure>
    </section>

    <section id="glance" aria-labelledby="glance-h">
      <h2 id="glance-h">At a glance</h2>
      {glance_tiles}
      {milestones_html()}
      <a class="more-link" href="/resume/#pathway">Full career pathway</a>
    </section>

    <section id="recognition" aria-labelledby="rec-h">
      <h2 id="rec-h">Selected awards and recognition</h2>
      {recognition_html(pubs)}
    </section>

    <section id="news">
      <h2>News</h2>
      <ul class="news" id="news-list">{items}</ul>
      {toggle}
    </section>

    <section id="research-themes">
      <h2>Research</h2>
      {theme_teasers()}
      <a class="more-link" href="/research/#applications">Applications in agriculture, health, energy and IoT</a>
    </section>

    <section id="featured">
      <h2>Featured work</h2>
      {''.join(feats)}
    </section>

    <section id="selected">
      <h2>Selected publications</h2>
      {sel_html}
      <a class="more-link" href="/publications/">All {len(pubs)} publications, with search and filters</a>
    </section>

    <section id="code">
      <h2>Code</h2>
      <div class="repos">{repos_html}</div>
      <p class="muted" style="margin-top:14px">Plus {n_hsi} hyperspectral computer vision repositories in MATLAB from my PhD and related projects.</p>
      <a class="more-link" href="/code/">All code</a> &nbsp; <a class="more-link" href="https://github.com/alizia369">github.com/alizia369</a>
    </section>"""
    write("/", "About", "Ali Zia is a machine learning researcher at La Trobe University working on topological deep learning, hyperspectral imaging and reliable AI for agriculture, health and industry.", body)


# ---------------------------------------------------------------- publications
def build_publications(pubs):
    tl = dict(TOPICS)
    by_year = {}
    for p in pubs:
        by_year.setdefault(p["year"], []).append(p)
    blocks = []
    for year in sorted(by_year, reverse=True):
        lis = []
        for p in by_year[year]:
            links = " ".join(f'<a href="{esc(p["links"][k])}">{lab}</a>' for k, lab in
                             (("paper", "paper"), ("arxiv", "arXiv"), ("code", "code"), ("project", "project")) if p["links"].get(k))
            tags = "".join(f'<span class="tag">{tl.get(t, t)}</span>' for t in p["topics"])
            note = f'<span class="award">{esc(p["note"])}</span>' if p.get("note") else ""
            search = esc(" ".join([p["title"], p["authors"], p["venue"], p.get("short", ""), str(p["year"])] + [tl.get(t, t) for t in p["topics"]]).lower())
            lis.append(f'<li class="pub" id="{pub_id(p)}" data-type="{p["type"]}" data-topics="{" ".join(p["topics"])}" data-search="{search}">'
                       f'<span class="t">{esc(p["title"])}</span><span class="a">{bold_me(p["authors"])}</span>'
                       f'<span class="meta"><span class="v">{esc(p["venue"])}</span>{links}{note}{tags}</span></li>')
        blocks.append(f'<section class="year-block"><h2>{year}</h2><ul class="pubs">{"".join(lis)}</ul></section>')
    types = [t for t in TYPES if any(p["type"] == t[0] for p in pubs)]
    type_chips = '<button class="chip" type="button" data-value="all" aria-pressed="true">All types</button>' + "".join(
        f'<button class="chip" type="button" data-value="{k}" aria-pressed="false">{v}</button>' for k, v in types)
    topic_chips = '<button class="chip" type="button" data-value="all" aria-pressed="true">All topics</button>' + "".join(
        f'<button class="chip" type="button" data-value="{k}" aria-pressed="false">{v}</button>' for k, v in TOPICS)
    body = f"""
    <section aria-labelledby="t">
      <h1 class="page-title" id="t">Publications</h1>
      <p class="intro-text">Papers, preprints and datasets, newest first. Citation counts and the complete record are on <a href="https://scholar.google.com/citations?user=BVBJ06QAAAAJ">Google Scholar</a>.</p>
      <div class="filters">
        <input type="search" id="pub-search" placeholder="Search titles, authors, venues or topics" aria-label="Search publications">
        <div class="chips" data-key="type" role="group" aria-label="Filter by type">{type_chips}</div>
        <div class="chips" data-key="topic" role="group" aria-label="Filter by topic">{topic_chips}</div>
        <span class="count" id="pub-count" aria-live="polite">{len(pubs)} papers</span>
      </div>
      {''.join(blocks)}
    </section>"""
    write("/publications/", "Publications", "Publications of Ali Zia on topological deep learning, hyperspectral imaging, anomaly detection and applied machine learning.", body)


# ---------------------------------------------------------------- code
def build_code(code):
    groups = []
    for g in code["groups"]:
        lang = f'<p class="muted">{esc(g["lang"])}</p>' if g.get("lang") else ""
        groups.append(f'<section><h2>{esc(g["title"])}</h2>{lang}<div class="repos">{"".join(repo_row(r) for r in g["items"])}</div></section>')
    total = sum(len(g["items"]) for g in code["groups"])
    body = f"""
    <section aria-labelledby="t">
      <h1 class="page-title" id="t">Code</h1>
      <p class="intro-text">Research code for my papers, from recent PyTorch projects to the original MATLAB code behind my hyperspectral work. Everything is on <a href="{esc(code["profile"])}">github.com/alizia369</a>.</p>
      <div class="downloads"><a class="primary" href="{esc(code["profile"])}">All repositories on GitHub</a><a href="/publications/">Papers with code links</a></div>
    </section>
    {''.join(groups)}"""
    write("/code/", "Code", f"Open-source research code by Ali Zia: {total} repositories covering topological deep learning, anomaly detection and hyperspectral computer vision.", body)


# ---------------------------------------------------------------- teaching
def build_teaching():
    body = """
    <section aria-labelledby="t">
      <h1 class="page-title" id="t">Teaching and supervision</h1>
      <p class="intro-text">More than a decade of teaching in Australia and Pakistan, from first-year programming to graduate courses in AI and computer vision, alongside supervision of research students in machine learning and imaging.</p>
      """ + tiles([fixed_tile("offerings"), fixed_tile("courses"), fixed_tile("students"), fixed_tile("years")], 4, "Teaching in numbers") + """
    </section>

    <section aria-labelledby="courses-h">
      <h2 id="courses-h">Courses</h2>
      <div class="two">
        <div>
          <ul class="entries">
            <li><div class="h">La Trobe University</div><div class="s">Data Analysis and Design (casual lecturer)</div></li>
            <li><div class="h">Griffith University</div><div class="s">Programming (casual lecturer); lab instructor over several years for Programming, Advanced Programming, Software Engineering, Software Design, Big Data Analysis, Sensor Networks and others</div></li>
            <li><div class="h">Australian National University</div><div class="s">Teaching in computing courses</div></li>
          </ul>
        </div>
        <div>
          <ul class="entries">
            <li><div class="h">COMSATS University, Pakistan</div><div class="s">Artificial Intelligence (eight semesters), Machine Learning (three), Computer Vision (two), Systems Programming and Advanced Operating Systems; designed the AI, Operating Systems and Systems Programming courses</div></li>
            <li><div class="h">Also taught</div><div class="s">Electric Circuits, Human–Computer Interaction, Computing for Management</div></li>
          </ul>
        </div>
      </div>
    </section>

    <section aria-labelledby="sup-h">
      <h2 id="sup-h">Supervision</h2>
      <p class="measure">I supervise PhD and honours students at La Trobe and with partner universities, and was main supervisor for a visiting PhD student at ANU who has since completed his doctorate. Recent student projects span topological deep learning, anomaly detection, radar perception and hyperspectral analysis.</p>
    </section>

    <section aria-labelledby="tut-h">
      <h2 id="tut-h">Tutorials and workshops</h2>
      <ul class="entries measure">
        <li><div class="h"><a href="https://alizia369.github.io/acml2026-tdl/">Topological Deep Learning for Robust Representation Learning</a></div><div class="s">Tutorial at ACML 2026, Melbourne, 1 December 2026, with Usman Ali and Abdelwahed Khamis</div></li>
        <li><div class="h">CSIRO ML Workshop Series</div><div class="s">Co-lead</div></li>
      </ul>
    </section>

    <section aria-labelledby="how-h">
      <h2 id="how-h">How I teach</h2>
      <div class="measure">
        <p>I try to build independent thinkers who can recover from being stuck. In lectures that means posing questions before giving answers and checking understanding as we go; in labs and projects it means real data, open-ended problems and plenty of peer discussion.</p>
        <p>I mix formal lectures with project-based, collaborative and enquiry-based learning, and use online tools where they genuinely help: recorded lectures, discussion forums and short quizzes that show students where they stand.</p>
        <p>With research students I start from their strengths, agree on a small first result, and widen from there.</p>
      </div>
    </section>"""
    write("/teaching/", "Teaching", "Teaching and supervision by Ali Zia at La Trobe, Griffith, ANU and COMSATS.", body)


# ---------------------------------------------------------------- grants
def build_grants(g):
    rows = "".join(
        f'<tr><td class="y">{esc(x["year"])}</td><td><div class="what">{esc(x["title"])}</div>'
        f'<div class="who">{esc(x["funder"])}{", " + esc(x["role"]) if x.get("role") else ""}</div></td>'
        f'<td class="amt">{esc(x["amount"]) if x.get("amount") else "&nbsp;"}</td></tr>' for x in g["items"])
    body = f"""
    <section aria-labelledby="t">
      <h1 class="page-title" id="t">Grants</h1>
      <p class="intro-text">{esc(g["summary"])}</p>
      <table class="grants">
        <thead><tr><th scope="col">Year</th><th scope="col">Project and funder</th><th scope="col" class="amt">Amount (AUD)</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </section>"""
    write("/grants/", "Grants", "Competitive research funding awarded to Ali Zia.", body)


# ---------------------------------------------------------------- resume
def build_resume():
    body = """
    <section aria-labelledby="t">
      <h1 class="page-title" id="t">Resume</h1>
      <p class="intro-text">A summary of my career is below. The PDFs carry full details; they date from 2023 and 2024 and will be refreshed.</p>
      <div class="downloads"><a class="primary" href="/assets/cv/Ali_Zia_CV_short.pdf">Short resume (PDF)</a><a href="/assets/cv/Ali_Zia_CV_detailed.pdf">Detailed resume (PDF)</a></div>
    </section>

    <section class="career-path" id="pathway" aria-labelledby="path-h">
      <h2 id="path-h">Career pathway</h2>
      <p class="intro-text">Several roles ran in parallel, and research has come with teaching at every stage. Dates and details are in the lists below.</p>
      """ + career_flow() + """
    </section>

    <section>
      <div class="two">
        <div>
          <h2 class="block-title">Positions</h2>
          <ul class="entries">
            <li><div class="h">Research Fellow</div><div class="s">School of Computing, Engineering and Mathematical Sciences, La Trobe University</div></li>
            <li><div class="h">Adjunct appointments</div><div class="s">CSIRO and the Australian National University</div></li>
            <li><div class="h">Postdoctoral Research Fellow</div><div class="s">Future Science Platform, Australian National University and CSIRO</div></li>
            <li><div class="h">Postdoctoral Researcher</div><div class="s">ARC Hub for Driving Farming Productivity and Disease Prevention, Griffith University</div></li>
            <li><div class="h">Developer, lab instructor and lecturer</div><div class="s">Griffith University</div></li>
            <li><div class="h">Assistant Professor</div><div class="s">COMSATS University, Pakistan</div></li>
            <li><div class="h">Research Scholar</div><div class="s">NICTA, Australia</div></li>
            <li><div class="h">Software Engineer</div><div class="s">Systems Ltd, Cambridge Docs and Techlogix, Pakistan</div></li>
          </ul>
        </div>
        <div>
          <h2 class="block-title">Education</h2>
          <ul class="timeline">
            <li><span class="y">2020</span><div><b>PhD in Artificial Intelligence</b>, Griffith University<br><span class="muted">Exploring extrinsic spectral properties of hyperspectral images for 3D computer vision</span></div></li>
            <li><span class="y">2009</span><div><b>Master of Computing</b>, Australian National University</div></li>
            <li><span class="y">2006</span><div><b>BSc (Hons) in Computer Science</b>, University of the Punjab</div></li>
          </ul>
          <h2 class="block-title" style="margin-top:32px">Service and recognition</h2>
          <ul class="entries">
            <li><div class="h">Lead guest editor</div><div class="s"><a href="https://link.springer.com/collections/fiaehabchh" rel="noopener">SN Computer Science collection, AI for Agriculture</a>, 2026</div></li>
            <li><div class="h">Tutorial lead</div><div class="s"><a href="https://www.acml-conf.org/2026/program/tutorials/" rel="noopener">Topological Deep Learning, ACML 2026</a></div></li>
            <li><div class="h">Silver Reviewer</div><div class="s">ICML 2026</div></li>
            <li><div class="h">Reviewer</div><div class="s">CVPR 2026</div></li>
            <li><div class="h">Co-lead</div><div class="s">CSIRO ML Workshop Series</div></li>
            <li><div class="h">Best student paper award</div><div class="s">APRS/IEEE, DICTA 2025</div></li>
            <li><div class="h">Guest editor</div><div class="s">Frontiers in Remote Sensing special issue on resilient cities, remote sensing and AI, 2025</div></li>
            <li><div class="h">Sole invited speaker</div><div class="s">Joint IEEE GRSS, IEEE CS and CDS seminar at ANU, 2025</div></li>
            <li><div class="h">Runner-up paper award</div><div class="s">DICTA 2023</div></li>
            <li><div class="h">Invited seminars</div><div class="s">COMSATS University and University of the Punjab, 2023</div></li>
            <li><div class="h">Best project award</div><div class="s">Robot path identification and map construction, 2011</div></li>
          </ul>
          <p style="margin-top:20px"><a href="/grants/">Grants</a> and <a href="/teaching/">teaching</a> have their own pages.</p>
        </div>
      </div>
    </section>"""
    write("/resume/", "Resume", "Resume of Ali Zia: positions, education, service and downloadable CVs.", body)


# ---------------------------------------------------------------- shared components (career, tiles, evidence)
CAT_LABEL = {"edu": "Education", "ind": "Industry", "acad": "Academic and teaching", "res": "Industry and academic research"}


def pub_id(p):
    """Stable anchor for a paper on the Publications page, derived from its title."""
    s = re.sub(r"[^a-z0-9]+", "-", p["title"].lower()).strip("-")
    if len(s) > 60:
        s = s[:60].rsplit("-", 1)[0]
    return "p-" + s


def icon(name):
    return svg(f"icons/{name}.svg")  # Lucide icons, ISC licence (assets/svg/icons/LICENSE-lucide.txt)


def find_pub(pubs, prefix):
    found = [p for p in pubs if p["title"].startswith(prefix)]
    if len(found) != 1:
        raise SystemExit(f"data/overview.json: {prefix!r} matches {len(found)} publications; it must match exactly one")
    return found[0]


def venue_tag(p):
    label = p.get("short") or ("arXiv" if p["type"] == "preprint" else p["venue"])
    return f'<a class="vt" href="/publications/#{pub_id(p)}" title="{esc(p["title"])}">{esc(label)} {p["year"]}</a>'


def career_node(n):
    badges = f'<span class="badge" data-cat="{n["cat"]}">{icon(n["cat"])}<span class="sr">{CAT_LABEL[n["cat"]]}</span></span>'
    if n.get("teach"):
        badges += f'<span class="badge" data-cat="acad">{icon("acad")}<span class="sr">with teaching</span></span>'
    role = esc(n["role"])
    if n.get("brief"):
        role = f'<span class="full">{role}</span><span class="brief" aria-hidden="true">{esc(n["brief"])}</span>'
    now = '<span class="now">Current role</span>' if n.get("current") else ""
    extra = f'<span class="o">{esc(n["extra"])}</span>' if n.get("extra") else ""
    cls = "node" + (" current" if n.get("current") else "") + (" par" if n.get("parallel") else "")
    return (f'<li class="{cls}" id="cn-{n["id"]}" data-cat="{n["cat"]}" style="--col:{n["col"]};--row:{n.get("row", 1)}">'
            f'<span class="badges">{badges}</span>{now}<span class="r">{role}</span><span class="o">{esc(n["org"])}</span>{extra}</li>')


def tile(value, label, detail, decimals=0, prefix="", suffix=""):
    shown = f"{prefix}{value:,.{decimals}f}{suffix}"
    return (f'<div class="tile"><b><span data-count="{value}" data-decimals="{decimals}" data-prefix="{esc(prefix)}" '
            f'data-suffix="{esc(suffix)}">{esc(shown)}</span></b>'
            f'<span class="l">{esc(label)}</span><span class="d">{esc(detail)}</span></div>')


def tiles(items, cols, label):
    return f'<div class="tiles t{cols}" role="group" aria-label="{esc(label)}">{"".join(items)}</div>'


def fixed_tile(key):
    s = OV["stats"][key]
    return tile(s["value"], s["label"], s["detail"], s.get("decimals", 0), s.get("prefix", ""), s.get("suffix", ""))


def top_venues_line(pubs):
    venues = OV["stats"]["top_venues"]
    shorts = {p.get("short") for p in pubs}
    missing = [v for v in venues if v not in shorts]
    if missing:
        raise SystemExit(f"data/overview.json: top_venues {missing} match no paper in publications.json")
    return "Including " + ", ".join(venues[:-1]) + " and " + venues[-1]


def counts(pubs, code):
    n_journal = sum(p["type"] == "journal" for p in pubs)
    n_conf = sum(p["type"] in ("conference", "workshop") for p in pubs)
    n_repos = sum(len(g["items"]) for g in code["groups"])
    return n_journal, n_conf, n_repos


def legend_html():
    return "".join(f'<li><span class="badge" data-cat="{k}">{icon(k)}</span>{v}</li>' for k, v in
                   (("edu", "Education"), ("ind", "Industry"), ("acad", "Academic and teaching"), ("res", "Research with industry")))


def career_flow():
    car = OV["career"]
    ids = {n["id"] for n in car["nodes"]}
    for e in car["edges"]:
        if e[0] not in ids or e[1] not in ids:
            raise SystemExit(f"data/overview.json: career edge {e} names an unknown node")
    band1 = "".join(career_node(n) for n in car["nodes"] if n["band"] == 1)
    band2 = "".join(career_node(n) for n in car["nodes"] if n["band"] == 2)
    return f"""<ul class="legend" aria-label="Key">{legend_html()}</ul>
      <div class="flow" data-flow data-edges="{esc(json.dumps(car["edges"]))}">
        <svg class="flow-lines" aria-hidden="true" focusable="false"></svg>
        <ol class="band band1" aria-label="Early career">{band1}</ol>
        <p class="par-label">{esc(car["parallel_label"])}</p>
        <ol class="band band2" aria-label="Griffith, postdoctoral and current roles">{band2}</ol>
      </div>"""


def milestones_html():
    lis = []
    for i, m in enumerate(OV["milestones"]):
        now = '<span class="sr">(current role)</span>' if m.get("current") else ""
        lis.append(f'<li data-cat="{m["cat"]}"{" class=\"current\"" if m.get("current") else ""} style="--i:{i}">'
                   f'<span class="badge">{icon(m["cat"])}<span class="sr">{CAT_LABEL[m["cat"]]}</span></span>'
                   f'<span class="r">{esc(m["role"])}{now}</span><span class="o">{esc(m["org"])}</span></li>')
    return f'<div class="mini-path" data-reveal><ol class="milestones" aria-label="Career milestones">{"".join(lis)}</ol></div>'


def evidence(items, pubs):
    lis = []
    for it in items:
        tags = "".join(venue_tag(find_pub(pubs, pre)) for pre in it["papers"])
        lis.append(f'<li><span class="it">{esc(it["t"])}</span><span class="vts">{tags}</span></li>')
    return f'<p class="ev-h">Key papers</p><ul class="ev">{"".join(lis)}</ul>'


def gallery(figs, pubs):
    out = []
    for f in figs:
        if f.get("svg"):
            media = f'<div class="g-media drawn" role="img" aria-label="{esc(f["alt"])}">{svg(f["svg"])}</div>'
        else:
            if not (ROOT / "assets" / "img" / f["img"]).exists():
                raise SystemExit(f"data/overview.json: figure {f['img']} not found in assets/img")
            media = (f'<a class="g-media" href="/assets/img/{esc(f["img"])}" title="Open full size">'
                     f'<img src="/assets/img/{esc(f["img"])}" alt="{esc(f["alt"])}" loading="lazy"></a>')
        tag = " " + venue_tag(find_pub(pubs, f["paper"])) if f.get("paper") else ""
        credit = f' <span class="g-credit">{esc(f["credit"])}</span>' if f.get("credit") else ""
        out.append(f'<figure class="g-item">{media}<figcaption>{esc(f["caption"])}{tag}{credit}</figcaption></figure>')
    return f'<p class="ev-h">From the papers</p><div class="gallery" data-n="{len(figs)}">{"".join(out)}</div>'


def card_head(title, icon_name, level="h3"):
    return f'<div class="card-head"><span class="area-ic">{icon(icon_name)}</span><{level}>{esc(title)}</{level}></div>'


def project_card(p):
    refs = "".join(f'<li>{"<a href=\"" + esc(r["url"]) + "\">" + esc(r["label"]) + "</a>" if r["url"] else esc(r["label"])}</li>'
                   for r in p.get("papers", []))
    video = f' <a href="/{esc(p["video"])}">Watch a clip</a>.' if p.get("video") else ""
    partners = f'<p class="partners">{esc(p["partners"])}</p>' if p.get("partners") else ""
    return (f'<article class="project"><img src="/assets/img/projects/{esc(p["image"])}" alt="{esc(p["alt"])}" loading="lazy">'
            f'<h4>{esc(p["title"])}</h4>{partners}<p>{esc(p["text"])}{video}</p>'
            f'{"<ul class=\"refs\">" + refs + "</ul>" if refs else ""}</article>')


# Figure and prose for each research theme on the Research page; the evidence lists come from data/overview.json
THEME_COPY = {
    "topology": ('<img src="/assets/img/projects/tdl-pipeline.jpg" alt="Diagram of topological deep learning: topological embedding, representation and loss during training, and topological analysis after training" loading="lazy">',
                 '<p>Topology describes what stays the same when data is stretched or corrupted: connected parts, loops and voids. I use persistent homology to turn anomaly maps into reliable pseudo-labels, optimal transport to compare persistence diagrams across scales, and hypergraphs and cell complexes to model relations between sensors and views in radar and fault diagnosis.</p>'
                 '<p>I co-wrote a <a href="https://link.springer.com/article/10.1007/s10462-024-10710-9">review of topological deep learning</a>, contributed to <a href="https://www.jmlr.org/papers/v25/24-0110.html">TopoX</a>, and am teaching a tutorial on the topic at ACML 2026.</p>'),
    "hyperspectral": ('<img src="/assets/img/papers/tip-depth-composite.webp" alt="Depth from chromatic aberration: a checkerboard board in a hyperspectral image, the same edge cropped from bands between 580 and 940 nm showing blur that changes with wavelength, and below, the 720 nm band image beside the recovered relative depth map" loading="lazy" width="1400" height="1041">',
                      '<p>A hyperspectral camera records hundreds of narrow bands, so each pixel carries a spectrum rather than three colours. My PhD used these spectra for 3D vision, recovering depth from chromatic aberration and defocus. Since then I have worked on weak-signal unmixing, spectral features for food and crops, and on fusing spectral data with lidar, point clouds and radar.</p>'),
    "reliable": ('<img src="/assets/img/anomaly-masks.jpg" alt="Anomaly segmentation results: input, ground truth, heat map, threshold baseline, TTT4AS and TopoTTA" loading="lazy" width="981" height="412">',
                 '<p>Models trained in the lab meet new lighting, sensors and populations in deployment. I work on test-time adaptation that needs no source data or labels, on diagnosing out-of-distribution robustness from representation geometry, on training-free reasoning with vision–language models, and on learning when labels are scarce.</p>'),
}

THEME_CAPTION = {  # optional caption under a theme's main figure: (text, start of the paper title)
    "hyperspectral": ("Depth from a single hyperspectral image, using chromatic aberration and defocus.", "Exploring Chromatic Aberration"),
}

THEME_TEASER = {
    "topology": "Persistent homology, optimal transport between persistence diagrams and message passing on hypergraphs and cell complexes, with a widely read review of the field and the TopoX library.",
    "hyperspectral": "Hundreds of narrow bands reveal what RGB cannot: protein in chickpea, contamination in meat, disease in sugarcane. Weak-signal unmixing, spectral 3D vision and fusion with lidar and radar.",
    "reliable": "Test-time adaptation and out-of-distribution robustness for models deployed where data shifts: industrial inspection, radar, fault diagnosis and embryo assessment for IVF.",
}


def theme_caption(theme_id, pubs):
    if theme_id not in THEME_CAPTION:
        return ""
    text, paper = THEME_CAPTION[theme_id]
    return f'<p class="theme-cap">{esc(text)} {venue_tag(find_pub(pubs, paper))}</p>'


def recognition_html(pubs):
    lis = []
    for r in OV["recognition"]:
        detail = esc(r["detail"])
        if r.get("paper"):
            detail += " " + venue_tag(find_pub(pubs, r["paper"]))
        title = esc(r["title"])
        if r.get("url"):
            title = f'<a href="{esc(r["url"])}" rel="noopener">{title}</a>'
        lis.append(f'<li><span class="aw-ic">{icon(r["icon"])}</span><div><span class="h">{title}</span>'
                   f'<span class="s">{detail}</span></div><span class="y">{esc(r["year"])}</span></li>')
    return f'<ul class="awards">{"".join(lis)}</ul>'


def theme_teasers():
    cards = "".join(f'<a class="teaser" href="/research/#{t["id"]}" style="--a:var(--c-{t["color"]})">{card_head(t["title"], t["icon"])}'
                    f'<p>{esc(THEME_TEASER[t["id"]])}</p><span class="go">Themes, papers and projects</span></a>' for t in OV["themes"])
    return f'<div class="teasers">{cards}</div>'


def build_research(projects, earlier, pubs, code):
    n_journal, n_conf, n_repos = counts(pubs, code)
    stats = tiles([
        tile(n_journal, "journal articles", "Including IEEE TPAMI, IEEE TIP, JMLR and Artificial Intelligence Review"),
        tile(n_conf, "conference and workshop papers", "Including NeurIPS, ECCV, WACV and CVPR workshops"),
        tile(SCHOLAR.get("h_index", 0), "h-index", f"i10-index {SCHOLAR.get('i10_index', 0)} and {SCHOLAR.get('citations', 0):,} citations on Google Scholar, {scholar_date()}"),
        tile(n_repos, "open-source repositories", "Research code for papers, from PyTorch to the original MATLAB"),
    ], 4, "Research in numbers")

    themes = []
    for t in OV["themes"]:
        fig, prose = THEME_COPY[t["id"]]
        themes.append(f'<article class="theme-card" id="{t["id"]}" style="--a:var(--c-{t["color"]})">{card_head(t["title"], t["icon"])}'
                      f'<div class="theme-body"><div><div class="theme-fig">{fig}</div>{theme_caption(t["id"], pubs)}</div><div class="theme-text">{prose}</div></div>'
                      f'{gallery(t.get("figures", []), pubs) if t.get("figures") else ""}{evidence(t["items"], pubs)}</article>')

    by_domain = {}
    for p in projects:
        by_domain.setdefault(p.get("domain", "other"), []).append(p)
    known = {a["id"] for a in OV["applications"]} | {"other"}
    for d in by_domain:
        if d not in known:
            raise SystemExit(f"data/projects.json: unknown domain {d!r}")
    domains = []
    for a in OV["applications"]:
        projs = by_domain.get(a["id"], [])
        proj_html = (f'<p class="ev-h">Projects</p><div class="projects">{"".join(project_card(p) for p in projs)}</div>' if projs else "")
        figs = gallery(a["figures"], pubs) if a.get("figures") else ""
        domains.append(f'<article class="domain" id="{a["id"]}" style="--a:var(--c-{a["color"]})">{card_head(a["title"], a["icon"])}'
                       f'{figs}{evidence(a["items"], pubs)}{proj_html}</article>')
    others = by_domain.get("other", [])
    other_html = (f'<h3 class="block-title" style="margin-top:40px">Other projects</h3><div class="projects">{"".join(project_card(p) for p in others)}</div>'
                  if others else "")
    earlier_html = "".join(f"<li>{esc(e)}</li>" for e in earlier)

    body = f"""
    <section aria-labelledby="t">
      <h1 class="page-title" id="t">Research</h1>
      <p class="intro-text">My work asks how to give learning systems structure they can trust: the shape of the data, the physics of the sensor and the relationships between modalities. It runs along three themes and is applied with partners in agriculture, food, health, energy and industry.</p>
      {stats}
      <nav class="jump" aria-label="On this page">{"".join(f'<a href="#{t["id"]}">{esc(t["title"])}</a>' for t in OV["themes"])}<a href="#applications">Applications</a></nav>
    </section>

    <section aria-labelledby="themes-h">
      <h2 id="themes-h">Research themes</h2>
      <p class="intro-text">Each tag opens the paper behind it on the Publications page.</p>
      {"".join(themes)}
    </section>

    <section id="applications" aria-labelledby="apps-h">
      <h2 id="apps-h">Applications</h2>
      <p class="intro-text">Where these methods are put to work, with the papers and projects in each area.</p>
      {"".join(domains)}
      {other_html}
      <h3 class="block-title" style="margin-top:36px">Earlier projects</h3>
      <ul class="plain measure">{earlier_html}</ul>
    </section>"""
    write("/research/", "Research", "Research themes and applications of Ali Zia: topological deep learning, hyperspectral and multimodal sensing, and reliable AI, applied to agriculture, health, energy and IoT security.", body)


if __name__ == "__main__":
    news = data("news.json")["items"]
    pubs = data("publications.json")["items"]
    projects = data("projects.json")
    code = data("code.json")
    build_home(news, pubs, code)
    build_code(code)
    build_research(projects["items"], projects.get("earlier", []), pubs, code)
    build_publications(pubs)
    build_teaching()
    build_grants(data("grants.json"))
    build_resume()
    redirect("/cv/", "/resume/")
