# AI by Design for Collaboration — LTRCOL-2011 lab guide

MkDocs site for the three-part **LTRCOL-2011** lab:

| Part | Page | Topic | Source |
|---|---|---|---|
| 1 | `/` (`docs/index.md`) | Webex AI: Cisco AI Assistant in Control Hub, AI in Messaging, Calling and Meetings (~115 min) | `Helpfiles/LTRCOL-2011 - AI Lab Guide - Published One.docx` |
| 2 | `/part-2/` (`docs/part-2/index.md`) | MCP: Webex Messaging MCP server with Codex, a WCIT and elicitation (~90 min) | `Helpfiles/mcp.docx` |
| 3 | `/part-3/` (`docs/part-3/index.md`) | GenAI: building Webex messaging workflows with LangChain in Google Colab (~120 min) | the earlier `CLUS26-AI-LAB` MkDocs project, merged into one page |

Each part is **one long page**. A sticky "TREE" rail on the left tracks your position as you scroll:

- the current section is highlighted and its module expands
- a `▓▓▓░░░` progress bar fills as you scroll
- **Mark complete** buttons at the end of each task add a ✓ to the rail (saved in the browser, separately for each part)
- the pixel avatar in the rail "loads" row by row as you scroll
- <kbd>J</kbd> / <kbd>K</kbd> jump to the next / previous section
- a **Notes** scratchpad (bottom-right), shared by all parts, for pod credentials and phone numbers
- the top bar switches between Parts 1, 2 and 3; click any screenshot to zoom; light/dark follows the system, with a toggle

## Local preview

Use the existing MkDocs virtual environment (no new venv needed):

```bash
source /Users/omer/VirtualEnvoirnments/Mkdocs/bin/activate
mkdocs serve          # http://127.0.0.1:8000  (Part 2: /part-2/, Part 3: /part-3/)
mkdocs build --strict # optional: fails on broken links or anchors
```

Fresh machine instead:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

## Project structure

```
.
├── mkdocs.yml                    # site config (Material theme + custom_dir, nav: Parts 1–3)
├── requirements.txt              # mkdocs, mkdocs-material, mkdocs-glightbox
├── .github/workflows/deploy.yml  # GitHub Pages deploy on push to main
├── overrides/
│   ├── main.html                 # single-page layout: hero, TREE rail, article (all parts)
│   ├── 404.html
│   ├── partials/header.html      # top bar: badge logo, Part 1 / 2 / 3, theme toggle, search
│   └── partials/hero-scene.html  # pixel avatar scene shown in the rail
├── docs/
│   ├── index.md                  # Part 1, the whole guide
│   ├── img/                      # Part 1 screenshots (module-1a-01.png …) and inline icons
│   ├── part-2/
│   │   ├── index.md              # Part 2 (MCP), the whole guide
│   │   └── img/                  # Part 2 screenshots (mcp-02.png …)
│   ├── part-3/
│   │   ├── index.md              # Part 3 (GenAI), the whole guide
│   │   └── img/                  # Part 3 screenshots (module-2a-001.png …)
│   ├── css/lab.css               # theme (colour tokens at the top)
│   └── js/lab.js                 # rail, progress, tasks, J/K keys, notes
├── tools/                        # pixel-art generators + one-off converters (see tools/README.md)
└── Helpfiles/                    # source Word documents (not published)
```

## Editing content

Each part is a single Markdown file. The hero (chip, title, standfirst, the four meta items) and the rail **LINKS** come from the page's front matter (`links:`; Part 1 uses the default `extra.rail_links` in `mkdocs.yml`). Internal links are site-relative: `""` is Part 1, `"part-2/"` is Part 2, `"part-3/"` is Part 3.

- **Module** = `##` heading, **task** = `###` heading, with a short eyebrow line above each:

  ```markdown
  <p class="eyebrow sub">Module 2e · ≈ 5 min</p>

  ### My new task { #module-2e data-toc-label="2e · Short rail label" data-task="2e" }
  ```

  `data-toc-label` is the text shown in the rail. `data-task` adds a **Mark complete** button and counts toward the task total. The `id` must be unique on the page.

- **Inside a task:** `####` for sub-sections (Goal, Prerequisites, Steps, Summary) and `#####` for steps. In Part 3, steps carry ids like `{ #t2b-step-12 }`, so links such as `[Step 12](#t2b-step-12)` work across tasks.
- **Part 2 extras:** `=== "Tab title"` content tabs, `- [ ]` checklists, and `<ol class="flow">…</ol>` for the step-by-step flow diagrams.
- **Screenshot with a caption** (indent it by 4 spaces under a numbered step so the numbering continues):

  ```markdown
  ![Alt text](img/module-2e-01.png){ loading=lazy }

  /// caption
  What the screenshot shows.
  ///
  ```

  Figures are numbered automatically (FIG 01, FIG 02, …).

- **Code:** fenced blocks get syntax colours and a copy button; add `linenums="1"` for line numbers (```` ```py linenums="1" ````).
- **Inline UI icon:** `![Copy icon](img/icon-03.png){ .icon }`
- **Callouts:** `!!! note`, `!!! tip`, `!!! info`, `!!! warning`, `!!! danger`, `!!! success`, with an optional `"Title"`.

Colours (including the accent) are the tokens at the top of `docs/css/lab.css`.

## Deploying

`.github/workflows/deploy.yml` builds and publishes to GitHub Pages on every push to `main`. After you create the new repository, add `site_url:` to `mkdocs.yml` (for example `https://<user>.github.io/<repo>/`) so the 404 page links back correctly.
