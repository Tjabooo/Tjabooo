"""Build the profile's SVGs (banner, project cards, fleet) in the ember palette.

    python3 assets/build.py      # rewrites assets/*.svg and assets/cards/*.svg

Everything is plain SVG with system monospace fonts, so GitHub renders it as an <img> with no
external services. Edit PROJECTS / FLEET below and rerun.
"""
import json
import os
import random
import urllib.request
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent
BG, PANEL, LINE, FG, DIM = "#120d0a", "#1a130f", "#3a2c22", "#d8cbbf", "#7a675a"
ORANGE, GOLD, RED, EMBER = "#ff8c1a", "#ffc857", "#e5484d", "#ff6a00"
FONT = "'JetBrains Mono','JetBrainsMono Nerd Font','SF Mono',ui-monospace,Menlo,Consolas,monospace"
LANG = {"JavaScript": "#f1e05a", "Python": "#4b8bbe", "C#": "#3fb950", "C": "#a8b9cc",
        "PowerShell": "#5391fe", "Rust": "#dea584", "Shell": "#89e051", "Java": "#e76f00",
        "Lua": "#7a8cff", "PHP": "#a074c4"}

PROJECTS = [
    ("marquee", "JavaScript", "self-hosted, phone-first media server: discover, download, subtitles, "
     "watch together, cast to TVs, game clips with share links. one node process, zero deps.",
     ["node", "ffmpeg", "homelab"]),
    ("archfleet", "Python", "terminal dashboard for every machine at home over plain ssh: status, wake-on-lan, "
     "processes, hyprland, files, shared clipboards and arch upkeep.",
     ["textual", "ssh", "tui"]),
    ("clipper", "C#", "medal / shadowplay replacement for linux and windows: always-on replay buffer, "
     "review queue, trimmer, clips straight to the home server.",
     ["gpu-screen-recorder", "obs"]),
    ("ember-latency", "C", "click-to-photon input latency for any vulkan game, right in mangohud. "
     "a tiny vulkan layer + mangohud patch, no fps cost.",
     ["vulkan", "mangohud", "linux gaming"]),
    ("agent-mesh", "Python", "one brain for claude code and codex across all my machines: shared "
     "instructions, memory and settings through a git repo.",
     ["ai agents", "git"]),
    ("cs2-presence", "Python", "discord doesn't see native linux cs2. this does: 'playing counter-strike 2' "
     "through discord's local rpc socket.",
     ["discord rpc", "linux"]),
]

FLEET = [
    ("magi", "desktop", ["arch · hyprland (ember)", "ryzen 7 9800x3d", "radeon rx 9070 xt", "240 hz oled + 144 hz"]),
    ("unit-01", "laptop", ["arch · hyprland (neon)", "zenbook s 16", "ryzen ai 9 hx 370", "radeon 890m"]),
    ("geofront", "server", ["windows 11", "i5-14600kf · gtx 1650", "runs marquee", "media · clips · backups"]),
]


def wrap(text, width):
    lines, line = [], ""
    for word in text.split():
        if len(line) + len(word) + 1 > width:
            lines.append(line)
            line = word
        else:
            line = f"{line} {word}".strip()
    return lines + [line] if line else lines


def save(name, svg):
    (OUT / name).write_text(svg.strip() + "\n")


# ---------- banner ----------
def banner():
    W, H = 1200, 300
    rnd = random.Random(7)
    sparks = []
    for i in range(70):
        x, y = rnd.uniform(0, W), rnd.uniform(H * 0.25, H)
        if x < 720 and y < 215:  # keep the text clear
            y = rnd.uniform(220, H)
        r = rnd.uniform(0.6, 1.9)
        d = rnd.uniform(3, 9)
        delay = rnd.uniform(0, 8)
        sparks.append(f'<circle class="s" cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" '
                      f'style="animation-duration:{d:.1f}s;animation-delay:-{delay:.1f}s"/>')
    waves = []
    for i, (amp, off, op, col) in enumerate([(38, 0, .9, ORANGE), (28, 40, .6, GOLD), (46, 90, .45, EMBER), (22, 150, .35, RED)]):
        y0 = 225 + i * 6
        d = (f"M-200 {y0} C 100 {y0 - amp} 300 {y0 + amp} 600 {y0} S 1100 {y0 - amp} 1400 {y0} "
             f"S 1900 {y0 + amp} 2200 {y0}")
        waves.append(f'<path class="w w{i}" d="{d}" stroke="{col}" stroke-opacity="{op}" '
                     f'style="animation-duration:{14 + i * 4}s;animation-delay:-{off / 10:.1f}s"/>')
    save("banner.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="tjabo">
  <defs>
    <radialGradient id="glow" cx="78%" cy="110%" r="70%">
      <stop offset="0" stop-color="{EMBER}" stop-opacity=".55"/>
      <stop offset=".45" stop-color="#7a2a00" stop-opacity=".25"/>
      <stop offset="1" stop-color="{BG}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="title" x1="0" x2="1">
      <stop offset="0" stop-color="{GOLD}"/><stop offset=".55" stop-color="{ORANGE}"/><stop offset="1" stop-color="{EMBER}"/>
    </linearGradient>
    <clipPath id="c"><rect width="{W}" height="{H}" rx="14"/></clipPath>
    <style>
      .w {{ fill: none; stroke-width: 1.6; animation: drift linear infinite; }}
      .s {{ fill: {GOLD}; animation: rise ease-in infinite; }}
      .cur {{ animation: blink 1.1s steps(1) infinite; }}
      @keyframes drift {{ from {{ transform: translateX(0) }} to {{ transform: translateX(-1000px) }} }}
      @keyframes rise {{ 0% {{ opacity: 0; transform: translateY(0) }} 15% {{ opacity: .9 }}
                         100% {{ opacity: 0; transform: translateY(-90px) }} }}
      @keyframes blink {{ 50% {{ opacity: 0 }} }}
      @media (prefers-reduced-motion: reduce) {{ .w, .s, .cur {{ animation: none }} }}
    </style>
  </defs>
  <g clip-path="url(#c)">
    <rect width="{W}" height="{H}" fill="{BG}"/>
    <rect width="{W}" height="{H}" fill="url(#glow)"/>
    {''.join(waves)}
    {''.join(sparks)}
    <rect x="0" y="0" width="{W}" height="3" fill="{ORANGE}"/>
    <text x="64" y="128" font-family="{FONT}" font-size="76" font-weight="800" fill="url(#title)">tjabo<tspan class="cur" fill="{ORANGE}">_</tspan></text>
    <text x="68" y="170" font-family="{FONT}" font-size="21" fill="{FG}">self-taught dev · stockholm, sweden</text>
    <text x="68" y="202" font-family="{FONT}" font-size="15" fill="{DIM}">arch + hyprland · homelab · linux gaming · tools i actually use</text>
    <rect x="{W - 64 - 168}" y="60" width="168" height="30" rx="15" fill="none" stroke="{LINE}"/>
    <circle cx="{W - 64 - 148}" cy="75" r="5" fill="{ORANGE}"><animate attributeName="opacity" values="1;.25;1" dur="2.4s" repeatCount="indefinite"/></circle>
    <text x="{W - 64 - 134}" y="80" font-family="{FONT}" font-size="13" fill="{FG}">ember · magi</text>
    <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="none" stroke="{LINE}"/>
  </g>
</svg>""")


# ---------- project cards ----------
def card(name, lang, desc, tags):
    W, H = 440, 150
    lines = wrap(desc, 49)[:3]
    body = "".join(f'<text x="24" y="{70 + i * 19}" class="d">{escape(l)}</text>' for i, l in enumerate(lines))
    x, chips = 24, []
    lx = 24 + 18 + len(lang) * 7.8 + 16
    x = lx
    for t in tags:
        w = len(t) * 7.2 + 16
        chips.append(f'<rect x="{x:.0f}" y="122" width="{w:.0f}" height="18" rx="9" fill="none" stroke="{LINE}"/>'
                     f'<text x="{x + w / 2:.0f}" y="135" class="t" text-anchor="middle">{escape(t)}</text>')
        x += w + 6
    save(f"cards/{name}.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{name}">
  <style>
    .n {{ font: 800 19px {FONT}; fill: {ORANGE}; }}
    .d {{ font: 13px {FONT}; fill: {FG}; }}
    .l {{ font: 12px {FONT}; fill: {DIM}; }}
    .t {{ font: 11px {FONT}; fill: {DIM}; }}
  </style>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="10" fill="{PANEL}" stroke="{LINE}"/>
  <rect x="0" y="12" width="3" height="{H - 24}" rx="1.5" fill="{ORANGE}"/>
  <text x="24" y="38" class="n">{escape(name)}</text>
  <text x="{W - 24}" y="38" class="l" text-anchor="end">→</text>
  {body}
  <circle cx="30" cy="131" r="5" fill="{LANG.get(lang, FG)}"/>
  <text x="42" y="135" class="l">{escape(lang)}</text>
  {''.join(chips)}
</svg>""")


# ---------- the fleet ----------
def fleet():
    W, H = 900, 190
    col = W / 3
    parts = []
    for i, (host, role, specs) in enumerate(FLEET):
        x = 28 + i * col
        parts.append(f'<circle cx="{x + 6}" cy="44" r="5" fill="{ORANGE}">'
                     f'<animate attributeName="opacity" values="1;.3;1" dur="{2 + i * .7:.1f}s" repeatCount="indefinite"/></circle>'
                     f'<text x="{x + 20}" y="49" class="h">{host}</text>'
                     f'<text x="{x + 20}" y="68" class="r">{role}</text>')
        parts += [f'<text x="{x + 20}" y="{98 + j * 20}" class="s">{escape(s)}</text>' for j, s in enumerate(specs)]
        if i:
            parts.append(f'<line x1="{i * col}" y1="28" x2="{i * col}" y2="{H - 28}" stroke="{LINE}"/>')
    save("fleet.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="my machines">
  <style>
    .h {{ font: 800 17px {FONT}; fill: {FG}; }}
    .r {{ font: 12px {FONT}; fill: {ORANGE}; letter-spacing: 2px; }}
    .s {{ font: 13px {FONT}; fill: {DIM}; }}
  </style>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="10" fill="{PANEL}" stroke="{LINE}"/>
  {''.join(parts)}
</svg>""")


# ---------- section headings ----------
def heading(slug, text):
    """Section titles sit on GitHub's own background, so they use mid tones that read in light and dark."""
    W, H = 900, 44
    save(f"h-{slug}.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{text}">
  <text x="0" y="29" font-family="{FONT}" font-size="20" font-weight="800" fill="{ORANGE}">~/<tspan fill="#d9731c">{escape(text)}</tspan></text>
  <line x1="{40 + len(text) * 12.5:.0f}" y1="22" x2="{W}" y2="22" stroke="#b5835a" stroke-opacity=".55" stroke-dasharray="2 6"/>
</svg>""")


# ---------- stats (from the GitHub API; the daily workflow refreshes it) ----------
USER = "Tjabooo"


def gh(path, body=None):
    req = urllib.request.Request("https://api.github.com" + path, data=json.dumps(body).encode() if body else None,
                                 headers={"Accept": "application/vnd.github+json", "User-Agent": "tjabo-profile"})
    if os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", "Bearer " + os.environ["GITHUB_TOKEN"])
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def stats():
    repos = [r for r in gh(f"/users/{USER}/repos?per_page=100&type=owner") if not r["fork"]]
    stars = sum(r["stargazers_count"] for r in repos)
    langs = {}  # by repo, not bytes: one old PHP site shouldn't outweigh everything else
    for r in repos:
        if r["language"] and r["language"] not in ("HTML", "CSS"):
            langs[r["language"]] = langs.get(r["language"], 0) + 1
    contributions = None
    if os.environ.get("GITHUB_TOKEN"):
        q = {"query": "query($u:String!){user(login:$u){contributionsCollection{contributionCalendar{totalContributions}}}}",
             "variables": {"u": USER}}
        contributions = gh("/graphql", q)["data"]["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]
    top = sorted(langs.items(), key=lambda kv: (-kv[1], kv[0]))[:7]
    total = sum(n for _, n in top) or 1
    W, H = 900, 170
    nums = [("public repos", len(repos)), ("stars", stars)]
    if contributions is not None:
        nums.append(("contributions this year", contributions))
    parts = []
    for i, (label, n) in enumerate(nums):
        x = 36 + i * 150
        parts.append(f'<text x="{x}" y="70" class="big">{n}</text><text x="{x}" y="94" class="lab">{label}</text>')
    # language bar
    x, bar, legend = 36, [], []
    for i, (lang, n) in enumerate(top):
        w = (W - 72) * n / total
        bar.append(f'<rect x="{x:.1f}" y="118" width="{max(w - 2, 1):.1f}" height="8" fill="{LANG.get(lang, DIM)}"/>')
        x += w
        lx = 36 + i * (W - 72) / 7
        legend.append(f'<circle cx="{lx + 5}" cy="147" r="4.5" fill="{LANG.get(lang, DIM)}"/>'
                      f'<text x="{lx + 16}" y="151" class="lg">{escape(lang.lower())} <tspan fill="{DIM}">{n}</tspan></text>')
    save("stats.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="github stats">
  <style>
    .big {{ font: 800 30px {FONT}; fill: {ORANGE}; }}
    .lab {{ font: 12px {FONT}; fill: {DIM}; letter-spacing: 1px; }}
    .lg  {{ font: 12px {FONT}; fill: {FG}; }}
  </style>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="10" fill="{PANEL}" stroke="{LINE}"/>
  <text x="{W - 36}" y="40" font-family="{FONT}" font-size="12" fill="{DIM}" text-anchor="end">main language of each repo</text>
  {''.join(parts)}
  <clipPath id="b"><rect x="36" y="118" width="{W - 72}" height="8" rx="4"/></clipPath>
  <g clip-path="url(#b)">{''.join(bar)}</g>
  {''.join(legend)}
</svg>""")


if __name__ == "__main__":
    banner()
    for p in PROJECTS:
        card(*p)
    fleet()
    try:
        stats()
    except Exception as error:  # offline or rate-limited: keep the last stats.svg
        print("stats skipped:", error)
    for slug, text in [("rice", "rice"), ("projects", "projects"), ("more", "smaller things"),
                       ("fleet", "the fleet"), ("stack", "stack"), ("stats", "stats")]:
        heading(slug, text)
    print("built", sorted(p.name for p in OUT.rglob("*.svg")))
