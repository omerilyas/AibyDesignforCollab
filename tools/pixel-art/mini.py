"""Two more pixel pieces, built from the same palette as scene.py:

1. ascii-overlay: desk strip + steaming coffee mug for the "AI BY DESIGN" panel (64x48).
2. mini-avatar: 24x16 header mascot, red-cap character typing (keys light up) next to a coffee.
"""
import sys
from scene import PAL, rects as rects64  # noqa: F401  (palette shared with the hero scene)

PAL = dict(PAL)
PAL.update({"lit": "#f2c14e", "steamc": "currentColor"})


def blank(w, h):
    return [[None] * w for _ in range(h)]


def from_rows(rows, legend, w, h, ox=0, oy=0, into=None):
    c = into or blank(w, h)
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch in legend and legend[ch]:
                c[oy + y][ox + x] = legend[ch]
    return c


def rects(layer):
    h, w = len(layer), len(layer[0])
    runs = []
    for y in range(h):
        x = 0
        while x < w:
            col = layer[y][x]
            if col is None:
                x += 1
                continue
            x0 = x
            while x < w and layer[y][x] == col:
                x += 1
            runs.append((col, x0, y, x - x0))
    by = {}
    for col, x0, y, rw in runs:
        by.setdefault((col, x0, rw), []).append(y)
    out = []
    for (col, x0, rw), ys in by.items():
        ys.sort()
        s = p = ys[0]
        for y in ys[1:] + [None]:
            if y is not None and y == p + 1:
                p = y
                continue
            out.append((col, x0, s, rw, p - s + 1))
            if y is not None:
                s = p = y
    return out


def svg(cls, w, h, layers, label=None, extra=""):
    aria = f'role="img" aria-label="{label}"' if label else 'aria-hidden="true" focusable="false"'
    parts = [f'<svg class="{cls}" viewBox="0 0 {w} {h}" shape-rendering="crispEdges" {extra}{aria}>']
    for gcls, layer in layers:
        parts.append(f'<g class="{gcls}">' if gcls else "<g>")
        groups = {}
        for col, x, y, rw, rh in rects(layer):
            groups.setdefault(col, []).append(f"M{x} {y}h{rw}v{rh}h-{rw}z")
        for col, ds in groups.items():
            parts.append(f'<path fill="{PAL[col]}" d="{"".join(ds)}"/>')
        parts.append("</g>")
    parts.append("</svg>")
    return "\n".join(parts)


# ------------------------------------------------------------------ 1. ASCII panel overlay
# The exact mug + steam from the hero scene, moved to the panel's lower right.
import scene as _scene
W, H = 64, 48
DX, DY = 50, 4


def moved(layer, drop=()):
    out = blank(W, H)
    for y in range(H):
        for x in range(W):
            col = layer[y][x]
            if col and col not in drop and 0 <= x + DX < W and 0 <= y + DY < H:
                out[y + DY][x + DX] = col
    return out


mug = moved(_scene.stack(_scene.mug_ol, _scene.mug), drop=("bg",))   # handle hole stays see-through
steam_a = moved(_scene.steam_a)
steam_b = moved(_scene.steam_b)
for layer in (steam_a, steam_b):
    for row in layer:
        for i, col in enumerate(row):
            if col:
                row[i] = "steamc"                                    # themed in CSS

ascii_svg = svg("ascii-desk", W, H, [("", mug), ("art-steam-a", steam_a), ("art-steam-b", steam_b)],
                extra='preserveAspectRatio="xMidYMid slice" ')

# ------------------------------------------------------------------ 2. header mini avatar (26x17)
MW, MH = 22, 16
AV = [
    "..KKKKKK..............",
    ".KRRRRRRK.............",
    "KRRRWWRRRK............",
    "KrrrrrrrrK............",
    "KHHHHHHHHK............",
    "KHSHHSSHSK............",
    "KSESSSSESK............",
    "KSSMSSMSSK............",
    "KSSSMMSSSK.....KKKKK..",
    "KJJJTTJJJK.....KcccK..",
    "KJJJTTJJJK.....KmmmKKK",
    "KjJJTTJJjK.....KmmmK.K",
    "KKKKKKKKKKKKK..KmmmKKK",
    "KkkkkkkkkkkkK..KnnnK..",
    "KKKKKKKKKKKKK..KKKKK..",
]
OX, OY = 0, 0
legend = {"K": "ol", "R": "cap", "r": "capd", "H": "hair", "S": "skin", "E": "ol", "M": "ol",
          "J": "jak", "j": "jakd", "T": "shirt", "k": "key", "c": "woodd", "m": "mug", "n": "mugd"}
fig = from_rows(AV, legend, MW, MH, ox=OX, oy=OY)
fig[OY + 2][OX + 4] = fig[OY + 2][OX + 5] = "wh"          # cap badge
fig[OY + 11][OX + 20] = None                                 # hole inside the mug handle
desk = blank(MW, MH)
for x in range(MW):
    desk[MH - 1][x] = "wood"
base = blank(MW, MH)
for layer in (fig, desk):
    for y in range(MH):
        for x in range(MW):
            if layer[y][x]:
                base[y][x] = layer[y][x]


def at(layer, pts, col):
    for x, y in pts:
        layer[OY + y][OX + x] = col
    return layer


hands_a = at(blank(MW, MH), [(2, 11), (3, 11), (6, 12), (7, 12)], "skin")   # left up, right pressing
hands_b = at(blank(MW, MH), [(2, 12), (3, 12), (6, 11), (7, 11)], "skin")   # left pressing, right up
keys = [at(blank(MW, MH), [(kx, 13)], "lit") for kx in (2, 8, 5, 10)]   # order the keys light up in
mini_steam_a = at(blank(MW, MH), [(16, 5), (18, 5), (17, 6), (16, 7)], "steamc")
mini_steam_b = at(blank(MW, MH), [(17, 5), (16, 6), (18, 6), (17, 7)], "steamc")
blink = at(blank(MW, MH), [(2, 6), (7, 6)], "skin")

mini_svg = svg("pxg avatar-mini", MW, MH,
               [("", base), ("ava-hands-a", hands_a), ("ava-hands-b", hands_b)]
               + [(f"ava-key ava-key-{i + 1}", k) for i, k in enumerate(keys)]
               + [("ava-steam-a", mini_steam_a), ("ava-steam-b", mini_steam_b), ("ava-blink", blink)])

if __name__ == "__main__":
    out = sys.argv[1]
    open(out + "/ascii-desk.svg", "w").write(ascii_svg)
    open(out + "/avatar-mini.svg", "w").write(mini_svg)
    print(len(ascii_svg), len(mini_svg))
