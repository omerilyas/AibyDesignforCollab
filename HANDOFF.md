# Handoff: AI by Design for Collaboration (LTRCOL-2011 lab guide)

_Last updated: 2026-10-04 23:52 (local) · by Claude Code (claude-opus-5-5) · session focus: three-part MkDocs lab guide (Part 1 Webex AI, Part 2 MCP, Part 3 GenAI), Claude-blog-style design, pixel-art mascot, rail LINKS (incl. Token assignment tool)_

## TL;DR
- A **MkDocs (Material) site** with three single-page lab guides: **Part 1** (`/`, Webex AI, from the LTRCOL Word doc), **Part 2** (`/part-2/`, **Webex Messaging MCP** with Codex + WCIT, from `Helpfiles/mcp.docx`) and **Part 3** (`/part-3/`, GenAI/LangChain, merged from the older `CLUS26-AI-LAB` project; it was Part 2 until the MCP guide was added).
- The design copies the claude.dev blog post layout: a hero on top, a sticky mono **"TREE" rail** on the left with a ▓░ scroll progress bar, tasks you can tick off, <kbd>J</kbd>/<kbd>K</kbd> section jumps, a Notes panel, and light/dark themes.
- `mkdocs build --strict` passes (anchor validation on). Last browser-checked 2026-10-04 23:52 on all three parts at 1920×1200, 1440×1080/900/768, 1100×800, 1280×720 and 390px mobile: no JS errors, no broken images/anchors, no horizontal overflow, rail never overflows, LINKS always visible, active TREE entry kept in view, progress reaches 100%, task storage separate per part.
- **Not yet published.** Next step: `git init` here, push to a **new** GitHub repo, add `site_url:` to `mkdocs.yml`; the Pages workflow is already in place.

## Goal and context
- Audience: students in Omer Ilyas's hands-on lab **LTRCOL-2011 "AI by Design for Collaboration"**. Part 1 = Cisco AI Assistant / Webex Messaging, Calling, Meetings. Part 2 = Webex Messaging MCP server in Control Hub + Codex with a WCIT and MCP elicitation. Part 3 = building the same ideas with LangChain + Webex APIs in Google Colab.
- Sources:
  - Part 1: `Helpfiles/LTRCOL-2011 - AI Lab Guide - Published One.docx`
  - Part 2: `Helpfiles/mcp.docx` (MCP lab, revision v1; 36 images, first one is a cover mark and is not used)
  - Part 3: `../CLUS26-AI-LAB/` (old MkDocs project, still live at https://omerilyas.github.io/AibyDesign/; **left untouched**)
  - Design reference: https://claude.dev/blog/getting-started-with-claude-code-mods/
- Owner: Omer Ilyas (oilyas@cisco.com), Principal TME. He is the only proctor listed.

## Current state
Working and verified 2026-10-04:
- **Part 1** `docs/index.md`: all docx content (About, Accessing your lab, Modules 1a–4d), 98 images (crops applied), 92 captioned figures, 18 tasks.
- **Part 2 (MCP)** `docs/part-2/index.md`: all of `mcp.docx` (About/lab profile/learning outcomes/before you begin, Start here in Control Hub, MCP servers at a glance, Modules 1–7, Appendix A), 35 captioned screenshots `mcp-02…36.png`, 8 tasks (`start`, `1`–`7`), prompts/config as copyable code blocks, Option 1/Option 2 as content tabs, `- [ ]` checklists, `<ol class="flow">` step diagrams.
- **Part 3 (GenAI)** `docs/part-3/index.md`: all 9 tasks (1a–1e, 2a–2d), 32 images, 113 code blocks with copy buttons; step anchors `#t2b-step-12` etc.; all cross-links internal.
- **Rail (top → bottom):** TREE (active section highlighted, its module expanded) → ▓░ progress bar → task counter → "PRESS J / K" hint → pixel **avatar scene that loads row by row with scroll** ("LOADING AVATAR…" → "AVATAR LOADED ✓") → **LINKS directly under the avatar caption, one column** (user's request). Only the TREE scrolls (inside itself) when the screen is too short, so the progress bar, avatar and LINKS are always visible; `lab.js` keeps the active TREE entry scrolled into view.
- **Rail LINKS** (set per page; Part 1 uses `extra.rail_links` in `mkdocs.yml`, Parts 2–3 use `links:` front matter):
  - Part 1: Part 2 · MCP, Part 3 · GenAI, **Token assignment tool**, dCloud, Webex Control Hub, Webex Help Center
  - Part 2: Part 1, Part 3, **Token assignment tool**, Webex Control Hub, Webex MCP docs
  - Part 3: Part 1, Part 2, **Token assignment tool**, Webex Developer Portal, Google Colab, LangChain docs
  - **Token assignment tool** = https://aibydesign-token-assignment.vercel.app/ ("AI by Design Lab Access"). `https://cs.co/AiByDesign` (used in Part 3 Module 1c for the OpenAI key) redirects to the same tool.
- **Header:** red-cap "player 1" pixel badge (blinks, glances, sparkles) + "AI BY DESIGN" + Part 1 / 2 / 3 switch (WEBEX AI / MCP / GENAI) + theme toggle + search. The favicon is the same badge.
- **Hero:** "AI BY DESIGN" ASCII panel (original neutral look) + chip, title, standfirst, 4 meta items from each page's front matter.
- Task ticks are stored per part in localStorage (`ltrcol2011:done`, `ltrcol2011:done:part-2`, `ltrcol2011:done:part-3`; key derived from the URL); notes are shared (`ltrcol2011:notes`).
- On screens shorter than 940px the rail also hides the "PRESS J / K" hint and the repeated page title, and shrinks the avatar to 10.5rem.

Known imperfections / not done: see Open items.

## Project map
| Path | What it is |
|---|---|
| `mkdocs.yml` | Site config: Material + `custom_dir: overrides`, `font: false`, palette auto light/dark, nav (Parts 1–3), `extra.rail_links` (Part 1 rail links), `validation.anchors: warn`, glightbox, favicon, `pymdownx.tabbed` + `pymdownx.tasklist` (used by Part 2) |
| `docs/index.md` | **Part 1**, the whole guide. Front matter drives the hero (`chip`, `headline`, `standfirst`, `meta`) |
| `docs/part-2/index.md` | **Part 2 (MCP)**, the whole guide. Front matter also sets rail `links:` |
| `docs/part-3/index.md` | **Part 3 (GenAI)**, the whole guide. Front matter also sets rail `links:` |
| `docs/img/`, `docs/part-2/img/`, `docs/part-3/img/` | Screenshots (Part 1 `module-1a-01.png`…, Part 2 `mcp-02.png`…, Part 3 `module-2a-001.png`…) + Part 1 inline UI icons `icon-0N.png` |
| `docs/css/lab.css` | All theming. Colour tokens at the top (light `:root`, dark `[data-md-color-scheme="slate"]`), rail, hero, figures, code, admonitions, pixel-art animations, responsive + short-screen rules |
| `docs/js/lab.js` | Rail active-section, progress bar, avatar reveal (`--reveal`), task buttons, J/K, Notes panel |
| `docs/assets/favicon.svg` | Badge favicon (generated by `tools/pixel-art/badge.py`) |
| `overrides/main.html` | Single-page layout used by all three parts: hero (ASCII panel), rail (TREE, progress, tasks, hint, then `.rail-foot` = avatar reveal + LINKS), article, footer |
| `overrides/partials/header.html` | Top bar with the inline badge SVG |
| `overrides/partials/hero-scene.html` | Inline SVG of the avatar-at-CRT scene (generated by `tools/pixel-art/scene.py`; shown in the rail despite its name) |
| `overrides/404.html` | 404 page |
| `tools/` | Pixel-art generators and one-off converters. **See `tools/README.md`; don't re-run converters over the docs** |
| `.github/workflows/deploy.yml` | GitHub Pages deploy on push to `main` (copied from the Part 2 repo) |
| `README.md` | Human-facing editing guide (headings, tasks, captions, callouts) |

## How to run and verify
**Use the existing venv; do not create a new one** (user instruction):
```bash
cd "/Users/omer/Library/Mobile Documents/com~apple~CloudDocs/Documents/Python_Code/TME Projects/AibyDesignForCollaboration"
source /Users/omer/VirtualEnvoirnments/Mkdocs/bin/activate   # note the spelling "Envoirnments"
mkdocs serve            # http://127.0.0.1:8000  ·  /part-2/  ·  /part-3/
mkdocs build --strict   # must pass; fails on broken links/anchors
```
The venv has mkdocs 1.6.1, mkdocs-material 9.7.6, mkdocs-glightbox 0.5.2. `requirements.txt` pins `mkdocs<2.0`.

Browser checks in this session used headless Chrome via `puppeteer-core` installed in a temp folder (not in the project). Re-install anywhere with `npm i puppeteer-core` and point it at `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`.

## Decisions and user preferences
- **One long page per part**, scrolled top to bottom, with the left rail showing progress. That was the core ask, "like the claude.dev blog".
- Light/dark follows the system, with a toggle. Fonts: Geist / Geist Mono from Google Fonts (loaded in `overrides/main.html`).
- **Hero meta:** chip shows only "Part N of 3" (**no "LTRCOL-2011"**). SESSION = "Delivered by Omer Ilyas". Part 1: EVENT = "AI by Design", UPDATED = "September 2026".
- **Proctors:** only Omer Ilyas. The user removed Kevin Ian Barrow, Hussain Ali, Shane Long and Venky Yechuri; every part lists only Omer.
- **Part order (user decision, 2026-10-04):** Part 1 Webex AI → **Part 2 MCP** → Part 3 GenAI. Every new part must follow the same structure: front matter hero, About (+ lab at a glance, how to use, proctor), eyebrow + `##` module headings with `data-task`, captioned figures, copyable code, callouts, "What's next" card. Emojis must render (emoji fonts are in the `--sans`/`--mono` stacks).
- **"AI BY DESIGN" ASCII panel:** keep it, in its **original neutral background with grey text**. The user explicitly rejected the orange background and any coffee mug on it, and was unhappy when it was removed. Don't remove or recolour it.
- **Red-cap avatar:** the user's own character (red cap with white badge, black hair, smile, red jacket, white tee). The full scene (typing at a beige 90s CRT showing `>AI`, steaming coffee) lives **in the rail under "PRESS J / K"** and reveals row by row with scroll progress (user's idea). The header uses the clearer **badge** portrait. The **robot mascot was removed** at the user's request.
- Style direction for art: retro 70s–2000s computing, "funky", pixel art, subtle animation, honours prefers-reduced-motion.
- Event branding: Part 2 had been rebranded **WebexOne 2026**; the Word doc said Cisco Live 2026. The footer copyright still reads "LTRCOL-2011 · AI by Design for Collaboration · WebexOne 2026" (see Open items).
- Part 1 text got a light copy edit (typos such as "Antia" → Anita; "Workstation 1's IP" → Workstation 2's). Part 3 (GenAI) text is kept as written, except 2d's broken "Step 1" link → Step 3. Part 2 (MCP) keeps the doc's wording with light punctuation fixes.
- Everything must work on **GitHub Pages**: no external assets except Google Fonts; art is inline SVG.
- **Rail LINKS must always be visible** (the user noticed when they were hidden on short screens and asked for them back) and sit **directly under "LOADING AVATAR", one column** — not beside the avatar and not pinned to the bottom of the rail.

## Open items / next steps
- [ ] Create a **new** GitHub repo, `git init` here, push to `main`; then add `site_url: https://<user>.github.io/<repo>/` to `mkdocs.yml` (the 404 page needs it). The `.gitignore` excludes `Helpfiles/`, `*.docx`, `site/`.
- [ ] Footer copyright (`mkdocs.yml` → `copyright`) still says "LTRCOL-2011 · … · WebexOne 2026". Asked the user whether to change it to e.g. "AI by Design for Collaboration · Delivered by Omer Ilyas"; **no answer yet**.
- [ ] Two steps say "ask one of the proctors" (Part 1 Module 3a step 4; Part 3 1c). Asked whether to make it singular; **no answer yet**.
- [ ] Optional: Part 2's MCP screenshots include the author's own tenant email on the Control Hub sign-in screen (`mcp-03.png`) and real space IDs (`mcp-36.png`); fine as-is per the source doc, but review before publishing publicly.
- [ ] Optional: images total ~31 MB (lazy-loaded). Could be compressed if repo size matters.
- [ ] Optional: the old Part 2 site (omerilyas.github.io/AibyDesign) still exists separately; nothing links to it from here.

## Gotchas
- `mkdocs build` prints a big red "MkDocs 2.0" warning banner from the Material team. It's informational; ignore it (we pin <2.0).
- Material remembers the chosen palette in localStorage. When testing light/dark, use a fresh browser profile/context or you'll keep seeing the old theme.
- Puppeteer `clip` screenshots of scrolled pages misrender the sticky rail/header. Take a viewport screenshot and crop it instead.
- In zsh, never name a loop variable `path`: it overwrites `$PATH` for that shell.
- Material adds top padding to code line-number cells; `lab.css` zeroes `.highlighttable .linenos` padding so numbers line up.
- The rail is a flex column with a fixed max-height. Everything in it has `flex-shrink: 0` **except `#tree`**, which shrinks and scrolls (`overflow-y: auto`). Don't hide rail items to make space; let the TREE scroll. Re-run the multi-size check (rail overflow 0, last link visible, active item in view) after adding anything to the rail.
- Figures use `pymdownx.blocks.caption` (`/// caption … ///`), which needs a **blank line** after the image. Inside numbered steps, indent by 4 spaces to keep the numbering going.
- Each task heading needs `data-task="…"` (unique per page) for its "Mark complete" button; the rail label comes from `data-toc-label`.
- `.glance` tables: add the `time` class (`<div class="glance time" markdown>`) only when the last column is a Time column; it right-aligns/nowraps that column. Applying it to text-heavy tables made Part 2 overflow on phones.
- Material stretches content-tab labels past the page edge on phones; `lab.css` resets `.tabbed-labels` margin.

## Session log
- 2026-10-04 23:52: Brought the rail LINKS back on all screen sizes (they had been hidden below 940px), placed them directly under the avatar in one column, made only the TREE scroll when space is short (active entry auto-kept in view), and added the **Token assignment tool** link to all three parts.
- 2026-10-04 (later): Added **Part 2 · MCP** from `Helpfiles/mcp.docx`; moved the GenAI guide to Part 3 (`docs/part-3/`) and renumbered all links, chips, rail links, header switch and storage keys; added tabs, checklists, flow diagrams, emoji font fallback; fixed mobile overflow and short-screen rail fit.
- 2026-10-04: Built the whole site. Converted the Part 1 docx; merged Part 2; Claude-blog design (rail, progress, tasks, J/K, notes); restyled the hero meta; trimmed proctors; pixel-art avatar scene (rail scroll-reveal) + header badge + favicon; robot removed; ASCII panel kept in its original look. Created the `/handoff` skill (`~/.claude/skills/handoff/`) and this file.
