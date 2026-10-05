"""18x18 arcade 'player portrait' badge of the red-cap avatar (header mascot + favicon)."""
import sys
from mini import rects

PAL = {
    "o": "#d97757", "K": "#1b1a18", "R": "#c8312b", "r": "#9e2420", "W": "#faf9f5",
    "H": "#1b1a18", "S": "#f2d4ad", "s": "#e8b48f", "E": "#1b1a18", "J": "#c8312b",
    "j": "#9e2420", "T": "#f4f1ea", "Y": "#f2c14e",
}

ART = [
    ".KKKKKKKKKKKKKKKK.",
    "KooooooooooooooooK",
    "KoooooKKKKKKoooooK",
    "KooooKRRRRRRKooooK",
    "KoooKRRRWWRRRKoooK",
    "KoooKRRRRRRRRKoooK",
    "KooKrrrrrrrrrrKooK",
    "KoooKHHHHHHHHKoooK",
    "KoooKHSSHSSSHKoooK",
    "KoooKSSESSESSKoooK",
    "KoooKSSESSESSKoooK",
    "KoooKsKSSSSKsKoooK",
    "KoooKSSKKKKSSKoooK",
    "KooooKSSSSSSKooooK",
    "KooKJJKTTTTKJJKooK",
    "KoKJJjJTTTTJjJJKoK",
    "KKJJJjJTTTTJjJJJKK",
    ".KKKKKKKKKKKKKKKK.",
]
assert all(len(r) == 18 for r in ART), [len(r) for r in ART]
N = 18


def layer(points, col):
    g = [[None] * N for _ in range(N)]
    for x, y in points:
        g[y][x] = col
    return g


base = [[(ch if ch != "." else None) for ch in row] for row in ART]
blink = layer([(7, 9), (10, 9)], "S")                                   # top half of eyes closes
look = layer([(7, 9), (7, 10), (10, 9), (10, 10)], "S")                 # erase eyes...
look_eyes = layer([(8, 9), (8, 10), (11, 9), (11, 10)], "E")            # ...and redraw them glancing right
sparkle = layer([(14, 2), (13, 3), (14, 3), (15, 3), (14, 4)], "Y")
scan = layer([(x, y) for y in range(2, 17, 2) for x in range(1, 17)
              if base[y][x] == "o"], "K")


def svg(cls, layers, size_attrs="", extra_style=""):
    parts = [f'<svg class="{cls}" viewBox="0 0 {N} {N}" shape-rendering="crispEdges" {size_attrs}'
             'aria-hidden="true" focusable="false">' + extra_style]
    for gcls, lay, opacity in layers:
        attrs = (f' class="{gcls}"' if gcls else "") + (f' opacity="{opacity}"' if opacity else "")
        parts.append(f"<g{attrs}>")
        groups = {}
        for col, x, y, w, h in rects(lay):
            groups.setdefault(col, []).append(f"M{x} {y}h{w}v{h}h-{w}z")
        for col, ds in groups.items():
            parts.append(f'<path fill="{PAL[col]}" d="{"".join(ds)}"/>')
        parts.append("</g>")
    parts.append("</svg>")
    return "\n".join(parts)


header = svg("pxg avatar-badge", [("", base, None), ("", scan, ".12"),
                                   ("badge-look", look, None), ("badge-look", look_eyes, None),
                                   ("badge-blink", blink, None), ("badge-sparkle", sparkle, None)])
favicon = svg("", [("", base, None), ("", scan, ".12")], size_attrs='xmlns="http://www.w3.org/2000/svg" ')

if __name__ == "__main__":
    out = sys.argv[1]
    open(out + "/badge.svg", "w").write(header)
    open(out + "/favicon.svg", "w").write(favicon)
    from PIL import Image
    im = Image.new("RGB", (N, N), (20, 20, 19))
    for y in range(N):
        for x in range(N):
            c = base[y][x]
            if c:
                im.putpixel((x, y), tuple(int(PAL[c][i:i + 2], 16) for i in (1, 3, 5)))
    im.resize((N * 20, N * 20), Image.NEAREST).save(out + "/badge.png")
    print(len(header), len(favicon))
