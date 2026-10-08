/**
 * Lab feedback → GitHub issue.
 *
 * The lab guide's "Report an issue" form posts here. This function holds the
 * GitHub token (Vercel env var GITHUB_TOKEN), so the token never reaches the
 * browser. Use a fine-grained token limited to this one repo with
 * Issues: read and write and nothing else.
 *
 * Env vars:
 *   GITHUB_TOKEN     required
 *   GITHUB_REPO      default "omerilyas/AibyDesignforCollab"
 *   ALLOWED_ORIGINS  comma-separated, default the GitHub Pages origin
 */

const REPO = process.env.GITHUB_REPO || "omerilyas/AibyDesignforCollab";
const ALLOWED = (process.env.ALLOWED_ORIGINS || "https://omerilyas.github.io")
  .split(",").map((s) => s.trim()).filter(Boolean);
const LABEL = "lab-feedback";

// Best effort: serverless instances don't share memory, but this still stops
// one browser from flooding a warm instance.
const WINDOW_MS = 10 * 60 * 1000;
const MAX_PER_WINDOW = 5;
const hits = new Map();

function limited(ip) {
  const now = Date.now();
  const recent = (hits.get(ip) || []).filter((t) => now - t < WINDOW_MS);
  recent.push(now);
  hits.set(ip, recent);
  return recent.length > MAX_PER_WINDOW;
}

function clean(value, max) {
  return String(value ?? "").replace(/\r/g, "").trim().slice(0, max);
}

// Stop reports from pinging GitHub users or closing issues via keywords.
function defang(text) {
  return text.replace(/(^|[^\w.])@(?=\w)/g, "$1@​").replace(/#(\d)/g, "#​$1");
}

function quote(text) {
  return text.split("\n").map((l) => "> " + l).join("\n");
}

export default async function handler(req, res) {
  const origin = req.headers.origin || "";
  if (ALLOWED.includes(origin)) {
    res.setHeader("Access-Control-Allow-Origin", origin);
    res.setHeader("Vary", "Origin");
    res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
    res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  }
  if (req.method === "OPTIONS") return res.status(204).end();
  if (req.method !== "POST") return res.status(405).json({ error: "Method not allowed" });
  if (!ALLOWED.includes(origin)) return res.status(403).json({ error: "Origin not allowed" });

  const token = process.env.GITHUB_TOKEN;
  if (!token) return res.status(500).json({ error: "Server is not configured" });

  let body = req.body;
  if (typeof body === "string") {
    try { body = JSON.parse(body); } catch { return res.status(400).json({ error: "Invalid JSON" }); }
  }
  body = body || {};

  // Honeypot: real people never see or fill this field.
  if (clean(body.website, 200)) return res.status(200).json({ ok: true });

  const ip = String(req.headers["x-forwarded-for"] || "").split(",")[0].trim() || "unknown";
  if (limited(ip)) return res.status(429).json({ error: "Too many reports. Please try again in a few minutes." });

  const message = clean(body.message, 4000);
  const section = clean(body.section, 200) || "Not specified";
  const page = clean(body.page, 200);
  const url = clean(body.url, 500);
  const contact = clean(body.contact, 200);
  if (message.length < 10) return res.status(400).json({ error: "Please describe the issue in a little more detail." });

  const title = `Lab issue: ${section}`.slice(0, 120);
  const lines = [
    `**Section:** ${defang(section)}`,
    page ? `**Page:** ${defang(page)}` : null,
    url.startsWith("https://") ? `**Link:** ${url}` : null,
    contact ? `**Reported by:** ${defang(contact)}` : null,
    "",
    "**What happened**",
    "",
    quote(defang(message)),
    "",
    "---",
    "_Submitted from the lab guide's Report an issue form._",
  ].filter((l) => l !== null);

  const gh = await fetch(`https://api.github.com/repos/${REPO}/issues`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      Accept: "application/vnd.github+json",
      "X-GitHub-Api-Version": "2022-11-28",
      "Content-Type": "application/json",
      "User-Agent": "lab-feedback",
    },
    body: JSON.stringify({ title, body: lines.join("\n"), labels: [LABEL] }),
  });

  if (!gh.ok) {
    console.error("GitHub API error", gh.status, await gh.text());
    return res.status(502).json({ error: "Could not file the report. Please tell your proctor." });
  }
  const issue = await gh.json();
  return res.status(201).json({ ok: true, number: issue.number });
}
