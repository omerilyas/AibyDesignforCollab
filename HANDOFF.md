# Handoff: AI by Design for Collaboration (LTRCOL-2011 lab guide)

## Current state

**What this is.** MkDocs (Material) site, one long page per part, Claude-blog style (TREE rail, progress bar, Mark complete, J/K, Notes, light/dark). Four parts:

| Part | Page | Topic |
|---|---|---|
| 1 | `docs/index.md` | Webex AI (unchanged content) |
| 2 | `docs/part-2/index.md` | **AI Receptionist & Customer Assist** (new, in progress, ~145 min) |
| 3 | `docs/part-3/index.md` | MCP (was Part 2; only labels/links renumbered) |
| 4 | `docs/part-4/index.md` | GenAI (was Part 3; only labels/links renumbered) |

**Nothing is committed or pushed** (user: local only, don't push). Folder moves are staged (renames tracked); later edits are partly unstaged; `docs/part-2/files/` and `hooks/` are untracked. `mkdocs build --strict` passes.

**User rule:** don't change Part 1, 3 or 4 *content*. Site-wide styling/behaviour changes are fine when asked (see "Site-wide changes").

### Part 2 — where it stands
Source `Helpfiles/AIreceptionist.pdf`, heavily reworked: **no CUCM/Unity migration**, everything built new in Collaboration Control Hub, lab access reused from Part 1, all test calls **internal** via Charles Holland's Webex App (AI Receptionist ext 6023, Auto Attendant 6500, queues 6501/6502; no E.164 numbers). Company name **AI By Design Solutions** everywhere (text, files, screenshots).

TREE: About → AI Receptionist overview → **1** AI Receptionist setup → Customer Assist overview → **2** Prepare Webex Calling → **3** Create the Auto Attendant → **4** Create the queues (+ test AA) → **5** Add a supervisor (+ optional Taylor supervisor view) → **6** Advanced queue features (bounced calls, join/unjoin, wrap-up, recording) → **7** Intent-based routing → Call-in options → **8** Webex App logins → **9** Verify AI Receptionist → **10–12** agent/supervisor/admin experience → Congratulations → Next (Part 3). Calling AI tasks and all appendices were removed.

Student downloads: `docs/part-2/files/AI By Design Solutions-KB.txt`, `docs/part-2/files/AI Receptionist Config.txt` (CRLF; mirrored in gitignored `Helpfiles/`).

### Next / open questions (offered, not yet answered)
- Tasks 3–4 wizard steps (AA and queue creation) were written without seeing the live UI; user to verify / send screenshots. `air-105.png` (AA Basics) still highlights "Open the bulk editor".
- Tasks 8, 10, 11 still mention Workstations 2–4 / mobile phone in places (e.g. "Call the AI Receptionist from your mobile phone"); Task 8 Taylor login may duplicate the optional Task 5 sign-in.
- Review screenshot `air-046.png` still shows "+44…, Ext 6023".
- Anita's old ext 6017 still in Task 4 tables / AA steps (notes say it varies).
- Task 2 Step 3 "Write down the main number. You need it later" — nothing uses it now.
- OfficeHours schedule 07:00–23:00 Mon–Fri (warning tells students to set All day); offered All day from the start.
- UK example values from the PDF (Europe/London, English UK/Emma voice) vs US dCloud.
- ~60 plain "Control Hub" mentions in Part 2; offered "Collaboration Control Hub" pass.
- Optional "Useful links" section (AIR / Customer Assist docs) after removing Appendix A.
- Rail links / nav label still "Part 2 · AI Receptionist".
- Then: user decides when to commit/push.

### Site-wide changes this session (affect all parts)
- `hooks/image_size.py` (registered under `hooks:` in `mkdocs.yml`) adds width/height to every PNG `<img>` so TREE anchor jumps land exactly (lazy images had 0 height). Verified with puppeteer: 116 px from top on all parts.
- Note admonitions are green like tips (`docs/css/lab.css`, `.admonition.note`).
- Header: Part 2 label "AI RECEPTIONIST & CUSTOMER ASSIST"; `.lab-nav__more` hides below 1280px, label words hide below 1088px (fixes header overflow at 960–1088px).

### How to run and verify
- Venv: `source /Users/omer/VirtualEnvoirnments/Mkdocs/bin/activate` (don't create a new one); `mkdocs build --strict`.
- `mkdocs serve` pages live under `/AibyDesignforCollab/…` because `site_url` has a path.
- Browser checks: `npm i puppeteer-core` (in a scratch folder), Chrome at `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`.

### Gotchas
- Python-Markdown merges a `- ` list directly followed by a `1.` list (or items after a nested list without a blank line) into one list: always separate with a blank line or lead-in sentence; verify steps render as `<ol>`.
- Captions: `/// caption` with a blank line after the image; indent 4 spaces per list level.
- Images: PNG, ≤1600 px wide, quantized to 256 colours (PIL MEDIANCUT, no dither). `air-NNN.png` from the PDF (gaps after removals); user screenshots get descriptive names (`air-kellie-*.png`, `air-taylor-supervisor.png`). Delete images that become orphaned.
- Screenshot text edits: macOS Vision OCR (Swift) + PIL repaint in SF font; red boxes detect with "R>140, R−G>50, R−B>50".
- Removing a task/step: renumber `### Step N`, `data-toc-label`, `#tN-sM` ids and "Task N, Step M" refs; update the "Lab at a glance" row and the total minutes (hero `LAB TIME` + table).
- A 13 px overflow at 390 px phone width is pre-existing.
- Don't use `git stash` here (renames + untracked files).
- `HANDOFF.md` and `handoff.md` are the same file on macOS.

### Design decisions (still in force)
- One long page per part; hero from front matter; rail links from `links:` (Part 1 uses `extra.rail_links`).
- Keep the "AI BY DESIGN" ASCII panel's original look; red-cap avatar in the rail; only proctor is Omer Ilyas.
- Rail LINKS always visible under the avatar, one column; only the TREE scrolls.
- Must work on GitHub Pages; no external assets except Google Fonts.

### Suggested skills
- `pstack:poteto-mode` (multi-file guide edits)
- `unslop` (guide prose)
- `run` (serve the site and check pages in a browser)
- `handoff` (update this file before ending)

## Log

### 2026-10-12 13:45
**Done**
- Part 2: removed remaining migration content (tasks, appendices), Calling AI tasks, Screen pop and Call back; rewrote Task 2–4 as manual Control Hub setup (Kellie/Taylor Webex Calling, TTS greeting, Cisco Calling Plan check, Auto Attendant, queues + AA test); added AI transparency, AI engine table, Customer Assist and supervisor intros, optional Taylor supervisor view, internal-extension Call-in options, several notes; replaced/edited many screenshots.
- Site-wide: image size hook (TREE jumps exact), green note boxes, header label/overflow fix.

**Next**
- Resolve the open questions in Current state (remaining mobile/Workstation wording, wizard screenshots, Control Hub naming), then commit when the user asks.

### 2026-10-12 12:07
**Done**
- Moved MCP → Part 3, GenAI → Part 4; renumbered labels/links only (chips, rail links, header switch, nav, README).
- Built Part 2 from `Helpfiles/AIreceptionist.pdf` (screenshots extracted to `docs/part-2/img/`), then reworked it per user feedback: removed CUCM/Unity migration (lab topology, tasks 1–2, export/data-dump/migrate/CSV steps, migration overview sections), rewrote About, AIR overview and Customer Assist overview from help.webex.com, added AI transparency, AI engine table, region note, downloadable text files, manual AA (Task 3) and queue (Task 4) creation, Kellie/Taylor Webex Calling step, TTS-only greeting, Cisco Calling Plan PSTN check.
- Renamed APEX UC Solutions → AI By Design Solutions in text, files and ~40 screenshot spots; replaced several screenshots with the user's new ones.
- Header: Part 2 label "AI RECEPTIONIST & CUSTOMER ASSIST" (wide screens) and fixed header overflow at 960–1088px.

**Next**
- Work through the open questions in Current state (PSTN/mobile wording, Calling AI tasks, appendices, wizard screenshots), then commit when the user asks.

### 2026-10-04 (earlier sessions, from the previous handoff format)
- 2026-10-04 23:52: Brought the rail LINKS back on all screen sizes (they had been hidden below 940px), placed them directly under the avatar in one column, made only the TREE scroll when space is short (active entry auto-kept in view), and added the **Token assignment tool** link to all three parts.
- 2026-10-04 (later): Added **Part 2 · MCP** from `Helpfiles/mcp.docx`; moved the GenAI guide to Part 3 (`docs/part-3/`) and renumbered all links, chips, rail links, header switch and storage keys; added tabs, checklists, flow diagrams, emoji font fallback; fixed mobile overflow and short-screen rail fit.
- 2026-10-04: Built the whole site. Converted the Part 1 docx; merged Part 2; Claude-blog design (rail, progress, tasks, J/K, notes); restyled the hero meta; trimmed proctors; pixel-art avatar scene (rail scroll-reveal) + header badge + favicon; robot removed; ASCII panel kept in its original look. Created the `/handoff` skill (`~/.claude/skills/handoff/`) and this file.
