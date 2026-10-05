"""Draft conversion of the LTRCOL-2011 Word lab guide to a single Markdown page.

Output is a *draft* that gets hand-edited afterwards.
"""
import hashlib
import io
import re
import sys
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph
from PIL import Image

SRC = Path(sys.argv[1])
OUT_MD = Path(sys.argv[2])
IMG_DIR = Path(sys.argv[3])
IMG_DIR.mkdir(parents=True, exist_ok=True)

doc = Document(str(SRC))
rels = doc.part.rels

# numbering formats: numId -> {ilvl: fmt}
numfmt = {}
npart = doc.part.numbering_part.element
abstract = {}
for a in npart.findall(qn("w:abstractNum")):
    lv = {}
    for l in a.findall(qn("w:lvl")):
        f = l.find(qn("w:numFmt"))
        lv[l.get(qn("w:ilvl"))] = f.get(qn("w:val")) if f is not None else "decimal"
    abstract[a.get(qn("w:abstractNumId"))] = lv
for n in npart.findall(qn("w:num")):
    numfmt[n.get(qn("w:numId"))] = abstract.get(n.find(qn("w:abstractNumId")).get(qn("w:val")), {})

EMU = 914400
saved = {}  # hash -> filename
counters = {}
section = "cover"


def save_image(blip, extent_in, crop):
    rid = blip.get(qn("r:embed"))
    part = rels[rid].target_part
    blob = part.blob
    key = hashlib.md5(blob + repr(crop).encode()).hexdigest()
    if key in saved:
        return saved[key]
    im = Image.open(io.BytesIO(blob))
    im.load()
    if crop:
        w, h = im.size
        l, t, r, b = (crop.get(k, 0) / 100000 for k in ("l", "t", "r", "b"))
        im = im.crop((round(w * l), round(h * t), round(w * (1 - r)), round(h * (1 - b))))
    icon = extent_in < 0.45
    if not icon and im.width > 1800:
        nh = round(im.height * 1800 / im.width)
        im = im.resize((1800, nh), Image.LANCZOS)
    if icon:
        name = f"icon-{len([v for v in saved.values() if v.startswith('icon')]) + 1:02d}.png"
    else:
        counters[section] = counters.get(section, 0) + 1
        name = f"{section}-{counters[section]:02d}.png"
    if im.mode not in ("RGB", "RGBA", "L", "LA", "P"):
        im = im.convert("RGBA")
    im.save(IMG_DIR / name, optimize=True)
    saved[key] = name
    return name


def run_items(el):
    """Yield ('t', text, bold, italic, href) / ('img', name, icon) items in order."""
    for child in el:
        tag = child.tag.split("}")[1]
        if tag == "r":
            yield from run_content(child, None)
        elif tag == "hyperlink":
            rid = child.get(qn("r:id"))
            href = rels[rid].target_ref if rid and rid in rels else None
            for r in child.iter(qn("w:r")):
                yield from run_content(r, href)
        elif tag in ("ins", "smartTag", "customXml", "sdt", "fldSimple"):
            for r in child.iter(qn("w:r")):
                yield from run_content(r, None)


def run_content(r, href):
    rpr = r.find(qn("w:rPr"))

    def on(t):
        if rpr is None:
            return False
        e = rpr.find(qn(t))
        return e is not None and e.get(qn("w:val")) not in ("0", "false")

    bold, ital = on("w:b"), on("w:i")
    for c in r:
        tag = c.tag.split("}")[1]
        if tag == "t":
            yield ("t", c.text or "", bold, ital, href)
        elif tag == "tab":
            yield ("t", " ", bold, ital, href)
        elif tag == "br":
            yield ("t", "\n", bold, ital, href)
        elif tag == "drawing":
            ext = c.find(".//" + qn("wp:extent"))
            w_in = int(ext.get("cx")) / EMU
            src = c.find(".//" + qn("a:srcRect"))
            crop = {k: int(v) for k, v in (src.attrib.items() if src is not None else [])}
            pr = c.find(".//" + qn("wp:docPr"))
            descr = (pr.get("descr") or "") if pr is not None else ""
            for blip in c.iter(qn("a:blip")):
                name = save_image(blip, w_in, crop)
                yield ("img", name, w_in < 0.45, descr)


def render(items):
    out = []
    figs = []
    buf = []  # (text, bold, ital, href)
    for it in items:
        if it[0] == "t":
            buf.append(it[1:])
        else:
            _, name, icon, descr = it
            if icon:
                alt = descr.split("\n")[0].strip() or "icon"
                if "speech bubble" in alt:
                    alt = "Closed captions icon"
                if "red circle" in alt:
                    alt = "End meeting icon"
                buf.append((f"![{alt}](img/{name}){{ .icon }}", False, False, "RAW"))
            else:
                figs.append(name)
    # merge segments
    segs = []
    for text, b, i, h in buf:
        if segs and segs[-1][1:] == (b, i, h) and h != "RAW":
            segs[-1] = (segs[-1][0] + text, b, i, h)
        else:
            segs.append((text, b, i, h))
    for text, b, i, h in segs:
        if h == "RAW":
            out.append(text)
            continue
        if not text.strip():
            out.append(text)
            continue
        lead = text[: len(text) - len(text.lstrip())]
        trail = text[len(text.rstrip()):]
        core = text.strip()
        if h and not h.startswith("mailto:"):
            core = f"[{core}]({h}){{:target=\"_blank\" rel=\"noopener\"}}"
        if b:
            core = f"**{core}**"
        if i and not b:
            core = f"*{core}*"
        out.append(lead + core + trail)
    s = "".join(out)
    s = s.replace(" ", " ")
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\*\*\s*\*\*", " ", s)
    s = re.sub(r"\[\s*(!\[[^\]]*\]\([^)]+\)\{ \.icon \})\s*\]", r"\1", s)
    return s.strip(), figs


lines = []
started = False
list_stack = None
for el in doc.element.body.iterchildren():
    if el.tag != qn("w:p"):
        continue
    p = Paragraph(el, doc)
    style = p.style.name
    text_plain = p.text.strip()
    if not started:
        if style == "Heading 1" and text_plain.startswith("About this Lab"):
            started = True
        else:
            continue

    # section tracking for image names
    m = re.match(r"Module (\d)([a-z])?:", text_plain)
    if style == "Heading 1":
        if text_plain.startswith("About"):
            section = "about"
        elif text_plain.startswith("Accessing"):
            section = "access"
        elif m:
            section = f"module-{m.group(1)}"
    elif m and m.group(2):
        section = f"module-{m.group(1)}{m.group(2)}"

    body, figs = render(run_items(el))
    if not body and not figs:
        continue

    numpr = el.find(".//" + qn("w:numPr"))
    tag = ""
    if numpr is not None:
        ilvl = numpr.find(qn("w:ilvl"))
        nid = numpr.find(qn("w:numId"))
        lvl = ilvl.get(qn("w:val")) if ilvl is not None else "0"
        nidv = nid.get(qn("w:val")) if nid is not None else "?"
        fmt = numfmt.get(nidv, {}).get(lvl, "decimal")
        tag = f"<<LIST {nidv} {lvl} {fmt}>> "

    if style == "Heading 1":
        lines.append(f"\n## {text_plain}\n")
    elif style == "Heading 2" or (m and m.group(2) and len(text_plain) < 200):
        lines.append(f"\n### {text_plain}\n")
    else:
        if body:
            lines.append(f"{tag}{body}")
        for f in figs:
            lines.append(f"<<FIG img/{f}>>")
    lines.append("")

OUT_MD.write_text("\n".join(lines))
print("images:", len(saved))
