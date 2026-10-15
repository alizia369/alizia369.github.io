#!/usr/bin/env python3
"""Build the static site for ali-zia.me (and its mirror alizia369.github.io).

Edit the files in data/ (news, publications, projects) or the page text below, then run:

    python3 build.py

It writes index.html, research/, publications/, teaching/ and cv/ in place. Standard library only.
"""
import html
import json
import pathlib
import re
from datetime import date

ROOT = pathlib.Path(__file__).resolve().parent
SITE = "https://ali-zia.me"
ME = re.compile(r"\b(A\.\s?Zia)\b")
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
TOPICS = [("topology", "Topology"), ("hyperspectral", "Hyperspectral"), ("anomaly", "Anomaly detection"),
          ("agriculture", "Agriculture & food"), ("health", "Health"), ("sensing", "Radar & sensing"),
          ("3d", "3D vision"), ("robustness", "Robustness"), ("generative", "Generative"), ("other", "Other")]
TYPES = [("journal", "Journal"), ("conference", "Conference"), ("workshop", "Workshop"),
         ("preprint", "Preprint"), ("dataset", "Dataset"), ("book", "Book chapter"), ("thesis", "Thesis")]

def load(name):
    return json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))["items"]

def esc(s):
    return html.escape(s, quote=True)

def bold_me(authors):
    return ME.sub(r'<b class="me">\1</b>', esc(authors))

def nice_date(d):
    parts = d.split("-")
    return f"{MONTHS[int(parts[1]) - 1]} {parts[0]}" if len(parts) > 1 else parts[0]

# ---------------------------------------------------------------- layout
NAV = [("/", "Home"), ("/research/", "Research"), ("/publications/", "Publications"),
       ("/teaching/", "Teaching"), ("/cv/", "CV")]

def page(path, title, description, body):
    nav = "".join(
        f'<li><a href="{href}"{" aria-current=\"page\"" if href == path else ""}>{label}</a></li>'
        for href, label in NAV)
    full_title = "Ali Zia" if path == "/" else f"{title} | Ali Zia"
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
<meta name="theme-color" content="#ffffff">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%23161c2d'/%3E%3Crect x='6' y='9' width='4' height='14' fill='%235b4bb7'/%3E%3Crect x='12' y='9' width='4' height='14' fill='%231e9e8f'/%3E%3Crect x='18' y='9' width='4' height='14' fill='%23d6aa1e'/%3E%3Crect x='24' y='9' width='3' height='14' fill='%23c8374a'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&family=Spectral:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css">
</head>
<body>
<a class="skip" href="#content">Skip to content</a>
<div class="strip" aria-hidden="true"></div>
<header class="site-head">
  <div class="wrap">
    <a class="brand" href="/">Ali Zia</a>
    <nav aria-label="Main"><ul class="nav">{nav}</ul></nav>
  </div>
</header>
<main id="content">
{body}
</main>
<footer class="site-foot">
  <div class="wrap">
    <div>
      <p>Ali Zia, School of Computing, Engineering and Mathematical Sciences, La Trobe University, Melbourne.</p>
      <p><a href="mailto:alizia369@gmail.com">alizia369@gmail.com</a> &nbsp; <a href="https://scholar.google.com/citations?user=BVBJ06QAAAAJ">Google Scholar</a> &nbsp; <a href="https://github.com/alizia369">GitHub</a> &nbsp; <a href="https://orcid.org/0000-0003-4819-6666">ORCID</a> &nbsp; <a href="https://www.linkedin.com/in/ali-zia-0411b123/">LinkedIn</a></p>
      <p>Last updated {updated}.</p>
    </div>
    <button class="theme-switch" type="button" id="theme-switch">Dark theme</button>
  </div>
</footer>
<script src="/assets/js/site.js" defer></script>
</body>
</html>
"""

def write(path, title, description, body):
    out = ROOT / (path.strip("/") or ".") / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page(path, title, description, body), encoding="utf-8")
    print("wrote", out.relative_to(ROOT))

def link_buttons(links, labels=(("paper", "Paper"), ("arxiv", "arXiv"), ("project", "Project page"), ("code", "Code"))):
    out = []
    for key, label in labels:
        if links.get(key):
            cls = ' class="code"' if key == "code" else ""
            out.append(f'<a{cls} href="{esc(links[key])}">{label}</a>')
    return "".join(out)

# ---------------------------------------------------------------- home
FEATURED_COPY = {
    "Topology-Aware Optimal Transport": ("svg:topoot-chain.svg", "TopoOT chains optimal transport across persistence diagrams from different thresholds and filtrations, then trains a light head online on the features that stay stable. Up to +24.1% mean F1 over the next best method on 2D benchmarks."),
    "Learning Topology-Aware Representations": ("topotta-arch.jpg", "TopoTTA replaces threshold heuristics with persistent homology on anomaly maps, producing pseudo-labels that keep defects connected. About 15% higher F1 on average across five 2D and 3D benchmarks."),
    "Hypergraph Contrastive Sensor Fusion": ("mmhcan.jpg", "MM-HCAN builds hypergraphs within and across sensor modalities and trains them contrastively, diagnosing bearing, stator and rotor faults together. Up to 99.82% accuracy with strong cross-domain transfer."),
    "2D–3D Feature Fusion": ("mafr.jpg", "MAFR fuses RGB and point clouds in one latent space and finds anomalies by how badly each modality restores. Mean I-AUROC of 0.972 on MVTec 3D-AD."),
}

def build_home(news, pubs):
    items = []
    for i, n in enumerate(news):
        cls = ' class="more"' if i >= 6 else ""
        items.append(f'<li{cls}><time datetime="{esc(n["date"])}">{nice_date(n["date"])}</time><span>{n["text"]}</span></li>')
    toggle = '<button class="btn-quiet" type="button" id="news-toggle" aria-expanded="false" aria-controls="news-list">Show older news</button>' if len(news) > 6 else ""

    cards = []
    for p in [x for x in pubs if x.get("featured")]:
        key = next((k for k in FEATURED_COPY if p["title"].startswith(k)), None)
        if not key:
            continue
        fig, what = FEATURED_COPY[key]
        if fig.startswith("svg:"):
            svg = (ROOT / "assets" / "svg" / fig[4:]).read_text(encoding="utf-8")
            figure = f'<div class="fig" style="background:var(--paper)" aria-hidden="true">{svg}</div>'
        else:
            figure = f'<div class="fig"><img src="/assets/img/{fig}" alt="Overview figure for {esc(p["title"])}" loading="lazy"></div>'
        cards.append(f"""<article class="paper">{figure}
      <div class="body"><span class="venue">{esc(p.get("short", p["venue"]))} {p["year"]}</span>
        <h3>{esc(p["title"])}</h3><p class="authors">{bold_me(p["authors"])}</p>
        <p class="what">{what}</p><div class="actions">{link_buttons(p["links"])}</div></div></article>""")

    body = f"""
<div class="wrap">
  <section class="hero" aria-labelledby="name">
    <div>
      <div class="who"><img src="/assets/img/profile.jpg" alt="Ali Zia" width="84" height="84">
        <div><h1 id="name">Ali Zia</h1></div></div>
      <p class="role">Research Fellow in Machine Learning, La Trobe University<br>Adjunct, CSIRO and the Australian National University</p>
      <p class="lede">I build machine learning models that keep working when data is scarce, noisy or shifted, using topology and spectral imaging to give them structure they can rely on.</p>
      <ul class="links">
        <li><a href="https://scholar.google.com/citations?user=BVBJ06QAAAAJ">Google Scholar</a></li>
        <li><a href="https://github.com/alizia369">GitHub</a></li>
        <li><a href="https://orcid.org/0000-0003-4819-6666">ORCID</a></li>
        <li><a href="https://www.linkedin.com/in/ali-zia-0411b123/">LinkedIn</a></li>
        <li><a href="mailto:alizia369@gmail.com">Email</a></li>
      </ul>
    </div>
    <figure class="cube">
      <img src="/assets/img/hero-cube.webp" width="1094" height="756" alt="A field image of grazing cattle with detection boxes and pose keypoints, drawn as the front face of a hyperspectral cube whose stacked layers are tinted from violet through red to near-infrared grey.">
      <figcaption>Cattle detection from our livestock work, drawn as a hyperspectral cube: one scene, many bands.</figcaption>
    </figure>
  </section>

  <section class="section split" aria-labelledby="news-h">
    <div>
      <div class="section-head"><h2 id="news-h">News</h2></div>
      <ul class="news" id="news-list">{''.join(items)}</ul>
      {toggle}
    </div>
    <aside class="now" aria-labelledby="now-h">
      <h3 id="now-h">Now</h3>
      <ul>
        <li><b>Research Fellow</b>, School of Computing, Engineering and Mathematical Sciences, La Trobe University</li>
        <li><b>Adjunct</b> at CSIRO and the Australian National University</li>
        <li><b>Co-lead</b>, CSIRO ML Workshop Series</li>
        <li><b>1 December 2026</b>: Topological deep learning tutorial at ACML, Melbourne</li>
        <li><b>NeurIPS 2026</b>, Sydney: presenting TopoOT</li>
      </ul>
    </aside>
  </section>

  <section class="section" aria-labelledby="dir-h">
    <div class="section-head"><h2 id="dir-h">Research directions</h2><a href="/research/">Projects and themes</a></div>
    <div class="directions">
      <div class="direction"><img src="/assets/img/projects/tdl-pipeline.jpg" alt="Diagram of topological deep learning: topological embedding, representation and loss during training, and topological analysis after training" loading="lazy">
        <h3>Topological deep learning</h3><p>Persistence-based pseudo-labels, optimal transport between persistence diagrams, and message passing on hypergraphs and cell complexes.</p></div>
      <div class="direction"><img src="/assets/img/projects/meat.jpg" alt="Hyperspectral images of steak and the abundance maps produced by different unmixing methods" loading="lazy">
        <h3>Hyperspectral and multimodal sensing</h3><p>Weak-signal unmixing and spectral 3D vision for crops, food and contamination, plus fusion with lidar and point clouds.</p></div>
      <div class="direction"><img src="/assets/img/anomaly-masks.jpg" alt="Anomaly segmentation on a bottle and a transistor, comparing heat maps, baselines and TopoTTA with the ground truth" loading="lazy">
        <h3>Reliable AI in the field</h3><p>Test-time adaptation and robustness for industrial inspection, radar perception, fault diagnosis and IVF embryo assessment.</p></div>
    </div>
  </section>

  <section class="section" aria-labelledby="pap-h">
    <div class="section-head"><h2 id="pap-h">Selected papers</h2><a href="/publications/">All publications</a></div>
    <div class="papers">{''.join(cards)}</div>
  </section>
</div>"""
    write("/", "Home", "Ali Zia is a machine learning researcher at La Trobe University working on topological deep learning, hyperspectral imaging and reliable AI for agriculture, health and industry.", body)

# ---------------------------------------------------------------- research
def build_research(projects, earlier):
    cards = []
    for p in projects:
        refs = "".join(
            f'<li>{"<a href=\"" + esc(r["url"]) + "\">" + esc(r["label"]) + "</a>" if r["url"] else esc(r["label"])}</li>'
            for r in p.get("papers", []))
        media = f'<img src="/assets/img/projects/{esc(p["image"])}" alt="{esc(p["alt"])}" loading="lazy">'
        video = f' <a href="/{esc(p["video"])}">Watch a clip</a>.' if p.get("video") else ""
        partners = f'<p class="partners">{esc(p["partners"])}</p>' if p.get("partners") else ""
        cards.append(f'<article class="project">{media}<h3>{esc(p["title"])}</h3>{partners}<p>{esc(p["text"])}{video}</p>'
                     f'{"<ul class=\"refs\">" + refs + "</ul>" if refs else ""}</article>')
    earlier_html = "".join(f"<li>{esc(e)}</li>" for e in earlier)
    body = f"""
<div class="wrap">
  <header class="page-head">
    <h1>Research</h1>
    <p>My work asks how to give learning systems structure they can trust: the shape of the data, the physics of the sensor, and the relationships between modalities. Most of it is applied with partners in agriculture, food, health and industry.</p>
  </header>

  <section class="theme">
    <div><h2>Topological deep learning</h2>
      <p>Topology describes what stays the same when data is stretched or corrupted: connected parts, loops and voids. I use persistent homology to turn anomaly maps into reliable pseudo-labels (TopoTTA, TPAMI 2026), optimal transport to compare persistence diagrams across scales (TopoOT, NeurIPS 2026), and hypergraphs and cell complexes to model relations between sensors and views in radar and fault diagnosis.</p>
      <p>I co-wrote a <a href="https://link.springer.com/article/10.1007/s10462-024-10710-9">review of topological deep learning</a> in Artificial Intelligence Review, contributed to the <a href="https://www.jmlr.org/papers/v25/24-0110.html">TopoX</a> software suite, and am teaching a tutorial on the topic at ACML 2026.</p></div>
    <img src="/assets/img/projects/tdl-pipeline.jpg" alt="Diagram of topological deep learning stages: topological embedding, representation and loss, and post-training topological analysis" loading="lazy">
  </section>

  <section class="theme">
    <div><h2>Hyperspectral and multimodal sensing</h2>
      <p>A hyperspectral camera records hundreds of narrow bands, so each pixel carries a spectrum rather than three colours. My PhD used these spectra for 3D vision, recovering depth from chromatic aberration and defocus. Since then I have worked on weak-signal unmixing for contamination in meat, protein prediction in chickpea, disease detection in sugarcane and herbicide resistance in ryegrass, and on fusing spectral data with lidar and point clouds.</p></div>
    <img src="/assets/img/projects/hsi-cube.jpg" alt="A hyperspectral image cube with the reflectance spectrum of one pixel, and a band image of a scene" loading="lazy">
  </section>

  <section class="theme">
    <div><h2>Reliable AI under real conditions</h2>
      <p>Models trained in the lab meet new lighting, sensors and populations in deployment. I work on test-time adaptation that needs no source data or labels, on diagnosing out-of-distribution robustness from representation geometry, and on decision support where errors are costly, such as embryo assessment for IVF.</p></div>
    <img src="/assets/img/anomaly-masks.jpg" alt="Anomaly segmentation results: input, ground truth, heat map, threshold baseline, TTT4AS and TopoTTA" loading="lazy">
  </section>

  <section class="section" aria-labelledby="proj-h">
    <div class="section-head"><h2 id="proj-h">Selected projects</h2></div>
    <div class="projects">{''.join(cards)}</div>
    <h3 style="font-size:1.25rem;margin:40px 0 12px">Earlier projects</h3>
    <ul class="plain measure">{earlier_html}</ul>
  </section>
</div>"""
    write("/research/", "Research", "Research themes and selected projects of Ali Zia: topological deep learning, hyperspectral imaging and reliable AI.", body)

# ---------------------------------------------------------------- publications
def build_publications(pubs):
    by_year = {}
    for p in pubs:
        by_year.setdefault(p["year"], []).append(p)
    blocks = []
    tl = dict(TOPICS)
    for year in sorted(by_year, reverse=True):
        lis = []
        for p in by_year[year]:
            links = " ".join(f'<a href="{esc(p["links"][k])}">{lab}</a>' for k, lab in
                             (("paper", "paper"), ("arxiv", "arXiv"), ("code", "code"), ("project", "project")) if p["links"].get(k))
            tags = "".join(f'<span class="tag">{tl.get(t, t)}</span>' for t in p["topics"])
            note = f'<span class="award">{esc(p["note"])}</span>' if p.get("note") else ""
            search = esc(" ".join([p["title"], p["authors"], p["venue"], p.get("short", ""), str(p["year"])] + [tl.get(t, t) for t in p["topics"]]).lower())
            lis.append(f'<li class="pub" data-type="{p["type"]}" data-topics="{" ".join(p["topics"])}" data-search="{search}">'
                       f'<span class="t">{esc(p["title"])}</span><span class="a">{bold_me(p["authors"])}</span>'
                       f'<span class="meta"><span class="v">{esc(p["venue"])}</span>{links}{note}{tags}</span></li>')
        blocks.append(f'<section class="year-block"><h2>{year}</h2><ul class="pubs">{"".join(lis)}</ul></section>')
    present_types = [t for t in TYPES if any(p["type"] == t[0] for p in pubs)]
    type_chips = '<button class="chip" type="button" data-value="all" aria-pressed="true">All types</button>' + "".join(
        f'<button class="chip" type="button" data-value="{k}" aria-pressed="false">{v}</button>' for k, v in present_types)
    topic_chips = '<button class="chip" type="button" data-value="all" aria-pressed="true">All topics</button>' + "".join(
        f'<button class="chip" type="button" data-value="{k}" aria-pressed="false">{v}</button>' for k, v in TOPICS)
    body = f"""
<div class="wrap">
  <header class="page-head">
    <h1>Publications</h1>
    <p>Papers, preprints and datasets, newest first. Citation counts and the complete record are on <a href="https://scholar.google.com/citations?user=BVBJ06QAAAAJ">Google Scholar</a>.</p>
  </header>
  <div class="filters">
    <input type="search" id="pub-search" placeholder="Search titles, authors or venues" aria-label="Search publications">
    <div class="chips" data-key="type" role="group" aria-label="Filter by type">{type_chips}</div>
    <div class="chips" data-key="topic" role="group" aria-label="Filter by topic">{topic_chips}</div>
    <span class="count" id="pub-count" aria-live="polite">{len(pubs)} papers</span>
  </div>
  {''.join(blocks)}
</div>"""
    write("/publications/", "Publications", "Publications of Ali Zia on topological deep learning, hyperspectral imaging, anomaly detection and applied machine learning.", body)

# ---------------------------------------------------------------- teaching
def build_teaching():
    body = """
<div class="wrap">
  <header class="page-head">
    <h1>Teaching and supervision</h1>
    <p>I have taught for more than a decade in Australia and Pakistan, from first-year programming to graduate courses in AI and computer vision, and I supervise research students across machine learning and imaging.</p>
  </header>
  <div class="cols section" style="padding-top:24px">
    <section class="block">
      <h2>Courses</h2>
      <ul class="entries">
        <li><div class="h">La Trobe University</div><div class="s">Data Analysis and Design (casual lecturer)</div></li>
        <li><div class="h">Griffith University</div><div class="s">Programming (casual lecturer); lab instructor over several years for Programming, Advanced Programming, Software Engineering, Software Design, Big Data Analysis, Sensor Networks and others</div></li>
        <li><div class="h">Australian National University</div><div class="s">Teaching in computing courses</div></li>
        <li><div class="h">Also taught</div><div class="s">Electric Circuits, Human–Computer Interaction, Computing for Management</div></li>
        <li><div class="h">COMSATS University, Pakistan</div><div class="s">Artificial Intelligence (eight semesters), Machine Learning (three), Computer Vision (two), Systems Programming, Advanced Operating Systems; designed the AI, Operating Systems and Systems Programming courses</div></li>
      </ul>
      <h2 style="margin-top:36px">Tutorials</h2>
      <ul class="entries">
        <li><div class="h"><a href="https://alizia369.github.io/acml2026-tdl/">Topological Deep Learning for Robust Representation Learning</a></div><div class="s">ACML 2026, Melbourne, 1 December 2026, with Usman Ali and Abdelwahed Khamis</div></li>
      </ul>
    </section>
    <section class="block">
      <h2>Supervision</h2>
      <p>I supervise PhD and honours students at La Trobe and with partner universities, and was main supervisor for a visiting PhD student at ANU who has since completed his doctorate. Recent student projects span topological deep learning, anomaly detection, radar perception and hyperspectral analysis.</p>
      <h2 style="margin-top:36px">How I teach</h2>
      <p>I try to build independent thinkers who can recover from being stuck. In lectures that means posing questions before giving answers and checking understanding as we go; in labs and projects it means real data, open-ended problems and plenty of peer discussion.</p>
      <p>I mix formal lectures with project-based, collaborative and enquiry-based learning, and use online tools where they genuinely help: recorded lectures, discussion forums and short quizzes that show students where they stand.</p>
      <p>With research students I start from their strengths, agree on a small first result, and widen from there.</p>
    </section>
  </div>
</div>"""
    write("/teaching/", "Teaching", "Teaching and supervision by Ali Zia at La Trobe, Griffith, ANU and COMSATS.", body)

# ---------------------------------------------------------------- cv
def build_cv():
    body = """
<div class="wrap">
  <header class="page-head">
    <h1>Curriculum vitae</h1>
    <p>A summary is below. The PDFs carry full details; they date from 2023 and 2024 and will be refreshed.</p>
    <div class="downloads"><a class="primary" href="/assets/cv/Ali_Zia_CV_short.pdf">Short CV (PDF)</a><a href="/assets/cv/Ali_Zia_CV_detailed.pdf">Detailed CV (PDF)</a></div>
  </header>
  <div class="cols section" style="padding-top:32px">
    <section class="block">
      <h2>Positions</h2>
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
      <h2 style="margin-top:36px">Education</h2>
      <ul class="timeline">
        <li><span class="y">2020</span><div><b>PhD in Artificial Intelligence</b>, Griffith University<br><span class="muted">Exploring extrinsic spectral properties of hyperspectral images for 3D computer vision</span></div></li>
        <li><span class="y">2009</span><div><b>Master of Computing</b>, Australian National University</div></li>
        <li><span class="y">2006</span><div><b>BSc (Hons) in Computer Science</b>, University of the Punjab</div></li>
      </ul>
    </section>
    <section class="block">
      <h2>Funding</h2>
      <ul class="timeline">
        <li><span class="y">2026</span><div>SpectraResist-AI: detecting herbicide resistance in ryegrass, La Trobe LISAF, SCEMS and LBS seed funding (lead)</div></li>
        <li><span class="y">2026</span><div>La Trobe Research Infrastructure Funding Scheme: high-speed camera</div></li>
        <li><span class="y">2023</span><div>CSIRO: protein content in chickpea varieties with hyperspectral imaging and machine learning</div></li>
        <li><span class="y">2023</span><div>CSIRO–CAS partnership: AI and hyperspectral tools for selecting salt-tolerant legumes</div></li>
        <li><span class="y">2022</span><div>CSIRO AI4M: 3D hyperspectral analysis to detect meat contamination</div></li>
      </ul>
      <h2 style="margin-top:36px">Service and recognition</h2>
      <ul class="entries">
        <li><div class="h">Tutorial organiser</div><div class="s">Topological Deep Learning, ACML 2026</div></li>
        <li><div class="h">Co-lead</div><div class="s">CSIRO ML Workshop Series</div></li>
        <li><div class="h">Runner-up paper award</div><div class="s">DICTA 2023</div></li>
        <li><div class="h">Best project award</div><div class="s">Robot path identification and map construction, 2011</div></li>
        <li><div class="h">Software</div><div class="s">Contributor to <a href="https://github.com/pyt-team">TopoX</a>; code for TopoOT, TopoTTA, MAFR and MM-HCAN on <a href="https://github.com/alizia369">GitHub</a></div></li>
      </ul>
    </section>
  </div>
</div>"""
    write("/cv/", "CV", "Curriculum vitae of Ali Zia: positions, education, funding and service.", body)

if __name__ == "__main__":
    news, pubs = load("news.json"), load("publications.json")
    proj_data = json.loads((ROOT / "data" / "projects.json").read_text(encoding="utf-8"))
    build_home(news, pubs)
    build_research(proj_data["items"], proj_data.get("earlier", []))
    build_publications(pubs)
    build_teaching()
    build_cv()
