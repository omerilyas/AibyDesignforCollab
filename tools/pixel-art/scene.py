"""Pixel-art hero scene: blocky red-cap avatar typing at a beige 90s CRT.

Builds a 64x48 pixel canvas from simple shapes, previews it as PNG, and
emits an inline SVG (rects merged per row/colour) with animated layers.
"""
import sys
from PIL import Image

W, H = 64, 48

PAL = {
    "bg": "#d97757", "bg2": "#c9674a", "bg3": "#e48a69",
    "ol": "#1b1a18", "wh": "#faf9f5",
    "cap": "#c8312b", "capd": "#9e2420", "hair": "#1b1a18",
    "skin": "#f2d4ad", "skind": "#e0b98c",
    "jak": "#c8312b", "jakd": "#9e2420", "shirt": "#f4f1ea", "shirtd": "#d9d4c8",
    "bolt": "#f2c14e",
    "beige": "#e9dcc0", "beiged": "#c9b994", "beigel": "#f5ecd8",
    "glass": "#10261a", "glass2": "#0c1f15", "phos": "#7cf29a", "phosd": "#3f9a5c",
    "wood": "#8a5a3b", "woodl": "#a8714b", "woodd": "#6e452c",
    "key": "#d8cbad", "keyd": "#b3a582",
    "mug": "#f4f1ea", "mugd": "#cfc8b8", "steam": "#f7e3d6", "led": "#7cf29a",
}


def canvas():
    return [[None] * W for _ in range(H)]


def rect(c, x0, y0, x1, y1, col):  # inclusive
    for y in range(max(0, y0), min(H - 1, y1) + 1):
        for x in range(max(0, x0), min(W - 1, x1) + 1):
            c[y][x] = col


def px(c, x, y, col):
    if 0 <= x < W and 0 <= y < H:
        c[y][x] = col


def outline(layer, col, into):
    """Draw a 1px outline (4-neighbour) around the non-empty pixels of layer."""
    for y in range(H):
        for x in range(W):
            if layer[y][x] is None:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H and layer[ny][nx] is not None:
                        into[y][x] = col
                        break


def merge(dst, src):
    for y in range(H):
        for x in range(W):
            if src[y][x] is not None:
                dst[y][x] = src[y][x]


def stack(*layers):
    out = canvas()
    for l in layers:
        merge(out, l)
    return out


FONT = {
    "A": [".#.", "#.#", "###", "#.#", "#.#"],
    "I": ["###", ".#.", ".#.", ".#.", "###"],
    ">": ["#..", ".#.", "..#", ".#.", "#.."],
}


def text(c, s, x, y, col):
    for ch in s:
        g = FONT[ch]
        for gy, row in enumerate(g):
            for gx, v in enumerate(row):
                if v == "#":
                    px(c, x + gx, y + gy, col)
        x += 4


# ---------------------------------------------------------------- background
bg = canvas()
rect(bg, 0, 0, W - 1, H - 1, "bg")
for y in range(H):
    for x in range(W):
        # light ordered dither in the top-left, darker toward the desk
        if y < 14 and (x + 2 * y) % 7 == 0 and (x * 3 + y) % 5 == 0:
            bg[y][x] = "bg3"
        if y > 24 and (x + y) % 2 == 0 and (x * 5 + y * 3) % 7 < (y - 24) // 4:
            bg[y][x] = "bg2"

# ---------------------------------------------------------------- desk
desk = canvas()
rect(desk, 0, 37, W - 1, 38, "woodl")
rect(desk, 0, 39, W - 1, H - 1, "wood")
rect(desk, 0, 39, W - 1, 39, "woodd")
for x in range(0, W, 9):
    rect(desk, x, 42, x + 4, 42, "woodd")  # grain
rect(desk, 20, 44, 43, 44, "woodd")       # drawer edge
rect(desk, 30, 45, 33, 45, "beiged")      # drawer pull

# ---------------------------------------------------------------- avatar
av = canvas()
# torso (jacket) + arms
rect(av, 11, 22, 30, 36, "jak")
rect(av, 11, 22, 12, 36, "jakd")          # jacket side shading
rect(av, 17, 22, 24, 36, "shirt")         # open front, white tee
rect(av, 17, 22, 17, 36, "jakd")          # lapel line
rect(av, 24, 22, 24, 36, "jakd")
rect(av, 18, 22, 23, 22, "shirtd")        # collar shadow
# lightning bolt on the tee
for gy, row in enumerate(["..##", ".##.", "####", ".##.", "##.."]):
    for gx, v in enumerate(row):
        if v == "#":
            px(av, 19 + gx, 25 + gy, "bolt")
# arms: upper arm blocks, then forearms angled to the keyboard
rect(av, 7, 22, 10, 31, "jak")
rect(av, 31, 22, 34, 31, "jak")
rect(av, 7, 22, 7, 31, "jakd")
rect(av, 34, 22, 34, 31, "jakd")
rect(av, 9, 31, 13, 33, "jak")
rect(av, 28, 31, 32, 33, "jak")
# head
rect(av, 14, 9, 27, 21, "skin")
rect(av, 14, 21, 27, 21, "skind")
# hair: sides + jagged fringe
rect(av, 13, 9, 15, 15, "hair")
rect(av, 26, 9, 28, 15, "hair")
rect(av, 14, 9, 27, 11, "hair")
for x in (15, 16, 18, 19, 22, 23, 25):
    px(av, x, 12, "hair")
for x in (16, 25):
    px(av, x, 13, "hair")
px(av, 13, 16, "hair")
px(av, 28, 16, "hair")
# cap
rect(av, 15, 3, 26, 8, "cap")
rect(av, 14, 5, 27, 8, "cap")
rect(av, 16, 2, 25, 2, "cap")
rect(av, 13, 8, 28, 9, "capd")            # brim band
rect(av, 19, 4, 22, 6, "wh")              # front panel badge
rect(av, 20, 5, 21, 5, "cap")
# face
smile = [(18, 17), (19, 18), (20, 18), (21, 18), (22, 18), (23, 17)]
for (x, y) in smile:
    px(av, x, y, "ol")
eyes_open = [(18, 14), (18, 15), (23, 14), (23, 15)]
for (x, y) in eyes_open:
    px(av, x, y, "ol")
px(av, 16, 16, "skind")                   # cheeks
px(av, 25, 16, "skind")

avatar_ol = canvas()
outline(av, "ol", avatar_ol)
avatar_white = canvas()
outline(stack(av, avatar_ol), "wh", avatar_white)

# ---------------------------------------------------------------- mug (left)
mug = canvas()
rect(mug, 1, 32, 5, 36, "mug")
rect(mug, 1, 36, 5, 36, "mugd")
rect(mug, 6, 33, 6, 35, "mug")            # handle
px(mug, 5, 34, "bg")
rect(mug, 2, 33, 4, 33, "woodd")          # coffee
mug_ol = canvas()
outline(mug, "ol", mug_ol)

# ---------------------------------------------------------------- keyboard + hands
kb = canvas()
rect(kb, 11, 34, 31, 37, "key")
rect(kb, 11, 37, 31, 37, "keyd")
for y in (35, 36):
    for x in range(12, 31, 2):
        px(kb, x, y, "keyd")
kb_ol = canvas()
outline(kb, "ol", kb_ol)

hands_a = canvas()                         # typing frame A
rect(hands_a, 12, 32, 14, 33, "skin")
rect(hands_a, 27, 33, 29, 34, "skin")
hands_b = canvas()                         # typing frame B
rect(hands_b, 12, 33, 14, 34, "skin")
rect(hands_b, 27, 32, 29, 33, "skin")

# ---------------------------------------------------------------- CRT computer (right)
pc = canvas()
rect(pc, 38, 11, 62, 33, "beige")
rect(pc, 38, 11, 62, 11, "beigel")
rect(pc, 62, 11, 62, 33, "beiged")
rect(pc, 38, 33, 62, 33, "beiged")
rect(pc, 40, 13, 60, 28, "beiged")       # bezel recess
rect(pc, 41, 14, 59, 27, "glass")
for y in range(15, 27, 2):                # scanlines
    rect(pc, 42, y, 58, y, "glass2")
for (x, y) in [(41, 14), (59, 14), (41, 27), (59, 27)]:
    px(pc, x, y, "beiged")                # rounded glass corners
text(pc, ">AI", 43, 16, "phos")
rect(pc, 43, 23, 50, 23, "phosd")         # dim "output" line
rect(pc, 43, 25, 47, 25, "phosd")
rect(pc, 42, 30, 53, 30, "beiged")        # floppy slot
rect(pc, 44, 30, 51, 30, "ol")
px(pc, 59, 30, "led")
rect(pc, 46, 34, 55, 35, "beiged")        # stand
rect(pc, 44, 36, 57, 36, "beige")
pc_ol = canvas()
outline(pc, "ol", pc_ol)

cursor = canvas()
rect(cursor, 55, 16, 57, 20, "phos")

steam_a = canvas()
for (x, y) in [(2, 30), (3, 29), (3, 28), (2, 27), (4, 30), (5, 29)]:
    px(steam_a, x, y, "steam")
steam_b = canvas()
for (x, y) in [(3, 30), (2, 29), (2, 28), (3, 27), (5, 30), (4, 29)]:
    px(steam_b, x, y, "steam")

eyes_closed = canvas()                    # drawn over open eyes during a blink
for (x, y) in [(18, 14), (23, 14)]:
    px(eyes_closed, x, y, "skin")

# ---------------------------------------------------------------- composite
base = stack(bg, desk, avatar_white, avatar_ol, av, mug_ol, mug, pc_ol, pc, kb_ol, kb)
LAYERS = [
    ("base", base, ""),
    ("hands-a", hands_a, "art-hands-a"),
    ("hands-b", hands_b, "art-hands-b"),
    ("cursor", cursor, "art-cursor"),
    ("steam-a", steam_a, "art-steam-a"),
    ("steam-b", steam_b, "art-steam-b"),
    ("blink", eyes_closed, "art-blink"),
]


def preview(path, layers):
    im = Image.new("RGB", (W, H))
    flat = stack(*layers)
    for y in range(H):
        for x in range(W):
            im.putpixel((x, y), tuple(int(PAL[flat[y][x]][i:i + 2], 16) for i in (1, 3, 5)))
    im.resize((W * 10, H * 10), Image.NEAREST).save(path)


def rects(layer):
    out = []
    for y in range(H):
        x = 0
        while x < W:
            col = layer[y][x]
            if col is None:
                x += 1
                continue
            x0 = x
            while x < W and layer[y][x] == col:
                x += 1
            out.append((col, x0, y, x - x0))
    # merge identical runs on consecutive rows into taller rects
    by_key = {}
    for col, x0, y, w in out:
        by_key.setdefault((col, x0, w), []).append(y)
    merged = []
    for (col, x0, w), ys in by_key.items():
        ys.sort()
        start = prev = ys[0]
        for y in ys[1:] + [None]:
            if y is not None and y == prev + 1:
                prev = y
                continue
            merged.append((col, x0, start, w, prev - start + 1))
            if y is not None:
                start = prev = y
    return merged


def svg():
    parts = ['<svg class="hero-scene" viewBox="0 0 64 48" shape-rendering="crispEdges" '
             'preserveAspectRatio="xMidYMid slice" role="img" '
             'aria-label="Pixel-art avatar in a red cap typing at a retro beige computer">']
    for name, layer, cls in LAYERS:
        cls_attr = f' class="{cls}"' if cls else ""
        parts.append(f"<g{cls_attr}>")
        groups = {}
        for col, x, y, w, h in rects(layer):
            groups.setdefault(col, []).append(f"M{x} {y}h{w}v{h}h-{w}z")
        for col, ds in groups.items():
            parts.append(f'<path fill="{PAL[col]}" d="{"".join(ds)}"/>')
        parts.append("</g>")
    parts.append("</svg>")
    return "\n".join(parts)


if __name__ == "__main__":
    out = sys.argv[1]
    preview(out + "/scene-a.png", [base, hands_a, cursor, steam_a])
    preview(out + "/scene-b.png", [base, hands_b, steam_b, eyes_closed])
    open(out + "/scene.svg", "w").write(svg())
    print("svg bytes:", len(svg()))
