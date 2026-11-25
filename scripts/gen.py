"""Generate Minecraft-style SVG assets for the GitHub profile README."""
import os, re, random, sys

OUT = sys.argv[1]
ICONS = sys.argv[2]
os.makedirs(OUT, exist_ok=True)

# ---------- 5x7 pixel font ----------
F = {
 'A': [".###.","#...#","#...#","#####","#...#","#...#","#...#"],
 'B': ["####.","#...#","#...#","####.","#...#","#...#","####."],
 'C': [".####","#....","#....","#....","#....","#....",".####"],
 'D': ["####.","#...#","#...#","#...#","#...#","#...#","####."],
 'E': ["#####","#....","#....","####.","#....","#....","#####"],
 'F': ["#####","#....","#....","####.","#....","#....","#...."],
 'G': [".####","#....","#....","#..##","#...#","#...#",".####"],
 'H': ["#...#","#...#","#...#","#####","#...#","#...#","#...#"],
 'I': [".###.","..#..","..#..","..#..","..#..","..#..",".###."],
 'J': ["....#","....#","....#","....#","#...#","#...#",".###."],
 'K': ["#...#","#..#.","#.#..","##...","#.#..","#..#.","#...#"],
 'L': ["#....","#....","#....","#....","#....","#....","#####"],
 'M': ["#...#","##.##","#.#.#","#...#","#...#","#...#","#...#"],
 'N': ["#...#","##..#","#.#.#","#..##","#...#","#...#","#...#"],
 'O': [".###.","#...#","#...#","#...#","#...#","#...#",".###."],
 'P': ["####.","#...#","#...#","####.","#....","#....","#...."],
 'Q': [".###.","#...#","#...#","#...#","#.#.#","#..#.",".##.#"],
 'R': ["####.","#...#","#...#","####.","#.#..","#..#.","#...#"],
 'S': [".####","#....","#....",".###.","....#","....#","####."],
 'T': ["#####","..#..","..#..","..#..","..#..","..#..","..#.."],
 'U': ["#...#","#...#","#...#","#...#","#...#","#...#",".###."],
 'V': ["#...#","#...#","#...#","#...#","#...#",".#.#.","..#.."],
 'W': ["#...#","#...#","#...#","#...#","#.#.#","##.##","#...#"],
 'X': ["#...#","#...#",".#.#.","..#..",".#.#.","#...#","#...#"],
 'Y': ["#...#","#...#",".#.#.","..#..","..#..","..#..","..#.."],
 'Z': ["#####","....#","...#.","..#..",".#...","#....","#####"],
 '0': [".###.","#...#","#..##","#.#.#","##..#","#...#",".###."],
 '1': ["..#..",".##..","..#..","..#..","..#..","..#..","#####"],
 '2': [".###.","#...#","....#","..##.",".#...","#....","#####"],
 '3': [".###.","#...#","....#","..##.","....#","#...#",".###."],
 '4': ["...#.","..##.",".#.#.","#..#.","#####","...#.","...#."],
 '5': ["#####","#....","####.","....#","....#","#...#",".###."],
 '6': ["..##.",".#...","#....","####.","#...#","#...#",".###."],
 '7': ["#####","#...#","....#","...#.","..#..","..#..","..#.."],
 '8': [".###.","#...#","#...#",".###.","#...#","#...#",".###."],
 '9': [".###.","#...#","#...#",".####","....#","...#.",".##.."],
 ' ': ["....."]*7,
 '!': ["..#..","..#..","..#..","..#..","..#..",".....","..#.."],
 '-': [".....",".....",".....",".###.",".....",".....","....."],
 '.': [".....",".....",".....",".....",".....",".....","..#.."],
 ',': [".....",".....",".....",".....",".....","..#..",".#..."],
 ':': [".....","..#..",".....",".....",".....","..#..","....."],
 "'": ["..#..","..#..",".....",".....",".....",".....","....."],
 '/': ["....#","....#","...#.","..#..",".#...","#....","#...."],
 '%': ["##..#","##..#","...#.","..#..",".#...","#..##","#..##"],
 '+': [".....","..#..","..#..","#####","..#..","..#..","....."],
}

def text_width(s, px):
    return len(s) * 6 * px - px

def text_rects(s, x, y, px, color):
    out = []
    for ci, ch in enumerate(s.upper()):
        g = F.get(ch, F[' '])
        for r, row in enumerate(g):
            c = 0
            while c < 5:
                if row[c] == '#':
                    s0 = c
                    while c < 5 and row[c] == '#':
                        c += 1
                    out.append(f'<rect x="{x + (ci*6 + s0)*px}" y="{y + r*px}" width="{(c-s0)*px}" height="{px}"/>')
                else:
                    c += 1
    return f'<g fill="{color}">' + ''.join(out) + '</g>'

def mc_text(s, x, y, px, color="#FFFFFF", shadow="#3F3F3F"):
    """Minecraft-style text: drop shadow offset by one pixel."""
    return text_rects(s, x + px, y + px, px, shadow) + text_rects(s, x, y, px, color)

def bitmap(rows, x, y, px, palette):
    out = []
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch in palette:
                out.append(f'<rect x="{x+c*px}" y="{y+r*px}" width="{px}" height="{px}" fill="{palette[ch]}"/>')
    return ''.join(out)

# ---------- block textures (16x16 at 2px -> 32px blocks) ----------
rnd = random.Random(7)

def texture(pid, fn, size=32, px=4):
    n = size // px
    cells = []
    for r in range(n):
        for c in range(n):
            cells.append(f'<rect x="{c*px}" y="{r*px}" width="{px}" height="{px}" fill="{fn(r, c, n)}"/>')
    return f'<pattern id="{pid}" width="{size}" height="{size}" patternUnits="userSpaceOnUse">{"".join(cells)}</pattern>'

def pick(opts):
    return rnd.choice(opts)

DIRT = ["#866043", "#79553A", "#966C4A", "#6C4A30", "#8B6446"]
GRASS = ["#5D9C35", "#6AAE3A", "#4F8A2B", "#79C04A", "#5A9632"]
STONE = ["#7F7F7F", "#747474", "#8A8A8A", "#6B6B6B", "#7A7A7A"]

def grass_fn(r, c, n):
    edge = 2 + (rnd.random() < 0.5)
    if r < edge:
        return pick(GRASS)
    if r == edge and rnd.random() < 0.4:
        return pick(GRASS)
    return pick(DIRT)

def dirt_fn(r, c, n):
    return pick(DIRT)

def stone_fn(r, c, n):
    return pick(STONE)

ORE_SPOTS = {(1, 1), (1, 2), (2, 1), (2, 2), (4, 5), (5, 5), (5, 6), (4, 6), (5, 1), (6, 1), (6, 2), (1, 5), (2, 5)}
def ore_fn(colors):
    def f(r, c, n):
        if (r, c) in ORE_SPOTS:
            return pick(colors)
        return pick(STONE)
    return f

def log_fn(r, c, n):
    return pick(["#6B5132", "#5A4329", "#735737", "#4E3A23"]) if c % 3 else "#3F2E1B"

def leaves_fn(r, c, n):
    v = rnd.random()
    if v < 0.12:
        return "#2E5A16"
    return pick(["#3F7F22", "#4A8C2A", "#38721E", "#559A30"])

DEFS = ''.join([
    texture("grass", grass_fn), texture("dirt", dirt_fn), texture("stone", stone_fn),
    texture("diamond", ore_fn(["#5DECF5", "#2FC4CF", "#A1FBE8"])),
    texture("gold", ore_fn(["#FCEE4B", "#E5C02B"])),
    texture("emerald", ore_fn(["#17DD62", "#0F9C45"])),
    texture("redstone", ore_fn(["#FF0000", "#AA0000"])),
    texture("log", log_fn), texture("leaves", leaves_fn),
])

def block(x, y, kind, size=32):
    return f'<rect x="{x}" y="{y}" width="{size}" height="{size}" fill="url(#{kind})"/>'

CREEPER_FACE = [
    "gGgggGgg",
    "gggGgggg",
    "gKKggKKg",
    "gKKggKKg",
    "gggKKggg",
    "ggKKKKgg",
    "ggKKKKgg",
    "ggKggKgg",
]

def creeper(x, y, px=4):
    pal = {'g': "#4CAF3A", 'G': "#6DC85A", 'K': "#111111"}
    head = bitmap(CREEPER_FACE, x, y, px, pal)
    body = ''.join(f'<rect x="{x+2*px + c*px}" y="{y+8*px + r*px}" width="{px}" height="{px}" fill="{rnd.choice(["#4CAF3A","#5BBE48","#3E9A2F","#6DC85A"])}"/>'
                   for r in range(10) for c in range(4))
    feet = ''.join(f'<rect x="{x + c*px}" y="{y+18*px + r*px}" width="{px}" height="{px}" fill="{rnd.choice(["#4CAF3A","#3E9A2F","#5BBE48"])}"/>'
                   for r in range(4) for c in range(8) if not (c in (3, 4)))
    return f'<g>{head}{body}{feet}</g>'

def cloud(x, y, w, h):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#FFFFFF"/>'
            f'<rect x="{x+16}" y="{y-16}" width="{w-48}" height="16" fill="#FFFFFF"/>'
            f'<rect x="{x}" y="{y+h}" width="{w}" height="6" fill="#E3E9F2"/>')

# ---------- banner ----------
def banner():
    W, H = 1280, 360
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" shape-rendering="crispEdges">']
    s.append('<style>'
             '.c1{animation:drift 60s linear infinite}'
             '.c2{animation:drift 90s linear infinite;animation-delay:-40s}'
             '.c3{animation:drift 75s linear infinite;animation-delay:-20s}'
             '@keyframes drift{from{transform:translateX(-400px)}to{transform:translateX(1400px)}}'
             '.splash{transform-origin:1065px 102px;animation:pulse .9s ease-in-out infinite alternate}'
             '@keyframes pulse{from{transform:rotate(-14deg) scale(1)}to{transform:rotate(-14deg) scale(1.08)}}'
             '.blink{animation:blink 1s steps(1) infinite}@keyframes blink{50%{opacity:0}}'
             '</style>')
    s.append(f'<defs>{DEFS}</defs>')
    # stepped sky
    sky = ["#6E9BF5", "#78A7FF", "#83B1FF", "#8FBAFF", "#9CC4FF", "#AACDFF", "#B8D6FF"]
    band = 48
    for i, col in enumerate(sky):
        s.append(f'<rect x="0" y="{i*band}" width="{W}" height="{band+1}" fill="{col}"/>')
    # sun
    s.append('<rect x="236" y="28" width="72" height="72" fill="#FFF3B0" opacity=".45"/>'
             '<rect x="248" y="40" width="48" height="48" fill="#FFFBE0"/>')
    # clouds
    s.append(f'<g class="c1">{cloud(0, 58, 176, 24)}</g>')
    s.append(f'<g class="c2">{cloud(0, 120, 128, 20)}</g>')
    s.append(f'<g class="c3">{cloud(0, 30, 96, 16)}</g>')

    # terrain
    cols = W // 32
    heights = [3, 3, 3, 4, 4, 4, 3, 3, 2, 2, 2, 3, 3, 3, 3, 2, 2, 2, 2, 3, 3, 3, 3, 3, 2, 2, 2, 2, 3, 3, 4, 4, 4, 3, 3, 3, 4, 4, 3, 3]
    ores = {(5, 0): "diamond", (12, 1): "gold", (21, 0): "redstone", (27, 0): "emerald", (34, 1): "diamond", (2, 1): "redstone", (17, 0): "gold"}
    ground_top = {}
    for c in range(cols):
        h = heights[c]
        top = H - h * 32
        ground_top[c] = top
        for r in range(h):
            y = top + r * 32
            if r == 0:
                kind = "grass"
            elif r == 1 and h >= 3:
                kind = "dirt"
            else:
                kind = ores.get((c, h - 1 - r), "stone")
            s.append(block(c * 32, y, kind))
    # trees
    for tc in (1,):
        base = ground_top[tc]
        for i in range(1, 5):
            s.append(block(tc * 32, base - i * 32, "log"))
        for dx in (-2, -1, 0, 1, 2):
            for dy in (5, 4):
                s.append(block((tc + dx) * 32, base - dy * 32 - 0, "leaves"))
        for dx in (-1, 0, 1):
            s.append(block((tc + dx) * 32, base - 6 * 32, "leaves"))
        s.append(block(tc * 32, base - 7 * 32, "leaves"))
    # creeper
    s.append(creeper(35 * 32 + 8, ground_top[35] - 88, 4))
    # flowers
    for fc, col in ((9, "#FF5555"), (14, "#FFFF55"), (22, "#FF5555"), (25, "#FFFF55")):
        x = fc * 32 + 12
        y = ground_top[fc]
        s.append(f'<rect x="{x+3}" y="{y-12}" width="2" height="12" fill="#2E7D1E"/><rect x="{x}" y="{y-18}" width="8" height="8" fill="{col}"/>')

    # title
    title = "HOUSSEIN"
    px = 10
    tw = text_width(title, px)
    tx = (W - tw) // 2
    # dark outline, stone-grey extrusion, white face
    for dx, dy in ((-4, 0), (4, 0), (0, -4), (0, 4)):
        s.append(text_rects(title, tx + dx, 64 + dy, px, "#1E1E1E"))
    s.append(text_rects(title, tx + 6, 64 + 8, px, "#1E1E1E"))
    s.append(text_rects(title, tx + 3, 64 + 4, px, "#6B6B6B"))
    s.append(text_rects(title, tx, 64, px, "#F0F0F0"))
    sub = "BUILDING THINGS ONE BLOCK AT A TIME"
    px2 = 3
    sx = (W - text_width(sub, px2)) // 2
    s.append(mc_text(sub, sx, 168, px2, "#FFFFFF", "#3F3F3F"))
    # splash text
    splash = "ALSO TRY GIT PUSH!"
    s.append(f'<g class="splash">{mc_text(splash, 905, 92, 3, "#FFFF55", "#3F3F15")}</g>')
    s.append('</svg>')
    return ''.join(s)

# ---------- hotbar HUD ----------
HEART = [
    ".KK.KK.",
    "KRRKRRK",
    "KRWRRRK",
    "KRRRRRK",
    ".KRRRK.",
    "..KRK..",
    "...K...",
]
DRUM = [
    "....KKK",
    "...KMMK",
    "..KMMMK",
    ".KMMMK.",
    "KBKKK..",
    "KWK....",
    ".K.....",
]

def load_icon(name, prefix):
    raw = open(os.path.join(ICONS, f"{name}.svg")).read()
    raw = re.sub(r'<\?xml[^>]*>', '', raw)
    raw = re.sub(r'id="([^"]+)"', lambda m: f'id="{prefix}{m.group(1)}"', raw)
    raw = re.sub(r'url\(#([^)]+)\)', lambda m: f'url(#{prefix}{m.group(1)})', raw)
    raw = re.sub(r'href="#([^"]+)"', lambda m: f'href="#{prefix}{m.group(1)}"', raw)
    # strip outer width/height so we can size it
    raw = re.sub(r'^\s*<svg width="48" height="48"', '<svg', raw.strip(), count=1)
    return raw

ITEMS = [("js", "JAVASCRIPT"), ("ts", "TYPESCRIPT"), ("py", "PYTHON"), ("c", "C"),
         ("html", "HTML"), ("css", "CSS"), ("git", "GIT"), ("linux", "LINUX"), ("latex", "LATEX")]

def hotbar(level):
    slot = 44
    bw = slot * 9 + 4
    W = 560
    ox = (W - bw) // 2
    H = 172
    bar_y = 118
    period = 2 * len(ITEMS)
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" shape-rendering="crispEdges">']
    s.append('<style>'
             '.it{opacity:0;animation:sel %ds steps(1) infinite}'
             '@keyframes sel{0%%{opacity:1}%.3f%%{opacity:0}100%%{opacity:0}}'
             '.hb{animation:beat 1.2s steps(1) infinite}@keyframes beat{0%%{transform:translateY(0)}10%%{transform:translateY(-2px)}20%%{transform:translateY(0)}}'
             '</style>' % (period, 100 / len(ITEMS)))
    # hotbar frame
    s.append(f'<rect x="{ox-2}" y="{bar_y-2}" width="{bw+4}" height="{slot+8}" fill="#000000"/>')
    s.append(f'<rect x="{ox}" y="{bar_y}" width="{bw}" height="{slot+4}" fill="#8B8B8B"/>')
    for i, (key, name) in enumerate(ITEMS):
        x = ox + 2 + i * slot
        s.append(f'<rect x="{x}" y="{bar_y+2}" width="{slot}" height="{slot}" fill="#373737"/>'
                 f'<rect x="{x+2}" y="{bar_y+4}" width="{slot-2}" height="{slot-2}" fill="#FFFFFF" opacity=".25"/>'
                 f'<rect x="{x+2}" y="{bar_y+4}" width="{slot-4}" height="{slot-4}" fill="#8B8B8B"/>')
        s.append(f'<svg x="{x+6}" y="{bar_y+8}" width="{slot-12}" height="{slot-12}" viewBox="0 0 256 256" shape-rendering="auto">'
                 + re.sub(r'^<svg[^>]*>', '', load_icon(key, f"i{i}_"))[:-len('</svg>')] + '</svg>')
    # animated selector + item name
    for i, (key, name) in enumerate(ITEMS):
        x = ox + 2 + i * slot
        delay = -((period - 2 * i) % period)
        st = f'style="animation-delay:{delay}s"'
        sel = (f'<rect x="{x-4}" y="{bar_y-2}" width="{slot+8}" height="{slot+8}" fill="none" stroke="#000" stroke-width="2"/>'
               f'<rect x="{x-2}" y="{bar_y}" width="{slot+4}" height="{slot+4}" fill="none" stroke="#FFFFFF" stroke-width="4"/>')
        nx = (W - text_width(name, 3)) // 2
        label = mc_text(name, nx, 6, 3, "#FFFFFF", "#3F3F3F")
        s.append(f'<g class="it" {st}>{sel}{label}</g>')
    # XP bar
    xp_y = bar_y - 20
    s.append(f'<rect x="{ox}" y="{xp_y}" width="{bw}" height="10" fill="#000000"/>')
    s.append(f'<rect x="{ox+2}" y="{xp_y+2}" width="{bw-4}" height="6" fill="#2A2A2A"/>')
    s.append(f'<rect x="{ox+2}" y="{xp_y+2}" width="{int((bw-4)*0.68)}" height="6" fill="#80FF20"/>')
    s.append(f'<rect x="{ox+2}" y="{xp_y+2}" width="{int((bw-4)*0.68)}" height="2" fill="#C8FF8F"/>')
    lv = str(level)
    lx = (W - text_width(lv, 3)) // 2
    ly = xp_y - 16
    lvl = (''.join(text_rects(lv, lx + dx, ly + dy, 3, "#000000") for dx, dy in ((-3, 0), (3, 0), (0, -3), (0, 3)))
           + text_rects(lv, lx, ly, 3, "#80FF20"))
    s.append(lvl)
    # hearts (left) & hunger (right)
    hy = xp_y - 44
    hp = {'K': "#000000", 'R': "#E21B1B", 'W': "#FFFFFF"}
    for i in range(10):
        s.append(f'<g class="hb" style="animation-delay:{-i*0.05:.2f}s">{bitmap(HEART, ox + i*18, hy, 2.5, hp)}</g>')
    dp = {'K': "#000000", 'M': "#B5502A", 'B': "#E8D4A6", 'W': "#FFFFFF"}
    for i in range(10):
        s.append(bitmap(DRUM, ox + bw - 18 - i*18, hy, 2.5, dp))
    s.append('</svg>')
    return ''.join(s)

# ---------- advancement toast ----------
DIAMOND = [
    "...KKKK...",
    "..KCCWCK..",
    ".KCWCCCCK.",
    "KCCCCCCDDK",
    ".KDCCCDDK.",
    "..KDCCDK..",
    "...KDDK...",
    "....KK....",
]
PICK = [
    ".KKKKKK...",
    "KCCCCCCK..",
    ".KKKKBCCK.",
    "....KBKCK.",
    "...KBK.KCK",
    "..KBK...KK",
    ".KBK......",
    "KBK.......",
]
ICON_PAL = {'K': "#0C1F21", 'C': "#4AEDD9", 'W': "#D5FFF6", 'D': "#1BA8A1", 'B': "#6B4A2B"}

def toast(kind, head, line, icon):
    W, H = 82 + max(text_width(head, 2.5), text_width(line, 2.5)) + 28, 84
    W = int(W)
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" shape-rendering="crispEdges">']
    s.append('<g>')
    s.append(f'<rect x="4" y="4" width="{W-8}" height="{H-8}" fill="#212121"/>'
             f'<rect x="0" y="8" width="{W}" height="{H-16}" fill="#212121"/>'
             f'<rect x="8" y="8" width="{W-16}" height="{H-16}" fill="#000000" opacity=".25"/>'
             f'<rect x="8" y="8" width="{W-16}" height="2" fill="#555555"/>')
    s.append(bitmap(icon, 20, 20, 4.4, ICON_PAL))
    s.append(mc_text(head, 82, 22, 2.5, "#FFFF55" if kind != "challenge" else "#FF55FF", "#3F3F15"))
    s.append(mc_text(line, 82, 48, 2.5, "#FFFFFF", "#3F3F3F"))
    s.append('</g></svg>')
    return ''.join(s)

# ---------- grass divider ----------
def divider():
    W, H = 1280, 32
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" shape-rendering="crispEdges"><defs>{DEFS}</defs>']
    for c in range(W // 32):
        s.append(block(c * 32, 0, "grass"))
    s.append('</svg>')
    return ''.join(s)

def section(title):
    px = 4
    W = text_width(title, px) + 48
    H = 56
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" shape-rendering="crispEdges">']
    # sign-like plank
    s.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#2B1D0E"/><rect x="4" y="4" width="{W-8}" height="{H-8}" fill="#A0784A"/>'
             f'<rect x="4" y="18" width="{W-8}" height="2" fill="#8A6438"/><rect x="4" y="36" width="{W-8}" height="2" fill="#8A6438"/>')
    s.append(mc_text(title, 24, 14, px, "#FFFFFF", "#3F2A14"))
    s.append('</svg>')
    return ''.join(s)

level = int(os.environ.get("LEVEL", "677"))
files = {
    "banner.svg": banner(),
    "hotbar.svg": hotbar(level),
    "advancement.svg": toast("goal", "ACHIEVEMENT GET!", f"{level} CONTRIBUTIONS THIS YEAR", PICK),
    "advancement-diamonds.svg": toast("task", "ADVANCEMENT MADE!", "DIAMONDS! SHIP A PROJECT", DIAMOND),
    "divider.svg": divider(),
    "sec-about.svg": section("ABOUT ME"),
    "sec-inventory.svg": section("INVENTORY"),
    "sec-chest.svg": section("LOOT CHEST"),
    "sec-stats.svg": section("STATS"),
}
for name, data in files.items():
    with open(os.path.join(OUT, name), "w") as f:
        f.write(data)
    print(name, len(data))
