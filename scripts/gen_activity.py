"""Commit-activity SVG generator. Standard library only, so it can run inside a GitHub Action.

    python scripts/gen_activity.py --login Manish-111913 --out assets/activity.svg --assets assets
    python scripts/gen_activity.py --json contrib.json --end 2026-10-13 --login Manish-111913 --out activity.svg   # offline
"""
import argparse, datetime as dt, re, json, sys, urllib.request
from collections import Counter
from html import escape
# Inter ExtraBold digits, outlined at 100px (baseline y=0). Generated.
GLYPHS = {'0': (69.2, 'M34.6 1C53.9 1 65.1 -12.8 65.1 -36.3C65.1 -59.8 53.8 -73.7 34.6 -73.7C15.3 -73.7 4 -59.9 4 -36.3C4 -12.8 15.3 1 34.6 1ZM34.6 -13.1C26.3 -13.1 21.8 -21.4 21.8 -36.3C21.8 -51.3 26.4 -59.7 34.6 -59.7C42.9 -59.7 47.4 -51.3 47.4 -36.3C47.4 -21.4 42.9 -13.1 34.6 -13.1Z'), '1': (44.1, 'M38.5 -72.8H20.7L4.4 -61.6V-46.5L20.8 -57.8H21.3V0H38.5Z'), '2': (63.8, 'M5.4 0H59V-13.9H29.3V-14.4L38.4 -22.8C54.1 -36.5 58.1 -43.5 58.1 -51.8C58.1 -64.8 47.5 -73.7 31.1 -73.7C15.1 -73.7 4.4 -64.5 4.4 -49.8H20.8C20.8 -56.3 24.9 -60.2 31.1 -60.2C37.1 -60.2 41.4 -56.5 41.4 -50.5C41.4 -45 37.9 -41.2 31.9 -35.7L5.4 -12.4Z'), '3': (65.7, 'M32.7 1C49.7 1 61.6 -8 61.6 -20.6C61.6 -29.6 55.9 -36 44.7 -37.4V-37.9C53.1 -39.2 59 -44.8 59 -52.9C59 -64.7 48.4 -73.7 32.9 -73.7C17.3 -73.7 5.8 -64.7 5.7 -51.8H22.3C22.3 -56.9 26.9 -60.2 32.9 -60.2C38.5 -60.2 42.3 -56.8 42.3 -51.9C42.3 -46.7 37.8 -43.2 31.3 -43.2H24.3V-30.9H31.3C38.8 -30.9 43.6 -27.2 43.6 -21.9C43.6 -16.7 39.2 -13.1 32.8 -13.1C26.5 -13.1 21.7 -16.4 21.6 -21.2H4.3C4.4 -8.2 16.2 1 32.7 1Z'), '4': (68.8, 'M4.5 -12.2H39.6V0H56.2V-12.2H64.9V-25.8H56.2V-72.8H34.4L4.5 -25.6ZM40 -25.8H21.7V-26.4L39.4 -54.4H40Z'), '5': (65.2, 'M33.2 1C50 1 61.2 -9.7 61.2 -24.6C61.2 -38.5 51.5 -48.3 38.5 -48.3C31.7 -48.3 26 -45.5 23.5 -41.5H23.1L24.8 -58.8H56.9V-72.8H10.6L7.4 -33.7L22.7 -30.8C24.7 -34 28.7 -36 33 -36C39.8 -36 44.5 -31.2 44.5 -24.1C44.5 -17 39.8 -12.4 33.2 -12.4C27.4 -12.4 22.6 -15.9 22.5 -21.2H5.7C6 -8.3 17.3 1 33.2 1Z'), '6': (66.2, 'M34.1 1C50.7 1 62.2 -9.5 62.2 -24.7C62.2 -38.1 52.9 -47.9 39.9 -47.9C31.8 -47.9 24.6 -44 21.5 -37.5H21C21 -50.6 25.5 -59 34.5 -59C39.5 -59 43.3 -56.5 44.4 -51.8H61.3C60 -64 49.6 -73.7 34.5 -73.7C16.1 -73.7 4 -59.1 4 -35.1C4 -8.5 18.3 1 34.1 1ZM34 -12.4C27.5 -12.4 22.7 -17.5 22.7 -24.1C22.7 -30.7 27.6 -35.8 34 -35.8C40.7 -35.8 45.5 -30.8 45.5 -24.1C45.5 -17.4 40.6 -12.4 34 -12.4Z'), '7': (58.8, 'M8.2 0H26L55.6 -58.6V-72.8H3.2V-58.8H37.6V-58.3Z'), '8': (66.4, 'M33.2 1C50.1 1 62.4 -7.9 62.4 -19.6C62.4 -28.7 55.1 -36 46.1 -37.5V-37.9C54 -39.5 59.8 -46 59.8 -54.1C59.8 -65.4 48.5 -73.7 33.2 -73.7C17.9 -73.7 6.6 -65.4 6.6 -54.1C6.6 -46.1 12.3 -39.5 20.3 -37.9V-37.5C11.1 -36 4 -28.7 4 -19.6C4 -7.9 16.3 1 33.2 1ZM33.2 -11.3C26.6 -11.3 22.1 -15.4 22.1 -21.1C22.1 -26.9 26.8 -31 33.2 -31C39.6 -31 44.3 -26.8 44.3 -21.1C44.3 -15.3 39.7 -11.3 33.2 -11.3ZM33.2 -43.2C27.6 -43.2 23.5 -47 23.5 -52.1C23.5 -57.4 27.5 -61 33.2 -61C38.9 -61 42.9 -57.4 42.9 -52.1C42.9 -46.9 38.8 -43.2 33.2 -43.2Z'), '9': (66.2, 'M31.7 1.1C50.1 1.1 62.2 -13.6 62.2 -37.7C62.2 -64.3 47.9 -73.8 32.1 -73.9C15.5 -73.9 4 -63.3 4 -48.1C4 -34.6 13.2 -24.9 26.3 -24.9C34.4 -24.9 41.7 -28.8 44.7 -35.3H45.1C45.1 -22.1 40.7 -13.6 31.7 -13.6C26.7 -13.6 22.9 -16.3 21.8 -21H4.8C6.2 -8.7 16.6 1.1 31.7 1.1ZM32.1 -37C25.5 -37 20.8 -41.9 20.8 -48.7C20.8 -55.3 25.7 -60.4 32.2 -60.4C38.8 -60.4 43.6 -55.2 43.6 -48.7C43.6 -42.1 38.7 -37 32.1 -37Z')}


# ---- palette (matches the rest of the profile) ------------------------------------------
BG, CARD, LINE, LINE2 = "#04060B", "#080D18", "#16203A", "#223157"
TEXT, MUTED, DIM = "#E9EEFB", "#98A4BD", "#5F6C8A"
BLUE, CYAN, ORANGE = "#4D9FFF", "#34E2E8", "#FF6B35"
SANS = "Inter, 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"
LEVELS = ["#0D1526", "#143A6E", "#1F63B8", "#3B8BF2", "#9AD0FF"]

# where the live number sits in hero.svg / about.svg (build_svgs.py lays the rest out around it)
HERO_BADGE_X, HERO_BADGE_Y = 290, 40
ABOUT_LIVE_X = 460


def fmt(v):
    return ("%.2f" % v).rstrip("0").rstrip(".")


def label(s, x, y, size=12, color=MUTED, anchor="start", weight=500, ls=0, mono=False):
    fam = MONO if mono else SANS
    lsa = f' letter-spacing="{ls}"' if ls else ""
    return (f'<text x="{fmt(x)}" y="{fmt(y)}" font-family="{fam}" font-size="{size}" font-weight="{weight}" '
            f'fill="{color}" text-anchor="{anchor}"{lsa}>{escape(str(s))}</text>')


def number_width(s, size):
    return sum(GLYPHS[c][0] for c in s) * size / 100.0


def big_number(s, size, x, y, fill, anchor="start", extra=""):
    sc = size / 100.0
    width = number_width(s, size)
    cx = x - (width if anchor == "end" else width / 2 if anchor == "middle" else 0)
    out = f'<g fill="{fill}" {extra}>'
    for c in s:
        adv, d = GLYPHS[c]
        out += f'<path transform="translate({fmt(cx)} {fmt(y)}) scale({sc})" d="{d}"/>'
        cx += adv * sc
    return out + "</g>", width


# ---- data --------------------------------------------------------------------------------
def _attr(tag, name):
    m = re.search(r'\b' + re.escape(name) + r'="([^"]*)"', tag)
    return m.group(1) if m else None


def parse_calendar(html):
    """Parse GitHub's public contributions fragment into {iso_date: count} for every day shown."""
    ids = {}
    for tag in re.findall(r'<td\b[^>]*data-date="[^"]*"[^>]*>', html):
        ids[_attr(tag, "id")] = _attr(tag, "data-date")
    counts = {d: 0 for d in ids.values()}
    for m in re.finditer(r'<tool-tip\b([^>]*)>([^<]*)</tool-tip>', html):
        fid = _attr(m.group(1), "for")
        if fid in ids:
            n = re.match(r"\s*(\d+)\s+contribution", m.group(2))
            counts[ids[fid]] = int(n.group(1)) if n else 0
    return counts


def fetch_calendar(login):
    import time
    # cache-buster + no-cache headers so a CDN can never hand back yesterday's calendar
    req = urllib.request.Request(f"https://github.com/users/{login}/contributions?_={int(time.time())}",
                                 headers={"User-Agent": "profile-readme-activity", "Accept": "text/html",
                                          "Cache-Control": "no-cache", "Pragma": "no-cache"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return parse_calendar(r.read().decode("utf-8"))


def compute_streak(counts, end):
    """Consecutive days with activity, counted back from `end` (or from yesterday if today is still empty)."""
    cur = end if counts.get(end.isoformat(), 0) > 0 else end - dt.timedelta(days=1)
    n, last = 0, cur
    while counts.get(cur.isoformat(), 0) > 0:
        n += 1
        cur -= dt.timedelta(days=1)
    return n, cur + dt.timedelta(days=1), last


def year_totals(counts, end):
    """Contributions and active days in the 365 days ending at `end`."""
    start = end - dt.timedelta(days=364)
    inwin = [v for k, v in counts.items() if start <= dt.date.fromisoformat(k) <= end and v > 0]
    return sum(inwin), len(inwin)


def level(n):
    return 0 if n == 0 else 1 if n == 1 else 2 if n <= 3 else 3 if n <= 7 else 4


def mshort(d):
    return d.strftime("%b")


def dlabel(d):
    return f"{mshort(d)} {d.day}"


# ---- live pieces of hero.svg and about.svg ------------------------------------------------
def hero_badge(total):
    txt = f"{total} CONTRIBUTIONS IN 12 MONTHS"
    w = 38 + len(txt) * 7.45
    x, y = HERO_BADGE_X, HERO_BADGE_Y
    return (f'<rect x="{x}" y="{y}" width="{fmt(w)}" height="26" rx="13" fill="#1A0F0A" stroke="#5A2A17"/>'
            f'<circle cx="{x+16}" cy="{y+13}" r="3.4" fill="{ORANGE}" filter="url(#glowS)"><animate attributeName="r" values="3.4;5;3.4" dur="1.8s" repeatCount="indefinite"/></circle>'
            + label(txt, x + 28, y + 17, 10.5, "#FFB394", weight=600, ls=1.1, mono=True))


def about_number(total):
    g, _ = big_number(str(total), 42, ABOUT_LIVE_X + 21, 71, ORANGE, extra='filter="url(#glowS)"')
    return g


def about_sub(active):
    return label(f"{active} active days in the last year", ABOUT_LIVE_X + 22, 92, 12, MUTED)


# ---- render ------------------------------------------------------------------------------
def render(counts, end, login):
    W, H = 900, 366
    cols, cell, pitch = 26, 17, 21.5
    gx, gy = 300, 84
    window_start = end - dt.timedelta(days=364)
    inwin = {dt.date.fromisoformat(k): v for k, v in counts.items() if window_start <= dt.date.fromisoformat(k) <= end and v > 0}
    total, active = year_totals(counts, end)
    streak, s_start, s_end = compute_streak(counts, end)
    best_day = max(inwin.items(), key=lambda kv: (kv[1], kv[0])) if inwin else (end, 0)
    month_tot = Counter()
    for d, v in inwin.items():
        month_tot[(d.year, d.month)] += v

    last_sun = end - dt.timedelta(days=(end.weekday() + 1) % 7)
    start_sun = last_sun - dt.timedelta(weeks=cols - 1)

    o = []
    defs = f"""
<linearGradient id="gAcc" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{BLUE}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>
<linearGradient id="gBar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7CC0FF"/><stop offset="1" stop-color="#2B6FD1"/></linearGradient>
<linearGradient id="gBarDim" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#27508F"/><stop offset="1" stop-color="#162B52"/></linearGradient>
<linearGradient id="gCard" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0D1526"/><stop offset="1" stop-color="{CARD}"/></linearGradient>
<filter id="glowS" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="1.6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<pattern id="dots" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#2A3A63" opacity=".8"/></pattern>
"""
    o.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="18" fill="url(#gCard)" stroke="{LINE}"/>')
    o.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="17" fill="url(#dots)" opacity=".28"/>')
    o.append(label("COMMIT ACTIVITY", 28, 38, 11, TEXT, weight=700, ls=2, mono=True))
    o.append(label(f"github.com/{login}  ·  last 26 weeks", W - 28, 38, 11, DIM, "end", mono=True))
    o.append(f'<path d="M28.5 52.5 H{W-28.5}" stroke="{LINE}"/>')

    # headline: contributions in the last 12 months
    o.append(f'<circle cx="31" cy="80" r="3.4" fill="{ORANGE}" filter="url(#glowS)"><animate attributeName="opacity" values="1;.3;1" dur="1.6s" repeatCount="indefinite"/></circle>')
    o.append(label("CONTRIBUTIONS", 42, 84, 11, ORANGE, weight=700, ls=1.6, mono=True))
    size = min(64.0, 130.0 / (number_width(str(total), 100) / 100))
    num, nw = big_number(str(total), size, 28, 146, ORANGE, extra='filter="url(#glowS)"')
    o.append(num)
    tx = 28 + nw + 16
    o.append(label("in the last", tx, 124, 12.5, MUTED))
    o.append(label("12 months", tx, 142, 12.5, MUTED))
    o.append(f'<path d="M28.5 164.5 H250" stroke="{LINE}"/>')

    # secondary stats
    best_month = max(month_tot.items(), key=lambda kv: (kv[1], kv[0])) if month_tot else ((end.year, end.month), 0)
    if streak > 1:
        streak_sub = f"{dlabel(s_start)} → {dlabel(s_end)}"
    elif streak:
        streak_sub = f"active on {dlabel(s_end)}"
    else:
        streak_sub = "the next commit starts one"
    rows = [(str(streak), "day streak", streak_sub),
            (str(best_day[1]), f"best day · {dlabel(best_day[0])}", "contributions in 24 hours"),
            (str(best_month[1]), f"in {dt.date(best_month[0][0], best_month[0][1], 1).strftime('%B')}", "my busiest month")]
    for i, (n, l1, l2) in enumerate(rows):
        y = 210 + i * 52
        nn, _ = big_number(n, 30, 28, y, "url(#gAcc)")
        o.append(nn)
        o.append(label(l1, 104, y - 12, 12.5, TEXT, weight=600))
        o.append(label(l2, 104, y + 5, 11.5, DIM))

    # heatmap
    last_month_label = -99
    for c in range(cols):
        for r in range(7):
            d = start_sun + dt.timedelta(days=7 * c + r)
            if d > end:
                continue
            n = counts.get(d.isoformat(), 0)
            x, y = gx + c * pitch, gy + r * pitch
            in_streak = streak > 0 and s_start <= d <= s_end
            if in_streak:
                i = (d - s_start).days
                a = 0.04 + 0.6 * i / max(streak - 1, 1)
                o.append(f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{cell}" height="{cell}" rx="4" fill="{LEVELS[level(n)]}" stroke="{ORANGE}" stroke-opacity=".5" stroke-width="1.1">'
                         f'<animate attributeName="stroke-opacity" values=".5;1;.5;.5" keyTimes="0;{fmt(a)};{fmt(a+.04)};1" dur="9s" repeatCount="indefinite"/>'
                         f'<animate attributeName="stroke-width" values="1.1;2.2;1.1;1.1" keyTimes="0;{fmt(a)};{fmt(a+.04)};1" dur="9s" repeatCount="indefinite"/></rect>')
            else:
                o.append(f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{cell}" height="{cell}" rx="4" fill="{LEVELS[level(n)]}"/>')
    for c in range(cols):
        d0 = start_sun + dt.timedelta(days=7 * c)
        for r in range(7):
            d = d0 + dt.timedelta(days=r)
            if d.day == 1 and d <= end and c - last_month_label >= 3:
                o.append(label(mshort(d), gx + c * pitch, gy - 12, 10, DIM, mono=True))
                last_month_label = c
    for r, nm in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        o.append(label(nm, gx - 10, gy + r * pitch + 12.5, 9.5, DIM, "end", mono=True))

    # legend
    ly = gy + 7 * pitch + 6
    o.append(f'<rect x="{gx}" y="{fmt(ly)}" width="12" height="12" rx="3.5" fill="{LEVELS[3]}" stroke="{ORANGE}" stroke-width="1.1"/>')
    o.append(label("streak day", gx + 19, ly + 10, 10.5, MUTED, mono=True))
    lx = gx + cols * pitch - 4.5
    o.append(label("more", lx, ly + 10, 10.5, DIM, "end", mono=True))
    for k in range(5):
        o.append(f'<rect x="{fmt(lx-48-(4-k)*16)}" y="{fmt(ly)}" width="12" height="12" rx="3.5" fill="{LEVELS[k]}"/>')
    o.append(label("less", lx - 48 - 4 * 16 - 7, ly + 10, 10.5, DIM, "end", mono=True))

    # monthly bars
    months = []
    y_, m_ = end.year, end.month
    for _ in range(9):
        months.append((y_, m_))
        m_ -= 1
        if m_ == 0:
            y_, m_ = y_ - 1, 12
    months.reverse()
    mx = max([month_tot.get(k, 0) for k in months] + [1])
    base, maxh = 340, 40
    bp = cols * pitch / 9.0
    o.append(label("CONTRIBUTIONS PER MONTH", gx, 282, 10, DIM, weight=600, ls=1.6, mono=True))
    for i, k in enumerate(months):
        v = month_tot.get(k, 0)
        h = max(2.0, v / mx * maxh) if v else 2.0
        bw = 34
        x = gx + i * bp + (bp - bw) / 2
        top = k == max(months, key=lambda kk: month_tot.get(kk, 0))
        fill = "url(#gBar)" if top else "url(#gBarDim)"
        o.append(f'<rect x="{fmt(x)}" y="{fmt(base-h)}" width="{bw}" height="{fmt(h)}" rx="4" fill="{fill}"/>')
        o.append(label(v, x + bw / 2, base - h - 6, 10.5, TEXT if top else MUTED, "middle", 700 if top else 500, mono=True))
        o.append(label(mshort(dt.date(k[0], k[1], 1)), x + bw / 2, base + 16, 10, DIM, "middle", mono=True))

    title = f"{total} contributions in the last year and a {streak}-day streak for {login}"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(title)}" fill="none">\n'
            f'<title>{escape(title)}</title>\n<defs>{defs}</defs>\n' + "\n".join(o) + "\n</svg>\n")


def _swap(s, tag, content):
    return re.sub(rf"<!--{tag}-->.*?<!--/{tag}-->", lambda m: f"<!--{tag}-->{content}<!--/{tag}-->", s, flags=re.S)


def patch_live(assets, total, active):
    """Keep the contribution count in hero.svg and about.svg in step with the heatmap."""
    import os
    p = os.path.join(assets, "hero.svg")
    if os.path.exists(p):
        s = open(p, encoding="utf-8").read()
        open(p, "w", encoding="utf-8", newline="\n").write(_swap(s, "live-badge", hero_badge(total)))
    p = os.path.join(assets, "about.svg")
    if os.path.exists(p):
        s = open(p, encoding="utf-8").read()
        s = _swap(s, "live-num", about_number(total))
        s = _swap(s, "live-sub", about_sub(active))
        open(p, "w", encoding="utf-8", newline="\n").write(s)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--login", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--json", help="offline: {date: count} for non-empty days")
    ap.add_argument("--end", help="offline: last day of the window (YYYY-MM-DD)")
    ap.add_argument("--assets", help="folder holding hero.svg and about.svg to keep in sync")
    a = ap.parse_args(argv)
    if a.json:
        counts = json.load(open(a.json))
        end = dt.date.fromisoformat(a.end) if a.end else dt.date.today()
    else:
        counts = fetch_calendar(a.login)
        if not counts:
            sys.exit("no contribution cells found; layout may have changed")
        end = max(dt.date.fromisoformat(d) for d in counts)
    svg = render(counts, end, a.login)
    with open(a.out, "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)
    print("wrote", a.out)
    if a.assets:
        total, active = year_totals(counts, end)
        patch_live(a.assets, total, active)
        print("patched live numbers in", a.assets, "->", total, "contributions,", active, "active days")


if __name__ == "__main__":
    main()
