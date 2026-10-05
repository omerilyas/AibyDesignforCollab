# AI by Design for Collaboration — lab guide site

MkDocs (Material) site for the three-part LTRCOL-2011 lab: Part 1 (Webex AI) at `docs/index.md`, Part 2 (MCP) at `docs/part-2/index.md`, Part 3 (GenAI) at `docs/part-3/index.md`.

## Python environment

- **On Omer's Mac:** use the existing venv: `source /Users/omer/VirtualEnvoirnments/Mkdocs/bin/activate && mkdocs serve`. Do not create a new virtual environment.
- **Anywhere else** (the software factory's worker Box, CI, a fresh machine): that path does not exist. If `.venv/` is already there, use it (`source .venv/bin/activate`); the factory creates it before you start. Otherwise create it: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`.

Before you finish a change, run `mkdocs build --strict`. It fails on broken links or anchors.

<!-- handoff:start -->
## Handoff
In an interactive session on Omer's Mac: before starting work, read `HANDOFF.md` in this folder. It records the current state, decisions, user preferences and next steps from the previous session. Update it with `/handoff` before ending a session.

When you work on a GitHub issue for the software factory (non-interactive, in a worker Box): read `HANDOFF.md` for context if useful, but do not edit it unless the issue asks you to.
<!-- handoff:end -->
