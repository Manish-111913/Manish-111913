"""Builds every static SVG in assets/ from the CONTENT section below.

    pip install fonttools
    python scripts/build_svgs.py            # writes assets/*.svg, then refreshes the live numbers
    python scripts/build_svgs.py --offline  # skip the GitHub fetch (live numbers stay as they are)

Display text (names, section titles, big numbers) is converted to outlines with the Inter typeface,
because GitHub shows README images as <img>, where an SVG cannot load web fonts. Inter 4.0 is
downloaded once into .cache/ (it is not committed). Everything else is plain SVG <text>.

assets/activity.svg and the contribution numbers in hero.svg / about.svg are owned by
scripts/gen_activity.py, which a GitHub Action runs every hour.
"""
import argparse, io, math, os, random, re, sys, urllib.request, zipfile
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_activity as live                                               # noqa: E402
from gen_activity import (fmt, label, BG, CARD, LINE, LINE2, TEXT, MUTED, DIM,  # noqa: E402
                          BLUE, CYAN, ORANGE)
from icons import ICONS                                                   # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")
LOGIN = "Manish-111913"

# ==== CONTENT =============================================================================
HERO = {
    "kicker": "FULL STACK · CLOUD · AI",
    "first": "Kota Srirama", "last": "Manish",
    "full_name": "Kota Srirama Manish",
    "line1": "I build products end to end —",
    "line2": "from the interface to the cloud, with AI built in.",
    "terminal": "design → build → deploy → scale",
    "center": ("nodejs", "API"),
    # six services around the centre, clockwise from upper left
    "orbit": ["react", "nextjs", "postgresql", "mongodb", "docker", "aws"],
}

MARQUEE = ["FULL STACK DEVELOPMENT", "CLOUD ENGINEERING", "RETRIEVAL-AUGMENTED GENERATION",
           "LARGE LANGUAGE MODELS", "SEMANTIC SEARCH", "SYSTEM DESIGN", "SCALABLE ARCHITECTURE"]

# (number, title, subtitle). Numbers are assigned in this order, so adding a section renumbers the rest.
SECTIONS = [
    ("about", "ABOUT", "what I do, in plain words"),
    ("stack", "TECH STACK", "the tools I build with"),
    ("projects", "PROJECTS", "nine systems: what each does, how it works and why"),
    ("activity", "ACTIVITY", "real contribution data from my GitHub, not decoration"),
    ("ai", "AI ENGINEERING", "how I ground language models in real data"),
    ("contact", "CONTACT", "let's talk"),
]

ABOUT = {
    # (label, big text, caption); the live contribution card is drawn in the third slot
    "stats": [("LAYERS I BUILD ACROSS", "3", "interface, server and cloud"),
              ("TOOLS IN MY STACK", None, "from first line to deploy"),       # None = counted from STACK
              None,
              ("STUDYING", "CSE", "Computer Science student")],
    "strengths": [
        ("web", "Full stack development", ["Clean, fast interfaces on", "top of APIs that hold up", "under real traffic."], "React · Next.js · Node"),
        ("cloud", "Cloud engineering", ["Reliable infrastructure,", "serverless where it fits,", "balanced under load."], "AWS · Docker · CI/CD"),
        ("chip", "AI engineering", ["RAG pipelines, vector", "stores and custom LLM", "inference endpoints."], "RAG · LLMs · vectors"),
        ("nodes", "System design", ["Decoupled backend parts", "that scale under load", "without a rewrite."], "decoupled · scalable"),
    ],
    "loop_title": "HOW I WORK",
    "loop_note": "then repeat, better",
    "loop": [("Design", "plan the system first"), ("Build", "ship a working version"),
             ("Deploy", "automate it to the cloud"), ("Scale", "fix the slow parts")],
}

STACK = [
    ("LANGUAGES", "how I write code", [("cpp", "C++"), ("java", "Java"), ("javascript", "JavaScript"),
                                       ("typescript", "TypeScript"), ("html", "HTML5"), ("css", "CSS3")]),
    ("FRONTEND", "the screens people see", [("react", "React"), ("nextjs", "Next.js"), ("tailwind", "Tailwind CSS"),
                                            ("bootstrap", "Bootstrap")]),
    ("BACKEND & DATA", "REST, WebSockets, storage", [("nodejs", "Node.js"), ("express", "Express"), ("postgresql", "PostgreSQL"),
                                                     ("mysql", "MySQL"), ("mongodb", "MongoDB"), ("redis", "Redis")]),
    ("CLOUD", "where it all runs", [("aws", "AWS"), ("vercel", "Vercel"), ("netlify", "Netlify"),
                                    ("firebase", "Firebase"), ("render", "Render")]),
    ("DEVOPS & TOOLS", "build, ship, automate", [("docker", "Docker"), ("jenkins", "Jenkins"), ("githubactions", "CI/CD"),
                                                 ("git", "Git"), ("github", "GitHub"), ("vscode", "VS Code")]),
    ("AI-NATIVE EDITORS", "where I pair with AI", [("cursor", "Cursor"), ("antigravity", "Antigravity")]),
]
LEARNING = ["Deep learning", "Container orchestration", "Multi-agent systems"]

from projects import PROJECTS                                             # noqa: E402  (one entry per assets/proj-N.svg)

AI = {
    "cards": [
        {"title": "semantic-search", "tag": "FOCUS",
         "desc": ["Finds text by meaning, not by keywords: the", "query and every document become vectors."],
         "visual": "vectors",
         "stats": [("k=5", "nearest neighbours", "returned for each query"), ("cos θ", "similarity score", "angle between two vectors")],
         "pills": ["Embeddings", "Dense vectors", "Cosine similarity", "Vector stores"],
         "pills2": ["Semantic indices", "Text parsing", "Chunking"]},
        {"title": "two-stage-retrieval", "tag": "FOCUS",
         "desc": ["A fast bi-encoder pulls candidates; a precise", "cross-encoder reranks them for the LLM."],
         "visual": "funnel",
         "stats": [("100", "candidates", "fast recall"), ("5", "passages", "precise rerank")],
         "pills": ["Bi-encoders", "Cross-encoders", "Reranking", "RAG"],
         "pills2": ["LLM inference", "Custom endpoints", "Workflows"]},
    ],
    "steps_title": "HOW A RAG ANSWER IS BUILT",
    "steps": ["Chunk and embed", "Retrieve top-k", "Rerank", "Answer with sources"],
    "steps_note": "goal: every answer traces back to a source",
}

CONTACT = [
    ("portfolio", "Portfolio", "see my work"),
    ("linkedin", "LinkedIn", "let's connect"),
    ("resume", "Resume", "one-page CV"),
    ("github", "GitHub", LOGIN),
    ("email", "Email", "say hello"),
]

FOOTER = ("Design it. Build it. Ship it. Scale it.", "thanks for stopping by  ·  built with hand-written SVG")


# ==== fonts ===============================================================================
INTER_ZIP = "https://github.com/rsms/inter/releases/download/v4.0/Inter-4.0.zip"
CACHE = os.path.join(ROOT, ".cache", "inter")
WEIGHTS = ["Medium", "SemiBold", "Bold", "ExtraBold"]
_fonts = {}


def ensure_fonts():
    if all(os.path.exists(os.path.join(CACHE, f"Inter-{w}.ttf")) for w in WEIGHTS):
        return
    os.makedirs(CACHE, exist_ok=True)
    print("downloading Inter 4.0 ...")
    with urllib.request.urlopen(INTER_ZIP, timeout=120) as r:
        z = zipfile.ZipFile(io.BytesIO(r.read()))
    for w in WEIGHTS:
        with open(os.path.join(CACHE, f"Inter-{w}.ttf"), "wb") as f:
            f.write(z.read(f"extras/ttf/Inter-{w}.ttf"))


def font(weight):
    if weight not in _fonts:
        from fontTools.ttLib import TTFont
        t = TTFont(os.path.join(CACHE, f"Inter-{weight}.ttf"))
        _fonts[weight] = (t, t.getGlyphSet(), t.getBestCmap(), t["head"].unitsPerEm)
    return _fonts[weight]


def text_width(s, size, weight="Medium", ls=0):
    _, gs, cmap, upm = font(weight)
    return sum(gs[cmap[ord(c)]].width for c in s) * size / upm + ls * (len(s) - 1)


def mono_width(s, size, ls=0):
    return len(s) * (size * 0.6 + ls)


def outline(s, x, y, size, weight="Bold", ls=0, anchor="start", fill=TEXT, extra=""):
    """Text as one <path>. Returns (svg, width)."""
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    _, gs, cmap, upm = font(weight)
    w = text_width(s, size, weight, ls)
    cx = x - (w if anchor == "end" else w / 2 if anchor == "middle" else 0)
    sc = size / upm
    pen = SVGPathPen(gs, lambda v: ("%.1f" % v).rstrip("0").rstrip("."))
    for c in s:
        g = gs[cmap[ord(c)]]
        g.draw(TransformPen(pen, (sc, 0, 0, -sc, cx, y)))
        cx += g.width * sc + ls
    return f'<path d="{pen.getCommands()}" fill="{fill}" {extra}/>', w


# ==== shared pieces =======================================================================
DEFS = """
<linearGradient id="gAcc" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4D9FFF"/><stop offset="1" stop-color="#34E2E8"/></linearGradient>
<linearGradient id="gAccV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4D9FFF"/><stop offset="1" stop-color="#2B6FD1"/></linearGradient>
<linearGradient id="gCard" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0D1526"/><stop offset="1" stop-color="#080D18"/></linearGradient>
<linearGradient id="gSheen" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4D9FFF" stop-opacity="0"/><stop offset=".5" stop-color="#4D9FFF" stop-opacity=".9"/><stop offset="1" stop-color="#34E2E8" stop-opacity="0"/></linearGradient>
<filter id="glow" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="glowS" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="1.6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0H0V30" stroke="#1A2744" stroke-width="1" opacity=".55"/></pattern>
<pattern id="dots" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#2A3A63" opacity=".8"/></pattern>
<linearGradient id="gAg" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#3B82F6"/><stop offset=".45" stop-color="#EA4335"/><stop offset=".75" stop-color="#FBBC05"/><stop offset="1" stop-color="#34A853"/></linearGradient>
"""


def svg(name, W, H, title, desc, body, extra_defs=""):
    out = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
           f'aria-label="{escape(title)}" fill="none">\n<title>{escape(title)}</title>\n<desc>{escape(desc)}</desc>\n'
           f'<defs>\n{DEFS}\n{extra_defs}\n</defs>\n{body}\n</svg>\n')
    with open(os.path.join(ASSETS, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(out)
    print("wrote", name)


def mono(s, x, y, size, color, anchor="start", weight=500, ls=0):
    return label(s, x, y, size, color, anchor, weight, ls, mono=True)


def icon(key, cx, cy, scale, color=None):
    """A 24x24 brand icon centred on (cx, cy)."""
    off = 12 * scale
    if key == "antigravity":   # not in Simple Icons: a rising arch in Google colours
        return (f'<g transform="translate({fmt(cx-off)} {fmt(cy-off)}) scale({fmt(scale)})">'
                f'<path d="M3.2 21.5C3.2 11.2 7 3 12 3S20.8 11.2 20.8 21.5" stroke="url(#gAg)" stroke-width="3.4" stroke-linecap="round"/>'
                f'<path d="M8.6 21.5C8.6 15.6 10.1 11.4 12 11.4S15.4 15.6 15.4 21.5" stroke="url(#gAg)" stroke-width="2.2" stroke-linecap="round" opacity=".7"/></g>')
    col, d = ICONS[key]
    return f'<path transform="translate({fmt(cx-off)} {fmt(cy-off)}) scale({fmt(scale)})" d="{d}" fill="{color or col}"/>'


def icon_color(key):
    return "#EA4335" if key == "antigravity" else ICONS[key][0]


def pill(s, x, y, primary=True, size=11):
    w = text_width(s, size, "Medium") + 20
    fill, stroke, col = ("#0B1A33", "#24406E", TEXT) if primary else ("#0A1120", LINE2, MUTED)
    return (f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="24" rx="12" fill="{fill}" stroke="{stroke}"/>'
            + label(s, x + 10, y + 15.85, size, col)), w


def pill_row(items, x, y, primary=True, gap=7):
    o = []
    for s in items:
        p, w = pill(s, x, y, primary)
        o.append(p)
        x += w + gap
    return "".join(o), x


def tag(s, x, y):
    w = mono_width(s, 10, 0.2) + 18
    return (f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="24" rx="12" fill="#09142A" stroke="#1C3560"/>'
            + label(s, x + 9, y + 15.5, 10, BLUE, ls=0.2, mono=True))


# ==== hero ================================================================================
def hero():
    W, H = 900, 340
    rnd = random.Random(7)
    o = [f'<g clip-path="url(#hc)"><rect width="{W}" height="{H}" fill="{BG}"/>',
         f'<rect width="{W}" height="{H}" fill="url(#grid)" mask="url(#gm)"/>',
         '<ellipse cx="735" cy="180" rx="300" ry="230" fill="url(#blobB)"/>',
         '<ellipse cx="90" cy="330" rx="280" ry="150" fill="url(#blobC)"/>']
    for _ in range(34):
        x, y = rnd.randint(525, 890), rnd.randint(15, 320)
        r = rnd.choice([0.8, 1, 1.2, 1.6])
        o.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#9CC6FF" opacity=".2"><animate attributeName="opacity" '
                 f'values=".08;.65;.08" dur="{rnd.uniform(2.5, 5.5):.1f}s" begin="{rnd.uniform(0.3, 2.9):.1f}s" repeatCount="indefinite" /></circle>')
    C = (735, 185)
    sats = [(638, 117), (755, 69), (842, 135), (846, 225), (745, 303), (628, 235)]
    for a, b in zip(sats, sats[1:] + sats[:1]):
        o.append(f'<path d="M{a[0]} {a[1]} L{b[0]} {b[1]}" stroke="{LINE2}" stroke-width="1" stroke-dasharray="3 5" opacity=".7"/>')
    for i, (x, y) in enumerate(sats):
        out_p, back_p = f"M{C[0]} {C[1]} L{x} {y}", f"M{x} {y} L{C[0]} {C[1]}"
        b1, b2 = i * 0.45, i * 0.45 + 1.35
        o.append(f'<path d="{out_p}" stroke="{LINE2}" stroke-width="1.4"/>')
        o.append(f'<circle r="3" fill="{BLUE}" filter="url(#glowS)" opacity="0"><set attributeName="opacity" to="1" begin="{b1:.2f}s"/>'
                 f'<animateMotion dur="2.7s" begin="{b1:.2f}s" repeatCount="indefinite" path="{out_p}"/></circle>')
        o.append(f'<circle r="2.4" fill="{CYAN}" filter="url(#glowS)" opacity="0"><set attributeName="opacity" to=".9" begin="{b2:.2f}s"/>'
                 f'<animateMotion dur="2.7s" begin="{b2:.2f}s" repeatCount="indefinite" path="{back_p}"/></circle>')
    for b in ("0.0", "1.5"):
        o.append(f'<circle cx="{C[0]}" cy="{C[1]}" r="30" stroke="{BLUE}" stroke-width="1.4" opacity="0"><animate attributeName="r" values="30;86" dur="3s" begin="{b}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values=".55;0" dur="3s" begin="{b}s" repeatCount="indefinite"/></circle>')
    for i, ((x, y), key) in enumerate(zip(sats, HERO["orbit"])):
        o.append(f'<circle cx="{x}" cy="{y}" r="21" fill="#0A1120" stroke="{LINE2}" stroke-width="1.2"/>')
        o.append(icon(key, x, y, 0.83))
        o.append(f'<circle cx="{x}" cy="{y}" r="21" stroke="{BLUE}" stroke-width="1.4" opacity="0"><animate attributeName="opacity" '
                 f'values="0;.9;0;0" keyTimes="0;.08;.22;1" dur="5.4s" begin="{i*0.9:.1f}s" repeatCount="indefinite" /></circle>')
    o.append(f'<circle cx="{C[0]}" cy="{C[1]}" r="32" fill="#0B1830" stroke="{BLUE}" stroke-width="1.6" filter="url(#glow)"/>')
    o.append(icon(HERO["center"][0], C[0], C[1], 1.25))
    o.append(mono(HERO["center"][1], C[0], 237, 9.5, DIM, "middle", 600, 2))

    o.append(f'<circle cx="54" cy="55" r="3.5" fill="{BLUE}"><animate attributeName="opacity" values="1;.25;1" dur="2s" repeatCount="indefinite"/></circle>')
    o.append(mono(HERO["kicker"], 66, 59, 11.5, BLUE, weight=600, ls=2.2))
    o.append(f"<!--live-badge-->{live.hero_badge(0)}<!--/live-badge-->")
    o.append(outline(HERO["first"], 50, 138, 66, "ExtraBold", ls=-1)[0])
    o.append(outline(HERO["last"], 50, 205, 66, "ExtraBold", ls=-1, fill="url(#nameG)")[0])
    o.append(f'<rect x="-200" y="80" width="90" height="140" fill="url(#gSheen)" opacity=".13" transform="skewX(-18)"><animateTransform '
             f'attributeName="transform" type="translate" values="-200 0;800 0" dur="7s" repeatCount="indefinite" additive="sum"/></rect>')
    o.append(label(HERO["line1"], 50, 236, 17, TEXT))
    o.append(label(HERO["line2"], 50, 259, 15, MUTED))
    o.append(f'<rect x="50" y="282" width="402" height="36" rx="10" fill="#070B14" stroke="{LINE}"/>')
    for cx, c in ((66, "#FF5F57"), (80, "#FEBC2E"), (94, "#28C840")):
        o.append(f'<circle cx="{cx}" cy="300" r="3.6" fill="{c}" opacity=".85"/>')
    o.append(mono(HERO["terminal"], 116, 304.5, 12.5, "#BFD6FF"))
    o.append(f'<rect x="{fmt(116 + len(HERO["terminal"]) * 7.87)}" y="292" width="7" height="16" fill="{CYAN}"><animate attributeName="opacity" '
             f'values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.1s" repeatCount="indefinite"/></rect>')
    o.append("</g>")
    o.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="20" stroke="{LINE2}"/>')
    extra = f"""
<radialGradient id="blobB" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#4D9FFF" stop-opacity=".30"/><stop offset="1" stop-color="#4D9FFF" stop-opacity="0"/></radialGradient>
<radialGradient id="blobC" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#34E2E8" stop-opacity=".14"/><stop offset="1" stop-color="#34E2E8" stop-opacity="0"/></radialGradient>
<radialGradient id="fade" cx="0.78" cy="0.5" r="0.62"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#000"/></radialGradient>
<mask id="gm"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>
<clipPath id="hc"><rect width="{W}" height="{H}" rx="20"/></clipPath>
<linearGradient id="nameG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4D9FFF"/><stop offset="1" stop-color="#34E2E8"/></linearGradient>
"""
    svg("hero.svg", W, H, f"{HERO['full_name']} — full stack, cloud and AI engineer",
        "Animated hero banner: a web of services around an API, with live data packets.", "\n".join(o), extra)


# ==== marquee =============================================================================
def marquee():
    W, H = 900, 46
    items, x = [], 1.0
    for s in MARQUEE:
        p, w = outline(s, x, 28, 12.3, "SemiBold", ls=2.73, fill=MUTED)
        items.append(p)
        x += w + 34.6
        items.append(f'<path d="M{fmt(x)} 22 l4 -4 l4 4 l-4 4 z" fill="{BLUE}"/>')
        x += 8 + 34.9
    span = x - 1
    sets = "".join(f'<g transform="translate({fmt(span*k)} 0)">' + "".join(items) + "</g>" if k else "<g>" + "".join(items) + "</g>"
                   for k in range(3))
    body = (f'<clipPath id="mc"><rect width="{W}" height="{H}" rx="12"/></clipPath><linearGradient id="mfade" x1="0" x2="1">'
            f'<stop offset="0" stop-color="{BG}"/><stop offset=".08" stop-color="{BG}" stop-opacity="0"/><stop offset=".92" stop-color="{BG}" stop-opacity="0"/>'
            f'<stop offset="1" stop-color="{BG}"/></linearGradient>\n<g clip-path="url(#mc)"><rect width="{W}" height="{H}" fill="#060A13"/>\n'
            f'<g>{sets}<animateTransform attributeName="transform" type="translate" from="0 0" to="-{fmt(span)} 0" dur="{span/38:.1f}s" repeatCount="indefinite"/></g>\n'
            f'<rect width="{W}" height="{H}" fill="url(#mfade)"/></g>\n<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="12" stroke="{LINE}"/>')
    svg("marquee.svg", W, H, "Focus areas", "Scrolling ticker of focus areas.", body)


# ==== section headers =====================================================================
def headers(sections):
    for n, (key, title, sub) in enumerate(sections, 1):
        W, H = 900, 64
        num = f"{n:02d}"
        t, tw = outline(title, 78, 39.5, 20, "Bold", ls=3.8)
        x0 = 78 + tw + 23
        x1 = 876 - text_width(sub, 12.5) - 24
        travel = max(x1 - x0 - 90, 0)
        body = [f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="#060A13" stroke="{LINE}"/>',
                f'<rect x="18.5" y="18.5" width="44" height="28" rx="8" fill="#0A1426" stroke="{LINE2}"/>',
                mono(num, 40.5, 37, 12.5, BLUE, "middle", 700, 1), t,
                label(sub, 876, 37, 12.5, MUTED, "end"),
                f'<path d="M{fmt(x0)} 32.5 H{fmt(x1)}" stroke="{LINE2}" stroke-width="1"/>',
                f'<rect x="{fmt(x0)}" y="31.5" width="90" height="2" rx="1" fill="url(#gSheen)" opacity="0"><set attributeName="opacity" to="1" begin="0s"/>'
                f'<animateTransform attributeName="transform" type="translate" values="0 0;{fmt(travel)} 0;0 0" dur="5s" repeatCount="indefinite" '
                f'calcMode="spline" keyTimes="0;.5;1" keySplines=".45 0 .55 1;.45 0 .55 1"/></rect>']
        svg(f"h-{key}.svg", W, H, f"{num} {title}", f"{num} {title}", "\n".join(body))


# ==== about ===============================================================================
def strength_icon(kind):
    if kind == "web":       # browser window whose layout blocks keep loading in
        return ('<rect x="3" y="6" width="38" height="32" rx="5" fill="#0B1830" stroke="#4D9FFF" stroke-width="2.4"/>'
                '<path d="M3 14 H41" stroke="#4D9FFF" stroke-width="2"/>'
                '<circle cx="8.5" cy="10" r="1.3" fill="#4D9FFF"/><circle cx="13" cy="10" r="1.3" fill="#4D9FFF"/><circle cx="17.5" cy="10" r="1.3" fill="#4D9FFF"/>'
                '<rect x="8" y="19" width="28" height="4" rx="2" fill="#34E2E8"><animate attributeName="width" values="0;28;28;0" keyTimes="0;.3;.85;1" dur="3.6s" repeatCount="indefinite"/></rect>'
                '<rect x="8" y="26" width="12" height="7" rx="2" fill="#4D9FFF" opacity=".8"><animate attributeName="opacity" values="0;0;.8;.8;0" keyTimes="0;.25;.45;.85;1" dur="3.6s" repeatCount="indefinite"/></rect>'
                '<rect x="23" y="26" width="13" height="7" rx="2" fill="#4D9FFF" opacity=".5"><animate attributeName="opacity" values="0;0;.5;.5;0" keyTimes="0;.4;.6;.85;1" dur="3.6s" repeatCount="indefinite"/></rect>')
    if kind == "cloud":     # a cloud with a build rising into it
        return ('<path d="M12.5 33 H33 A8 8 0 0 0 34 17.1 A11 11 0 0 0 13.2 15.3 A9 9 0 0 0 12.5 33 Z" fill="#0B1830" stroke="#4D9FFF" stroke-width="2.4" stroke-linejoin="round"/>'
                '<g stroke="#34E2E8" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M22 29 V20 M18 24 L22 20 L26 24"/>'
                '<animateTransform attributeName="transform" type="translate" values="0 6;0 -1;0 -1;0 6" keyTimes="0;.35;.8;1" dur="2.8s" repeatCount="indefinite"/>'
                '<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.35;.8;1" dur="2.8s" repeatCount="indefinite"/></g>'
                '<path d="M12 40 H32" stroke="#223157" stroke-width="2" stroke-linecap="round"/>')
    if kind == "chip":
        return ('<g stroke="#4D9FFF" stroke-width="2" stroke-linecap="round"><path d="M16 6 V11 M16 33 V38 M6 16 H11 M33 16 H38"/><path d="M22 6 V11 M22 33 V38 M6 22 H11 M33 22 H38"/>'
                '<path d="M28 6 V11 M28 33 V38 M6 28 H11 M33 28 H38"/></g><rect x="10" y="10" width="24" height="24" rx="5" fill="#0B1830" stroke="#4D9FFF" stroke-width="2.4"/>'
                '<rect x="16" y="16" width="12" height="12" rx="2.5" fill="#4D9FFF"><animate attributeName="opacity" values=".25;.9;.25" dur="2.2s" repeatCount="indefinite"/></rect>'
                '<path d="M38 2 l1.6 3.6 l3.6 1.6 l-3.6 1.6 l-1.6 3.6 l-1.6 -3.6 l-3.6 -1.6 l3.6 -1.6 z" fill="#34E2E8"><animate attributeName="opacity" values="1;.2;1" dur="1.8s" repeatCount="indefinite"/></path>')
    # nodes: three services, one request travelling between them
    return ('<path d="M22 7 L7 34" stroke="#223157" stroke-width="1.8"/><path d="M7 34 L37 34" stroke="#223157" stroke-width="1.8"/><path d="M37 34 L22 7" stroke="#223157" stroke-width="1.8"/>'
            '<circle r="2.6" fill="#34E2E8" filter="url(#glowS)"><animateMotion dur="3s" repeatCount="indefinite" path="M22 7 L37 34 L7 34 Z"/></circle>'
            '<circle cx="22" cy="7" r="5.5" fill="#0B1830" stroke="#4D9FFF" stroke-width="2"/><circle cx="7" cy="34" r="5.5" fill="#0B1830" stroke="#4D9FFF" stroke-width="2"/>'
            '<circle cx="37" cy="34" r="5.5" fill="#0B1830" stroke="#4D9FFF" stroke-width="2"/><circle cx="22" cy="7" r="5.5" stroke="#4D9FFF" stroke-width="1.4" opacity="0">'
            '<animate attributeName="r" values="5.5;15" dur="2.4s" repeatCount="indefinite"/><animate attributeName="opacity" values=".8;0" dur="2.4s" repeatCount="indefinite"/></circle>')


def about():
    W, H = 900, 482
    o = []
    tools = sum(len(r[2]) for r in STACK)
    for i, st in enumerate(ABOUT["stats"]):
        x = i * 230
        if st is None:      # live contribution card, kept current by gen_activity.py
            assert x == live.ABOUT_LIVE_X
            o.append(f'<rect x="{x+.5}" y="0.5" width="209" height="103" rx="14" fill="#120B0A" stroke="#4A2616" />')
            o.append(mono("CONTRIBUTIONS", x + 22, 28, 10, ORANGE, weight=600, ls=1.6))
            o.append(f"<!--live-num-->{live.about_number(0)}<!--/live-num-->")
            o.append(f"<!--live-sub-->{live.about_sub(0)}<!--/live-sub-->")
            o.append(f'<circle cx="{x+186}" cy="26" r="4" fill="{ORANGE}" filter="url(#glowS)"><animate attributeName="opacity" values="1;.3;1" dur="1.6s" repeatCount="indefinite"/></circle>')
            continue
        lab, big, cap = st
        big = big or str(tools)
        o.append(f'<rect x="{x+.5}" y="0.5" width="209" height="103" rx="14" fill="url(#gCard)" stroke="{LINE}" />')
        o.append(mono(lab, x + 22, 28, 10, DIM, weight=600, ls=1.6))
        o.append(outline(big, x + 21, 71, 42, "ExtraBold", ls=-0.45, fill="url(#gAcc)")[0])
        o.append(label(cap, x + 22, 92, 12, MUTED))
    for i, (kind, title, lines, tg) in enumerate(ABOUT["strengths"]):
        x = i * 230
        o.append(f'<rect x="{x+.5}" y="124.5" width="209" height="217" rx="14" fill="url(#gCard)" stroke="{LINE}" />')
        o.append(f'<rect x="{x+1}" y="125" width="70" height="2" rx="1" fill="url(#gSheen)" opacity="0"><set attributeName="opacity" to="1" begin="{i*0.7:.1f}s"/>'
                 f'<animateTransform attributeName="transform" type="translate" values="0 0;138 0;0 0" dur="6s" begin="{i*0.7:.1f}s" repeatCount="indefinite"/></rect>')
        o.append(f'<g transform="translate({x+22} 148)">{strength_icon(kind)}</g>')
        o.append(label(title, x + 22, 222, 15.5, TEXT, weight=700))
        for k, ln in enumerate(lines):
            o.append(label(ln, x + 22, 245 + k * 18, 12.5, MUTED))
        o.append(tag(tg, x + 18, 304))
    # the loop
    o.append(f'<rect x="0.5" y="366.5" width="899" height="115" rx="14" fill="url(#gCard)" stroke="{LINE}" />')
    o.append(mono(ABOUT["loop_title"], 26, 394, 10.5, DIM, weight=600, ls=2.2))
    loop = "M48 456 L840 456 Q856 456 856 440 L856 436 Q856 420 840 420 L64 420 Q48 420 48 436 L48 456"
    o.append(f'<path d="M48 456 L840 456 Q856 456 856 440 L856 436 Q856 420 840 420 L64 420 Q48 420 48 436 L48 456" stroke="{LINE2}" stroke-width="1.5" stroke-dasharray="2 6" stroke-linecap="round"/>')
    o.append(f'<rect x="372" y="411" width="156" height="18" fill="{CARD}"/>')
    o.append(mono(ABOUT["loop_note"], 450, 424, 11, DIM, "middle"))
    o.append(f'<circle r="3.6" fill="{CYAN}" filter="url(#glow)"><animateMotion dur="9s" repeatCount="indefinite" path="{loop}"/></circle>')
    for i, (t, s) in enumerate(ABOUT["loop"]):
        cx = 70 + i * 222
        o.append(f'<circle cx="{cx}" cy="456" r="17" fill="#0B1830" stroke="{BLUE}" stroke-width="1.6"/>')
        o.append(mono(i + 1, cx, 460.6, 13, BLUE, "middle", 700))
        o.append(f'<circle cx="{cx}" cy="456" r="17" stroke="{CYAN}" stroke-width="1.6" opacity="0"><animate attributeName="opacity" values="0;1;0;0" '
                 f'keyTimes="0;.06;.2;1" dur="9s" begin="{fmt(i*2.15)}s" repeatCount="indefinite"/></circle>')
        o.append(label(t, cx + 28, 454, 14, TEXT, weight=700))
        o.append(label(s, cx + 28, 471, 11.5, MUTED))
    svg("about.svg", W, H, "Strengths and numbers",
        "Four headline numbers, four engineering strengths and the design-build-deploy-scale loop.", "\n".join(o))


# ==== stack ===============================================================================
def stack():
    W = 900
    H = 22 + len(STACK) * 98 + 4
    o = [f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="18" fill="{CARD}" stroke="{LINE}" />',
         f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="17" fill="url(#dots)" opacity=".35"/>']
    total = sum(len(r[2]) for r in STACK)
    k = 0
    for r, (lab, sub, tiles) in enumerate(STACK):
        y = 22 + r * 98
        o.append(f'<rect x="28" y="{y+14}" width="3" height="40" rx="1.5" fill="url(#gAccV)"/>')
        o.append(mono(lab, 44, y + 31, 11, TEXT, weight=700, ls=1.6))
        o.append(label(sub, 44, y + 51, 12.5, MUTED))
        for i, (key, name) in enumerate(tiles):
            x = 224 + i * 108
            t0 = round(k / total * 0.84, 3)
            o.append(f'<rect x="{x}" y="{y}" width="96" height="82" rx="14" fill="#0A1120" stroke="#18223A" stroke-width="1.2"><animate attributeName="stroke" '
                     f'values="#18223A;{icon_color(key)};#18223A;#18223A" keyTimes="0;{t0+0.02:.3f};{t0+0.09:.3f};1" dur="10s" repeatCount="indefinite"/></rect>')
            o.append(icon(key, x + 48, y + 31, 1.33))
            o.append(label(name, x + 48, y + 68, 11, TEXT, "middle", 600))
            k += 1
        if r == len(STACK) - 1:          # "currently learning" fills the rest of the last row
            x = 224 + len(tiles) * 108
            bw = 860 - x
            o.append(f'<rect x="{x}" y="{y}" width="{bw}" height="82" rx="14" fill="#091428" stroke="#1C3560"/>')
            o.append(f'<circle cx="{x+22}" cy="{y+24}" r="3.4" fill="{CYAN}"><animate attributeName="opacity" values="1;.25;1" dur="2s" repeatCount="indefinite"/></circle>')
            o.append(mono("CURRENTLY LEARNING", x + 36, y + 28, 10.5, CYAN, weight=700, ls=1.8))
            px = x + 20
            for s in LEARNING:
                w = text_width(s, 11) + 20
                o.append(f'<rect x="{fmt(px)}" y="{y+44}" width="{fmt(w)}" height="26" rx="13" fill="#0B1A33" stroke="#24406E"/>'
                         + label(s, px + 10, y + 60.85, 11, TEXT))
                px += w + 8
            assert px - 8 <= x + bw - 16, "learning pills overflow"
    names = "; ".join(f"{lab.title()}: " + ", ".join(n for _, n in tiles) for lab, _, tiles in STACK)
    svg("stack.svg", W, H, "Tech stack", "Logos of the languages, frameworks, databases, cloud platforms and tools I use. " + names, "\n".join(o))


# ==== projects ============================================================================
# The nine projects are described in scripts/projects.py; this section only draws them.
KIND_LEGEND = [("io", "input / output"), ("proc", "step"), ("hot", "core step"), ("store", "data store"),
               ("ext", "external service"), ("decision", "decision"), ("planned", "planned"), ("unverified", "not verified")]
EXT = "#9B8CFF"
BADGE = {"warn": ("#1A140A", "#5A4317", "#FFC66B"), "gold": ("#1A160A", "#5A4A17", "#FFD866"),
         "blue": ("#0A1426", LINE2, "#9CC6FF")}
EDGE = "#2E4372"


def wrap(text, width, size, weight="Medium"):
    lines, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if cur and text_width(t, size, weight) > width:
            lines.append(cur)
            cur = word
        else:
            cur = t
    return lines + ([cur] if cur else [])


def _port(nd, side):
    x, y, w, h = nd["x"], nd["y"], nd["w"], nd["h"]
    return {"l": (x, y + h / 2), "r": (x + w, y + h / 2), "t": (x + w / 2, y), "b": (x + w / 2, y + h)}[side]


def _route(nodes, e):
    sa, sb = e.get("sa", "r"), e.get("sb", "l")
    p1, p2 = _port(nodes[e["a"]], sa), _port(nodes[e["b"]], sb)
    if "ay" in e:                      # attach at a given height on a tall node
        p1 = (p1[0], e["ay"])
    if "by" in e:
        p2 = (p2[0], e["by"])
    if e.get("via"):
        return [p1] + list(e["via"]) + [p2]
    if sa in "lr" and sb in "lr":
        if abs(p1[1] - p2[1]) < .5 and "mx" not in e:
            return [p1, p2]
        mx = e.get("mx", (p1[0] + p2[0]) / 2)
        return [p1, (mx, p1[1]), (mx, p2[1]), p2]
    if sa in "tb" and sb in "tb":
        if abs(p1[0] - p2[0]) < .5 and "my" not in e:
            return [p1, p2]
        my = e.get("my", (p1[1] + p2[1]) / 2)
        return [p1, (p1[0], my), (p2[0], my), p2]
    if abs(p1[0] - p2[0]) < .5 or abs(p1[1] - p2[1]) < .5:
        return [p1, p2]
    if sa in "lr":
        return [p1, (p2[0], p1[1]), p2]
    return [p1, (p1[0], p2[1]), p2]


def _rounded(pts, r=8):
    """Polyline with rounded corners, as path data."""
    d = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    for (x0, y0), (x1, y1), (x2, y2) in zip(pts, pts[1:], pts[2:]):
        l1, l2 = math.hypot(x1 - x0, y1 - y0), math.hypot(x2 - x1, y2 - y1)
        rr = min(r, l1 / 2, l2 / 2)
        ax, ay = x1 - (x1 - x0) / l1 * rr, y1 - (y1 - y0) / l1 * rr
        bx, by = x1 + (x2 - x1) / l2 * rr, y1 + (y2 - y1) / l2 * rr
        d += f" L{fmt(ax)} {fmt(ay)} Q{fmt(x1)} {fmt(y1)} {fmt(bx)} {fmt(by)}"
    return d + f" L{fmt(pts[-1][0])} {fmt(pts[-1][1])}"


def _shape(kind, x, y, w, h, rx=None):
    """Outline of one node."""
    fill, stroke, sw, dash = "#0A1120", LINE2, 1, ""
    if kind == "hot":
        fill, stroke, sw = "#0B1830", BLUE, 1.4
    elif kind == "ext":
        stroke = EXT
    elif kind == "planned":
        fill, dash = "#070C17", ' stroke-dasharray="5 4"'
    elif kind == "unverified":
        fill, stroke, dash = "#070C17", "#5F6C8A", ' stroke-dasharray="1.5 3.5" stroke-linecap="round"'
    if kind == "store":
        e = min(6, h / 4)
        return (f'<path d="M{fmt(x)} {fmt(y+e)} A{fmt(w/2)} {fmt(e)} 0 0 1 {fmt(x+w)} {fmt(y+e)} V{fmt(y+h-e)} A{fmt(w/2)} {fmt(e)} 0 0 1 {fmt(x)} {fmt(y+h-e)} Z" fill="{fill}" stroke="{stroke}"/>'
                f'<path d="M{fmt(x)} {fmt(y+e)} A{fmt(w/2)} {fmt(e)} 0 0 0 {fmt(x+w)} {fmt(y+e)}" stroke="{stroke}"/>')
    if kind == "decision":
        cx, cy = x + w / 2, y + h / 2
        return (f'<path d="M{fmt(cx)} {fmt(y)} L{fmt(x+w)} {fmt(cy)} L{fmt(cx)} {fmt(y+h)} L{fmt(x)} {fmt(cy)} Z" '
                f'fill="#0B1426" stroke="{BLUE}" stroke-width="1.2" stroke-linejoin="round"/>')
    if rx is None:
        rx = h / 2 if kind == "io" else 10
    out = f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{fmt(h)}" rx="{fmt(rx)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{dash}/>'
    if kind == "ext":
        out += f'<rect x="{fmt(x+3)}" y="{fmt(y+3)}" width="{fmt(w-6)}" height="{fmt(h-6)}" rx="{fmt(max(rx-2.5, 1))}" stroke="{EXT}" stroke-opacity=".35"/>'
    return out


def _node(nd, errors):
    x, y, w, h, kind = nd["x"], nd["y"], nd["w"], nd["h"], nd.get("kind", "proc")
    o = [_shape(kind, x, y, w, h)]
    title, sub = nd["t"], nd.get("s")
    if kind == "decision":
        lines = title.split("\n")
        for i, ln in enumerate(lines):
            if text_width(ln, 11.5, "SemiBold") > w * 0.66:
                errors.append(f"decision '{ln}' too wide for w={w}")
            o.append(label(ln, x + w / 2, y + h / 2 + 4 + (i - (len(lines) - 1) / 2) * 13, 11.5, TEXT, "middle", 600))
        return "".join(o)
    tx = x + 12
    if nd.get("icon"):
        o.append(icon(nd["icon"], x + 24, y + h / 2, 0.8))
        tx = x + 44
    elif kind == "io":
        o.append(f'<circle cx="{fmt(x+15)}" cy="{fmt(y+h/2)}" r="3.2" fill="{BLUE}"/>')
        tx = x + 26
    room = x + w - tx - 8
    if text_width(title, 13, "SemiBold") > room:
        errors.append(f"title '{title}' needs {text_width(title, 13, 'SemiBold'):.0f}px, has {room:.0f}")
    if sub and mono_width(sub, 10) > room + 4:
        errors.append(f"sub '{sub}' needs {mono_width(sub, 10):.0f}px, has {room:.0f}")
    ty = y + h / 2 + (-1 if sub else 4.5)
    if kind in ("planned", "unverified"):
        ty += 4
        o.append(mono("PLANNED" if kind == "planned" else "NOT VERIFIED", tx, y + 13, 7.5, DIM, weight=600, ls=1))
    o.append(label(title, tx, ty, 13, DIM if kind in ("planned", "unverified") else TEXT, weight=600))
    if sub:
        o.append(mono(sub, tx, ty + 14, 10, DIM if kind in ("planned", "unverified") else MUTED))
    if kind == "hot":
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" stroke="{BLUE}" stroke-width="1.4" opacity="0"><animate attributeName="opacity" values="0;.9;0" dur="3.2s" repeatCount="indefinite"/>'
                 f'<animate attributeName="stroke-width" values="1;5;1" dur="3.2s" repeatCount="indefinite"/></rect>')
    return "".join(o)


def _edge(i, pts, e):
    d = _rounded(pts)
    (x1, y1), (x2, y2) = pts[-2], pts[-1]
    ang = math.atan2(y2 - y1, x2 - x1)
    c, s = math.cos(ang), math.sin(ang)
    a1 = (x2 - 6 * c - 3.2 * s, y2 - 6 * s + 3.2 * c)
    a2 = (x2 - 6 * c + 3.2 * s, y2 - 6 * s - 3.2 * c)
    dash = ' stroke-dasharray="4 4"' if e.get("dashed") else ""
    o = (f'<path d="{d}" stroke="{EDGE}" stroke-width="1.5" stroke-linecap="round"{dash}/>'
         f'<polygon points="{fmt(x2)},{fmt(y2)} {fmt(a1[0])},{fmt(a1[1])} {fmt(a2[0])},{fmt(a2[1])}" fill="{EDGE}"/>')
    if not e.get("dashed"):
        length = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))
        b0 = f"{(i * 0.37) % 3:.2f}"
        o += (f'<circle r="3" fill="{BLUE}" filter="url(#glowS)" opacity="0"><set attributeName="opacity" to="1" begin="{b0}s"/>'
              f'<animateMotion dur="{max(1.2, length / 75):.1f}s" begin="{b0}s" repeatCount="indefinite" path="{d}" calcMode="linear"/></circle>')
    if e.get("label"):
        if e.get("lpos"):
            lx, ly = e["lpos"]
        else:
            k = len(pts) // 2
            lx, ly = (pts[k - 1][0] + pts[k][0]) / 2, (pts[k - 1][1] + pts[k][1]) / 2
        tw = mono_width(e["label"], 9)
        o += (f'<rect x="{fmt(lx-tw/2-4)}" y="{fmt(ly-7.5)}" width="{fmt(tw+8)}" height="14" rx="4" fill="#050912" stroke="#16203A"/>'
              + mono(e["label"], lx, ly + 3, 9, "#8B99B8", "middle", 600))
    return o


def _legend_mark(kind, sx, sy):
    if kind == "store":
        return (f'<path d="M{sx} {sy+2} A8 2.5 0 0 1 {sx+16} {sy+2} V{sy+9} A8 2.5 0 0 1 {sx} {sy+9} Z" fill="#0A1120" stroke="{LINE2}"/>'
                f'<path d="M{sx} {sy+2} A8 2.5 0 0 0 {sx+16} {sy+2}" stroke="{LINE2}"/>')
    if kind == "decision":
        return f'<path d="M{sx+8} {sy-1} L{sx+16} {sy+5} L{sx+8} {sy+11} L{sx} {sy+5} Z" fill="#0B1426" stroke="{BLUE}"/>'
    if kind == "ext":
        return f'<rect x="{sx}" y="{sy}" width="16" height="10" rx="3" fill="#0A1120" stroke="{EXT}"/>'
    return _shape(kind, sx, sy, 16, 10, rx=5 if kind == "io" else 3)


def diagram(dg, errors):
    """Everything inside the diagram box, in box coordinates (843 wide)."""
    nodes = {nd["id"]: nd for nd in dg["nodes"]}
    g = []
    for gx, gy, gw, gh, gl in dg.get("groups", []):
        g.append(f'<rect x="{gx}" y="{gy}" width="{gw}" height="{gh}" rx="10" fill="#0A1222" fill-opacity=".6" stroke="#1A2540"/>')
        g.append(mono(gl, gx + 12, gy + 15, 9, "#6F7D9C", weight=600, ls=1.6))
    for x, y, s in dg.get("labels", []):
        g.append(mono(s, x, y, 9, "#6F7D9C", weight=600, ls=1.6))
    for i, e in enumerate(dg.get("edges", [])):
        g.append(_edge(i, _route(nodes, e), e))
    for nd in dg["nodes"]:
        g.append(_node(nd, errors))
    for x, y, s in dg.get("notes", []):
        g.append(mono(s, x, y, 9, DIM))
    for cy, lab, items, style in dg.get("chips", []):
        g.append(mono(lab, 18, cy + 14.5, 9, "#6F7D9C", weight=600, ls=1.6))
        cx = 18 + mono_width(lab, 9, 1.6) + 8
        for it in items:
            w = text_width(it, 10.5) + 18
            if style == "planned":
                g.append(f'<rect x="{fmt(cx)}" y="{cy}" width="{fmt(w)}" height="21" rx="10.5" fill="#070C17" stroke="#3A4A6E" stroke-dasharray="4 3"/>'
                         + label(it, cx + 9, cy + 14.5, 10.5, DIM))
            else:
                g.append(f'<rect x="{fmt(cx)}" y="{cy}" width="{fmt(w)}" height="21" rx="10.5" fill="#0B1A33" stroke="#24406E"/>'
                         + label(it, cx + 9, cy + 14.5, 10.5, TEXT))
            cx += w + 6
        if cx > 843:
            errors.append(f"chip row '{lab}' overflows by {cx-843:.0f}px")
    used = {nd.get("kind", "proc") for nd in dg["nodes"]}
    lx, ly = 828, dg["h"] - 11
    for kind, name in reversed(KIND_LEGEND):
        if kind in used:
            g.append(mono(name, lx, ly, 9, DIM, "end"))
            lx -= mono_width(name, 9) + 22
            g.append(_legend_mark(kind, lx, ly - 8))
            lx -= 14
    return "".join(g)


def _badge(b, x, y):
    txt, style = b
    fill, stroke, col = BADGE[style]
    w = mono_width(txt, 9.5, 1.2) + 20
    return (f'<rect x="{fmt(x)}" y="{y}" width="{fmt(w)}" height="20" rx="10" fill="{fill}" stroke="{stroke}"/>'
            + mono(txt, x + 10, y + 13.8, 9.5, col, weight=600, ls=1.2))


def project_card(n, p):
    """Desktop card: header, problem, flow diagram, stack, key decision and trade-off."""
    W, errors, o = 900, [], []
    o.append(outline(f"{n:02d}", 24, 64, 44, "ExtraBold", fill="none", extra='stroke="#2C4276" stroke-width="1.3"')[0])
    t, tw = outline(p["name"], 112, 47.3, 29.8, "SemiBold")
    o.append(t)
    if p.get("badge"):
        o.append(_badge(p["badge"], 112 + tw + 14, 28))
    o.append(label(p["subtitle"], 112, 72, 13, MUTED))
    for i, key in enumerate(reversed(p["icons"])):
        cx = 856 - i * 40
        o.append(f'<circle cx="{cx}" cy="48" r="17" fill="#0A1120" stroke="{LINE2}"/>' + icon(key, cx, 48, 0.75))
    if p.get("icons") and 112 + tw + 14 + (mono_width(p["badge"][0], 9.5, 1.2) + 20 if p.get("badge") else 0) > 856 - 40 * len(p["icons"]) - 4:
        errors.append("title + badge collide with the icons")
    desc = wrap(p["problem"], 844, 14)
    if len(desc) > 3:
        errors.append(f"problem text is {len(desc)} lines")
    for i, ln in enumerate(desc):
        o.append(label(ln, 28, 107 + i * 20, 14, "#C9D3EA"))
    y0 = 107 + (len(desc) - 1) * 20 + 22
    dg = p["diagram"]
    dh = dg["h"]
    o.append(f'<rect x="28.5" y="{y0+.5}" width="843" height="{dh}" rx="14" fill="#050912" stroke="{LINE}"/>')
    o.append(f'<rect x="29" y="{y0+1}" width="842" height="{dh-1}" rx="13" fill="url(#dots)" opacity=".45"/>')
    o.append(f'<g transform="translate(28 {y0})">{diagram(dg, errors)}</g>')
    # stack, grouped by role
    y = y0 + dh + 30
    o.append(mono("STACK", 30, y, 9.5, BLUE, weight=700, ls=2))
    x0 = x = 92
    for role, items in p["stack"]:
        rw = mono_width(role.upper(), 9, 1.4)
        iw = text_width(items, 12)
        if x > x0 and x + rw + 8 + iw > 872:
            x, y = x0, y + 22
        o.append(mono(role.upper(), x, y, 9, DIM, weight=600, ls=1.4))
        o.append(label(items, x + rw + 8, y + .5, 12, "#C9D3EA"))
        x += rw + 8 + iw + 24
    if p.get("stack_note"):
        y += 20
        o.append(mono(p["stack_note"], x0, y, 9.5, DIM))
    y += 22
    o.append(f'<path d="M28.5 {y}.5 H871.5" stroke="{LINE}"/>')
    y += 30
    dec, tra = wrap(p["decision"][1], 404, 13), wrap(p["tradeoff"][1], 396, 13)
    o.append(mono("KEY DECISION", 30, y, 10.5, BLUE, weight=700, ls=2))
    o.append(mono(p["decision"][0], 30 + mono_width("KEY DECISION", 10.5, 2) + 8, y, 8.5, DIM, weight=600, ls=1))
    o.append(mono("TRADE-OFF", 474, y, 10.5, MUTED, weight=700, ls=2))
    o.append(mono(p["tradeoff"][0], 474 + mono_width("TRADE-OFF", 10.5, 2) + 8, y, 8.5, DIM, weight=600, ls=1))
    for i, ln in enumerate(dec):
        o.append(label(ln, 30, y + 24 + i * 19, 13, TEXT))
    for i, ln in enumerate(tra):
        o.append(label(ln, 474, y + 24 + i * 19, 13, MUTED))
    rows = max(len(dec), len(tra))
    o.append(f'<path d="M450.5 {y-12} V{y+24+(rows-1)*19+8}" stroke="{LINE}"/>')
    H = int(y + 24 + (rows - 1) * 19 + 28)
    o.insert(0, f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="18" fill="url(#gCard)" stroke="{LINE}" />')
    if errors:
        raise SystemExit(f"proj-{n} ({p['name']}) layout problems:\n  " + "\n  ".join(errors))
    svg(f"proj-{n}.svg", W, H, f"{p['name']} — architecture", f"{p['name']}: {p['subtitle']}. {p['problem']}", "\n".join(o))
    project_card_mobile(n, p)


def readme_projects():
    """Rewrite the block between <!--projects--> and <!--/projects--> in README.md from PROJECTS."""
    out = ['<p align="center"><img src="./assets/h-projects.svg" alt="Projects" width="100%"></p>', ""]
    for n, p in enumerate(PROJECTS, 1):
        out += ['<p align="center">', "<picture>",
                f'<source media="(max-width: 700px)" srcset="./assets/proj-{n}-m.svg">',
                f'<img src="./assets/proj-{n}.svg" alt="{escape(p["name"])}: {escape(p["summary"])}" width="100%">',
                "</picture>", "</p>", ""]
        if p["links"]:
            out += ['<p align="center">', "\n&nbsp;·&nbsp;\n".join(f'<a href="{u}"><b>{t}</b></a>' for t, u in p["links"]), "</p>", ""]
        out += ["<details>", f"<summary><b>How {p['name']} works</b>, step by step</summary>", ""]
        for i, st in enumerate(p["steps"], 1):
            note = {"planned": " *(planned)*", "unverified": " *(not verified)*"}.get(st["kind"], "")
            sep = " " if st["t"].endswith("?") and not note else ": "
            out.append(f"{i}. **{st['t']}**{note}{sep}{st['m']}")
        out += ["", "| Part | Technology |", "| --- | --- |"]
        out += [f"| {role} | {items} |" for role, items in p["stack"]]
        chips = p["diagram"].get("chips", [])
        built = [", ".join(items) for _, _, items, style in chips if style == "built"]
        planned = [", ".join(items) for _, _, items, style in chips if style == "planned"]
        extra = []
        if built:
            extra.append(f"**Also built:** {'; '.join(built)}.")
        if planned:
            extra.append(f"**Planned, not built yet:** {'; '.join(planned)}.")
        if p.get("stack_note"):
            extra.append(f"*{p['stack_note']}*")
        if extra:
            out += [""] + [e + "<br>" if i < len(extra) - 1 else e for i, e in enumerate(extra)]
        out += ["", "</details>", "", "<br>", ""]
    path = os.path.join(ROOT, "README.md")
    s = open(path, encoding="utf-8").read()
    block = "<!--projects-->\n" + "\n".join(out) + "<!--/projects-->"
    s, k = re.subn(r"<!--projects-->.*?<!--/projects-->", lambda m: block, s, flags=re.S)
    assert k == 1, "README.md needs one <!--projects--> ... <!--/projects--> block"
    open(path, "w", encoding="utf-8", newline="\n").write(s)
    print("wrote README.md projects block")


def project_card_mobile(n, p):
    """Phone version: the same story with the flow stacked top to bottom."""
    W, o, X, CW = 480, [], 20, 440
    o.append(outline(f"{n:02d}", 18, 50, 32, "ExtraBold", fill="none", extra='stroke="#2C4276" stroke-width="1.2"')[0])
    name_lines = wrap(p["name"], CW - 62, 22, "SemiBold")
    y = 42
    for ln in name_lines:
        o.append(outline(ln, 82, y, 22, "SemiBold")[0])
        y += 26
    y -= 4
    for ln in wrap(p["subtitle"], CW - 62, 12.5):
        o.append(label(ln, 82, y, 12.5, MUTED))
        y += 18
    if p.get("badge"):
        o.append(_badge(p["badge"], 82, y - 6))
        y += 24
    y += 14
    for ln in wrap(p["problem"], CW, 14):
        o.append(label(ln, X, y, 14, "#C9D3EA"))
        y += 20
    y += 14
    o.append(mono("HOW IT FLOWS", X, y, 9.5, BLUE, weight=700, ls=2))
    y += 12
    tags = {"store": "DATA", "decision": "DECISION", "ext": "EXTERNAL", "planned": "PLANNED", "unverified": "NOT VERIFIED"}
    for i, st in enumerate(p["steps"]):
        kind = st.get("kind", "proc")
        subs = wrap(st["m"], CW - 60, 11.5)
        h = 32 + 16 * len(subs)
        o.append(_shape(kind if kind in ("planned", "unverified", "hot", "ext") else "proc", X, y, CW, h, rx=12))
        o.append(f'<circle cx="{X+20}" cy="{y+20}" r="10" fill="#0B1830" stroke="{BLUE}" stroke-width="1.2"/>'
                 + mono(i + 1, X + 20, y + 24, 10, BLUE, "middle", 700))
        o.append(label(st["t"], X + 40, y + 25, 13.5, DIM if kind in ("planned", "unverified") else TEXT, weight=600))
        if kind in tags:
            o.append(mono(tags[kind], X + CW - 12, y + 24, 8.5, EXT if kind == "ext" else DIM, "end", 600, 1))
        for k, ln in enumerate(subs):
            o.append(label(ln, X + 40, y + 43 + k * 16, 11.5, MUTED))
        y += h
        if i < len(p["steps"]) - 1:
            o.append(f'<path d="M{X+20} {y+3} V{y+11}" stroke="{EDGE}" stroke-width="1.5"/><polygon points="{X+20},{y+15} {X+16.5},{y+9} {X+23.5},{y+9}" fill="{EDGE}"/>')
            y += 18
    y += 34
    o.append(mono("STACK", X, y, 9.5, BLUE, weight=700, ls=2))
    y += 22
    for role, items in p["stack"]:
        o.append(mono(role.upper(), X, y, 9, DIM, weight=600, ls=1.2))
        for k, ln in enumerate(wrap(items, CW - 128, 12)):
            o.append(label(ln, X + 128, y + k * 17, 12, "#C9D3EA"))
        y += 17 * len(wrap(items, CW - 128, 12)) + 5
    if p.get("stack_note"):
        for ln in wrap(p["stack_note"], CW, 10.5):
            o.append(label(ln, X, y + 2, 10.5, DIM))
            y += 15
    for head, (tg, text), col, hc in (("KEY DECISION", p["decision"], TEXT, BLUE), ("TRADE-OFF", p["tradeoff"], MUTED, MUTED)):
        y += 18
        o.append(f'<path d="M{X} {y-2}.5 H{X+CW}" stroke="{LINE}"/>')
        y += 26
        o.append(mono(head, X, y, 10.5, hc, weight=700, ls=2) + mono(tg, X + mono_width(head, 10.5, 2) + 8, y, 8.5, DIM, weight=600, ls=1))
        y += 24
        for ln in wrap(text, CW, 13):
            o.append(label(ln, X, y, 13, col))
            y += 19
    H = int(y + 10)
    o.insert(0, f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="18" fill="url(#gCard)" stroke="{LINE}" />')
    svg(f"proj-{n}-m.svg", W, H, f"{p['name']} — architecture", f"{p['name']}: {p['subtitle']}. {p['problem']}", "\n".join(o))


# ==== AI engineering ======================================================================
def vectors_visual():
    """A 2-D slice of embedding space: a query lands, its nearest neighbours light up."""
    rnd = random.Random(11)
    centres = [(70, 128, "#2D5FB0"), (196, 116, "#2D5FB0"), (110, 196, "#2D5FB0"), (214, 192, "#2D5FB0")]
    pts = []
    for cx, cy, _ in centres:
        for _ in range(22):
            a, r = rnd.uniform(0, 6.283), abs(rnd.gauss(0, 1)) * 17
            x, y = cx + math.cos(a) * r * 1.3, cy + math.sin(a) * r
            if 44 <= x <= 246 and 106 <= y <= 216:
                pts.append((x, y))
    q = (182, 160)
    near = sorted(pts, key=lambda p: math.hypot(p[0] - q[0], p[1] - q[1]))[:5]
    o = [f'<rect x="24" y="96" width="236" height="140" rx="10" fill="#050912" stroke="{LINE}"/>',
         f'<path d="M36 224 H248 M36 224 V106" stroke="{LINE2}" stroke-width="1"/>']
    for p in pts:
        if p in near:
            continue
        o.append(f'<circle cx="{fmt(p[0])}" cy="{fmt(p[1])}" r="3" fill="#1B2A4C"/>')
    o.append(f'<circle cx="{q[0]}" cy="{q[1]}" r="6" stroke="{CYAN}" stroke-width="1.2" opacity="0"><animate attributeName="r" values="6;40" dur="3.2s" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values=".8;0" dur="3.2s" repeatCount="indefinite"/></circle>')
    for i, p in enumerate(near):
        t = 0.12 + i * 0.08
        o.append(f'<path d="M{q[0]} {q[1]} L{fmt(p[0])} {fmt(p[1])}" stroke="{BLUE}" stroke-width="1.2" stroke-dasharray="2 3" opacity="0">'
                 f'<animate attributeName="opacity" values="0;0;.9;.9;0" keyTimes="0;{t:.2f};{t+.05:.2f};.85;1" dur="3.2s" repeatCount="indefinite"/></path>')
        o.append(f'<circle cx="{fmt(p[0])}" cy="{fmt(p[1])}" r="3.4" fill="#1B2A4C"><animate attributeName="fill" values="#1B2A4C;#1B2A4C;#4D9FFF;#4D9FFF;#1B2A4C" '
                 f'keyTimes="0;{t:.2f};{t+.05:.2f};.85;1" dur="3.2s" repeatCount="indefinite"/></circle>')
    o.append(f'<path d="M{q[0]} {q[1]-7} l7 7 l-7 7 l-7 -7 z" fill="{CYAN}" filter="url(#glowS)"/>')
    o.append(mono("query", q[0] + 10, q[1] - 9, 9.5, CYAN, weight=600))
    o.append(mono("embedding space", 248, 234, 9, DIM, "end"))
    return "".join(o)


def funnel_visual():
    """Candidates narrowing stage by stage."""
    rows = [("corpus · every chunk", 224, "#16264A", TEXT), ("bi-encoder · top 100", 190, "#1F4A8F", TEXT),
            ("cross-encoder · top 5", 156, "#2F74D6", TEXT), ("LLM answer", 104, "#34E2E8", BG)]
    o = []
    for i, (name, w, col, tc) in enumerate(rows):
        y = 98 + i * 32
        x = 142 - w / 2
        assert text_width(name, 11, "SemiBold") < w - 16, name
        o.append(f'<rect x="{fmt(x)}" y="{y}" width="{w}" height="24" rx="8" fill="{col}"/>')
        o.append(f'<rect x="{fmt(x)}" y="{y}" width="{w}" height="24" rx="8" fill="#fff" opacity="0"><animate attributeName="opacity" '
                 f'values="0;.3;0;0" keyTimes="0;{.06+i*.14:.2f};{.16+i*.14:.2f};1" dur="4s" repeatCount="indefinite"/></rect>')
        o.append(label(name, 142, y + 16, 11, tc, "middle", 600))
        if i < 3:
            o.append(f'<path d="M142 {y+25} V{y+31}" stroke="{LINE2}" stroke-width="1.4"/>')
    o.append(mono("illustrative", 30, 238, 9, DIM))
    return "".join(o)


def ai():
    W, H = 900, 428
    o = []
    for c, card in enumerate(AI["cards"]):
        g = [f'<rect x="0.5" y="0.5" width="439" height="327" rx="16" fill="url(#gCard)" stroke="{LINE}" />',
             mono(card["title"], 24, 36, 13.5, BLUE, weight=700)]
        tw = mono_width(card["tag"], 10, 1.5) + 20
        g.append(f'<rect x="{fmt(416-tw)}" y="20" width="{fmt(tw)}" height="22" rx="11" fill="#0A1120" stroke="{LINE2}"/>'
                 + mono(card["tag"], 426 - tw, 34.5, 10, MUTED, ls=1.5))
        for i, ln in enumerate(card["desc"]):
            g.append(label(ln, 24, 62 + i * 18, 13, "#C9D3EA"))
        g.append(vectors_visual() if card["visual"] == "vectors" else funnel_visual())
        for i, (big, l1, l2) in enumerate(card["stats"]):
            y = 131 + i * 67
            g.append(outline(big, 282, y, 42, "ExtraBold", ls=-0.45, fill="url(#gAcc)")[0])
            g.append(label(l1, 282, y + 12, 12.5, TEXT, weight=600))
            g.append(label(l2, 282, y + 27, 11, DIM))
        row, _ = pill_row(card["pills"], 24, 252)
        row2, _ = pill_row(card["pills2"], 24, 284, primary=False)
        g += [row, row2]
        o.append(f'<g transform="translate({c*460} 0)">' + "\n".join(g) + "</g>")
    s = [f'<rect x="0.5" y="0.5" width="899" height="83" rx="16" fill="url(#gCard)" stroke="{LINE}" />',
         mono(AI["steps_title"], 24, 32, 10.5, DIM, weight=600, ls=2),
         f'<circle r="3.4" fill="{CYAN}" filter="url(#glow)"><animateMotion dur="6s" repeatCount="indefinite" path="M44 58 L852 58"/></circle>']
    for i, st in enumerate(AI["steps"]):
        cx = 44 + i * 214
        end = cx + 20 + text_width(st, 13, "SemiBold") + 10
        nxt = cx + 214 - 17 if i < len(AI["steps"]) - 1 else 852
        s.insert(2, f'<path d="M{fmt(end)} 58 L{fmt(nxt)} 58" stroke="{LINE2}" stroke-width="1.4" stroke-dasharray="2 6" stroke-linecap="round"/>')
        s.append(f'<circle cx="{cx}" cy="58" r="11" fill="#0B1830" stroke="{BLUE}" stroke-width="1.4"/>' + mono(i + 1, cx, 62, 11, BLUE, "middle", 700))
        s.append(label(st, cx + 20, 62.5, 13, TEXT, weight=600))
    s.append(mono(AI["steps_note"], 876, 32, 11, MUTED, "end"))
    o.append('<g transform="translate(0 344)">' + "\n".join(s) + "</g>")
    svg("ai.svg", W, H, "AI engineering",
        "Semantic search over embeddings, two-stage retrieval with a bi-encoder and a cross-encoder, and how a RAG answer is built.", "\n".join(o))


# ==== contact pills =======================================================================
PILL_ICONS = {
    "portfolio": ('<g transform="translate(14 16)" stroke="#4D9FFF" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="10"/>'
                  '<ellipse cx="12" cy="12" rx="4.2" ry="10"/><path d="M2 12H22 M4 6.5H20 M4 17.5H20" stroke-width="1.4"/></g>'),
    "resume": ('<g transform="translate(14 16)" stroke="#34E2E8" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
               '<path d="M5 1.5H14.5L20 7V22.5H5Z"/><path d="M14.5 1.5V7H20"/><path d="M8.5 12H16.5 M8.5 15.5H16.5 M8.5 19H13" stroke-width="1.5"/></g>'),
    "linkedin": ('<path transform="translate(14 16) scale(1)" d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" fill="#3B8FE0"/>'),
    "github": f'<path transform="translate(14 16) scale(1)" d="{ICONS["github"][1]}" fill="#F2F5FA"/>',
    "email": ('<path transform="translate(14 16) scale(1)" d="M24 5.457v13.909c0 .904-.732 1.636-1.636 1.636h-3.819V11.73L12 16.64l-6.545-4.91v9.273H1.636A1.636 1.636 0 0 1 0 19.366V5.457c0-2.023 2.309-3.178 3.927-1.964L5.455 4.64 12 9.548l6.545-4.91 1.528-1.145C21.69 2.28 24 3.434 24 5.457z" fill="#EA4335"/>'),
}


def pills():
    for i, (key, name, sub) in enumerate(CONTACT):
        body = (f'<rect x=".5" y=".5" width="163" height="55" rx="14" fill="#0A1120" stroke="{LINE2}"><animate attributeName="stroke" '
                f'values="{LINE2};{BLUE};{LINE2};{LINE2}" keyTimes="0;.08;.2;1" dur="8s" begin="{i*0.9:.1f}s" repeatCount="indefinite"/></rect>'
                + PILL_ICONS[key] + label(name, 50, 25, 14, TEXT, weight=700) + mono(sub, 50, 42, 10.5, MUTED))
        svg(f"pill-{key}.svg", 164, 56, name, name, body)


# ==== footer ==============================================================================
def footer():
    W, H = 900, 170
    line, sub = FOOTER
    waves = []
    for start, base, amp, col, op, frm, to, dur in ((-300, 122, 12, BLUE, .22, "0 0", "-300 0", 9),
                                                    (-225, 134, 10, CYAN, .16, "-225 0", "0 0", 13),
                                                    (-180, 146, 9, BLUE, .3, "0 0", "-180 0", 7)):
        half = -start / 2
        d = f"M{start} {base} Q{fmt(start+half/2)} {base-amp} {fmt(start+half)} {base}"
        x = start + half
        while x < W + 1000:
            x += half
            d += f" T{fmt(x)} {base}"
        d += f" V180 H{start} Z"
        waves.append(f'<path d="{d}" fill="{col}" opacity="{op}"><animateTransform attributeName="transform" type="translate" '
                     f'from="{frm}" to="{to}" dur="{dur}s" repeatCount="indefinite"/></path>')
    body = (f'<clipPath id="fc"><rect width="{W}" height="{H}" rx="20"/></clipPath><g clip-path="url(#fc)"><rect width="{W}" height="{H}" fill="{BG}"/>\n'
            f'<rect width="{W}" height="{H}" fill="url(#grid)" opacity=".25"/>\n'
            + outline(line, 450, 62.3, 25, "Bold", ls=-0.15, anchor="middle")[0] + "\n"
            + mono(sub, 450, 90, 12, MUTED, "middle") + "\n" + "\n".join(waves)
            + f'\n</g>\n<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="20" stroke="{LINE2}"/>')
    svg("footer.svg", W, H, line, line, body)


# ==== main ================================================================================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true", help="do not fetch live contribution numbers")
    a = ap.parse_args()
    ensure_fonts()
    os.makedirs(ASSETS, exist_ok=True)
    sections = [s for s in SECTIONS if s[0] != "projects" or PROJECTS]
    hero(); marquee(); headers(sections); about(); stack(); ai(); pills(); footer()
    for n, p in enumerate(PROJECTS, 1):
        project_card(n, p)
    if PROJECTS:
        readme_projects()
    if not a.offline:
        live.main(["--login", LOGIN, "--out", os.path.join(ASSETS, "activity.svg"), "--assets", ASSETS])


if __name__ == "__main__":
    main()
