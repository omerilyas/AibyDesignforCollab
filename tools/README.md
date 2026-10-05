# tools/

Helper scripts used to build this site. **Not part of the published site** (MkDocs only builds `docs/`). Run them with any Python 3 that has Pillow (`pip install pillow`); `docx_to_markdown.py` also needs `python-docx`.

## pixel-art/

Pixel art is drawn as Python pixel maps and emitted as inline SVG (rects merged per row/colour).

| Script | Output | Used in |
|---|---|---|
| `scene.py` | 64×48 avatar-at-CRT scene → `scene.svg`, PNG previews | `overrides/partials/hero-scene.html` (shown in the left rail, revealed by scroll) |
| `badge.py` | 18×18 "player 1" portrait → `badge.svg`, `favicon.svg`, `badge.png` | header logo in `overrides/partials/header.html`; `docs/assets/favicon.svg` |
| `mini.py` | shared `rects()` helper (badge.py imports it); its own outputs (desk/mug overlay, old mini avatar) are **no longer used** | — |

Regenerate (run from this folder, output to any folder):

```bash
cd tools/pixel-art
python3 scene.py /tmp/art && python3 badge.py /tmp/art
```

Then paste the new `<svg>` into the target file. Keep the first comment line of `hero-scene.html`. Header badge: replace the `<svg class="pxg avatar-badge" …>` block. Animation classes (`art-*`, `badge-*`) are styled in `docs/css/lab.css`.

## conversion/ (one-off, already applied)

- `docx_to_markdown.py`: first-pass conversion of the Part 1 Word guide (`Helpfiles/…docx`) to Markdown + images. The output was then **hand-edited** into `docs/index.md`.
- `merge_part2.py` + `part2-parts/`: merged the old GenAI MkDocs project (`../CLUS26-AI-LAB/docs`) into what is now **`docs/part-3/index.md`** (it was Part 2 until the MCP guide was added). It has since been edited too.
- Part 2 (MCP, `docs/part-2/index.md`) was written by hand from `Helpfiles/mcp.docx`; its 35 screenshots were extracted with Word crops applied.

**Do not re-run these over the current docs**: they would overwrite manual edits. They're kept for reference only.
