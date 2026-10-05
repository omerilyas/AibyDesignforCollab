"""Merge the Part 2 MkDocs pages into one single-page lab guide (docs/part-2/index.md)."""
import re
import shutil
import sys
from pathlib import Path

SRC = Path(sys.argv[1])          # CLUS26-AI-LAB/docs
OUT = Path(sys.argv[2])          # AibyDesignForCollaboration/docs/part-2
HERE = Path(__file__).parent

M1 = "module-1-setup-your-lab-environment"
M2 = "module-2-langchain-for-messaging-intelligence"

TASKS = [
    # id, file, title, rail label, minutes, eyebrow extra, lede
    ("1a", f"{M1}/module-1a-webex-developer-portal.md", "Webex Developer Portal Setup", "1a · Webex Developer Portal", 10, "", None),
    ("1b", f"{M1}/module-1b-google-colab.md", "Google Colab Setup", "1b · Google Colab", 5, "", None),
    ("1c", f"{M1}/module-1c-managing-api-keys-in-colab.md", "Managing API Keys in Google Colab", "1c · API keys in Colab", 5, "", None),
    ("1d", f"{M1}/module-1d-introduction-to-streamlit.md", "Introduction to Streamlit", "1d · Streamlit (optional)", 5, " · optional, read only", None),
    ("1e", f"{M1}/module-1e-introduction-to-ngrok.md", "Introduction to ngrok", "1e · ngrok (optional)", 5, " · optional, read only", None),
    ("2a", f"{M2}/module-2a-connect-langchain-to-webex-messaging.md", "Connect LangChain to Webex Messaging", "2a · Read Webex messages", 15, " · Task 1", "Read Webex messages as AI context."),
    ("2b", f"{M2}/module-2b-ask-me-anything-webex-spaces.md", "Ask Me Anything for Webex Spaces", "2b · Ask Me Anything (RAG)", 30, " · Task 2", None),
    ("2c", f"{M2}/module-2c-generate-space-summaries.md", "Generate Space Summaries", "2c · Space summaries", 20, " · Task 3", None),
    ("2d", f"{M2}/module-2d-ai-rewrite-assistant.md", "AI Rewrite Assistant", "2d · Rewrite assistant", 25, " · Task 4", None),
]

H2_RENAME = {
    "Steps to Obtain and Use Your Webex Token": "Steps",
    "What You Will Learn": "What you will learn",
    "What is Streamlit?": "What is Streamlit?",
}

# link target: other task page (optionally with #step-N-...)
LINK_TASK = re.compile(
    r"\]\((?:\.\./)?(?:module-[12]-[a-z-]+/)?module-(\d[a-e])-[a-z0-9-]+\.md(?:#step-(\d+)[a-z0-9-]*)?\)")
LINK_MODIDX = re.compile(r"\]\((?:\.\./)?(module-([12])-[a-z-]+)/index\.md\)")
LINK_LOCAL_STEP = re.compile(r"\]\(#step-(\d+)[a-z0-9-]*\)")
IMG = re.compile(r"^(\s*)!\[([^\]]*)\]\(([^)\s]+)\)\s*$")
STEP_H3 = re.compile(r"^### (?:Step )?(\d+)(?:\s*\((Optional)\))?[:.]\s*(.+)$")


def convert(tid, rel, title, label, minutes, extra, lede):
    lines = (SRC / rel).read_text().splitlines()
    out = []
    i = 0
    # drop the H1
    assert lines[0].startswith("# ")
    i = 1
    # drop the inline-styled badge block
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i < len(lines) and lines[i].startswith('<div style="display:flex'):
        while not lines[i].startswith("</div>"):
            i += 1
        i += 1

    out.append(f'<p class="eyebrow sub">Module {tid}{extra} · ≈ {minutes} min</p>')
    out.append("")
    out.append(f'### {title} {{ #module-{tid} data-toc-label="{label}" data-task="{tid}" }}')
    out.append("")
    if lede:
        out.append(f'<p class="lede">{lede}</p>')
        out.append("")

    for line in lines[i:]:
        # 2b/2c/2d tagline blockquote → lede paragraph
        m = re.match(r"^> \*\*(.+)\*\*\s*$", line)
        if m:
            out.append(f'<p class="lede">{m.group(1)}</p>')
            continue
        if line.startswith("## "):
            name = line[3:].strip()
            name = re.sub(r"^Task \d \(\d[a-e]\) Summary$", "Summary", name)
            name = H2_RENAME.get(name, name)
            out.append(f"#### {name}")
            continue
        m = STEP_H3.match(line)
        if m:
            n, opt, rest = m.groups()
            opt = " (optional)" if opt else ""
            out.append(f"##### Step {n}{opt}: {rest} {{ #t{tid}-step-{n} }}")
            continue
        if line.startswith("### "):
            out.append("##### " + line[4:])
            continue
        m = IMG.match(line)
        if m:
            ind, alt, src = m.groups()
            name = Path(src).name
            cap = alt.strip()
            if not cap.endswith((".", "?", "!")):
                cap += "."
            out.append(f"{ind}![{alt}](img/{name}){{ loading=lazy }}")
            out.append("")
            out.append(f"{ind}/// caption")
            out.append(f"{ind}{cap}")
            out.append(f"{ind}///")
            continue

        # links
        def task_link(mm):
            t, step = mm.group(1), mm.group(2)
            if step:
                return f"](#t{t}-step-{step})"
            return f"](#module-{t})"
        line = LINK_TASK.sub(task_link, line)
        line = LINK_MODIDX.sub(lambda mm: f"](#module-{mm.group(2)})", line)
        line = LINK_LOCAL_STEP.sub(lambda mm: f"](#t{tid}-step-{mm.group(1)})", line)
        out.append(line)

    text = "\n".join(out).rstrip() + "\n"
    # Original 2d pointed at a non-existent "#step-1-confirm-or-create-…" anchor;
    # the LLM/output parser are actually created in Step 3.
    if tid == "2d":
        text = text.replace("in [Step 1](#t2d-step-1) below", "in [Step 3](#t2d-step-3) below")
    return text


parts = [(HERE / "head.md").read_text().rstrip() + "\n"]
for t in TASKS:
    if t[0] == "2a":
        parts.append((HERE / "mod2.md").read_text().rstrip() + "\n")
    parts.append(convert(*t))
parts.append((HERE / "tail.md").read_text())
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "index.md").write_text("\n".join(parts))

img_out = OUT / "img"
img_out.mkdir(exist_ok=True)
n = 0
for d in (M1, M2):
    for f in sorted((SRC / d / "img").glob("*.png")):
        shutil.copy2(f, img_out / f.name)
        n += 1
print("images copied:", n)
