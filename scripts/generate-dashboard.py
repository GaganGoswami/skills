#!/usr/bin/env python3
"""
generate-dashboard.py

Reads all skills/*/SKILL.md files and produces dashboard.html.
Run directly or via the git pre-commit hook.
"""

import os
import re
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

REPO_ROOT = Path(__file__).parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
OUTPUT = REPO_ROOT / "dashboard.html"


# ─── parsing helpers ──────────────────────────────────────────────────────────

def parse_frontmatter(text: str) -> dict:
    """Extract YAML frontmatter key/value pairs (handles simple multi-line values)."""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', text, re.DOTALL)
    if not match:
        return {}
    fm = match.group(1)
    result: dict = {}
    current_key: str | None = None
    current_lines: list[str] = []

    for line in fm.splitlines():
        kv = re.match(r'^([a-z_-]+):\s*(.*)', line)
        if kv:
            if current_key:
                result[current_key] = ' '.join(current_lines).strip().strip('"\'').strip('>')
            current_key = kv.group(1)
            current_lines = [kv.group(2).strip()] if kv.group(2).strip() else []
        elif current_key and (line.startswith('  ') or line.startswith('\t')):
            current_lines.append(line.strip())

    if current_key:
        result[current_key] = ' '.join(current_lines).strip().strip('"\'').strip('>')

    return result


def extract_triggers(description: str) -> str:
    """Pull the 'Use when …' clause from the description string."""
    match = re.search(r'[Uu]se when (.+?)(?:\.\s*$|$)', description, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""


def extract_section(content: str, *headings: str) -> str:
    """Return the first matching section body (up to the next ## heading)."""
    pattern = '|'.join(re.escape(h) for h in headings)
    match = re.search(
        rf'## (?:{pattern})\s*\n(.*?)(?=\n## |\Z)',
        content,
        re.DOTALL | re.IGNORECASE,
    )
    if not match:
        return ""
    raw = match.group(1)
    # strip code blocks, then markdown symbols
    raw = re.sub(r'```.*?```', '', raw, flags=re.DOTALL)
    raw = re.sub(r'[`*#]', '', raw)
    raw = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', raw)   # keep link text
    raw = re.sub(r'\n{3,}', '\n\n', raw)
    return raw.strip()[:500]


def collect_skills() -> dict:
    skills: dict = {}
    for category in ["engineering", "productivity"]:
        cat_dir = SKILLS_DIR / category
        if not cat_dir.exists():
            continue
        cat_skills = []
        for skill_dir in sorted(cat_dir.iterdir()):
            skill_file = skill_dir / "SKILL.md"
            if not skill_file.exists():
                continue
            content = skill_file.read_text(encoding="utf-8")
            fm = parse_frontmatter(content)

            name = fm.get("name", skill_dir.name)
            raw_desc = fm.get("description", "")
            description = re.sub(r'\s+', ' ', raw_desc).strip()

            when_to_use = extract_triggers(description)
            how_to_use = extract_section(
                content,
                "Workflow", "Process", "Quick start",
                "How to use", "Usage", "Protocol",
            )

            # short tagline = everything BEFORE "Use when"
            short = re.split(r'\.\s*[Uu]se when', description)[0].strip()

            cat_skills.append({
                "name": name,
                "slug": skill_dir.name,
                "category": category,
                "path": f"skills/{category}/{skill_dir.name}/SKILL.md",
                "description": description,
                "tagline": short,
                "when_to_use": when_to_use,
                "how_to_use": how_to_use,
            })
        skills[category] = cat_skills
    return skills


# ─── icon map ─────────────────────────────────────────────────────────────────

ICONS: dict[str, str] = {
    "debug":                    "🐛",
    "arch-audit":               "🏛️",
    "tdd":                      "🧪",
    "ai-architecture":          "🤖",
    "to-prd":                   "📋",
    "to-tasks":                 "✅",
    "triage":                   "🚦",
    "big-picture":              "🗺️",
    "plan-and-build-with-me":   "👩‍💻",
    "repo-intelligence":        "🔍",
    "semantic-memory":          "🧠",
    "assumption-hunter":        "🎯",
    "architecture-lineage":     "📜",
    "decision-cascade":         "🌊",
    "first-principles":         "⚛️",
    "knowledge-spike":          "⚡",
    "multi-agent-orchestrator": "🕸️",
    "plan-with-me-with-docs":   "📝",
    "prompt-coach":             "🎓",
    "session-handoff":          "🤝",
    "skill-factory":            "🏭",
    "init-skills":              "🚀",
    "vuln-scanner":             "🛡️",
    "forge-skill":              "⚒️",
    "idea-accelerator":         "💡",
    "plan-with-me":             "🧭",
    "token-saver":              "💾",
    "upgrade-agent-pack":       "🔄",
}


def icon(slug: str) -> str:
    return ICONS.get(slug, "🔧")


# ─── HTML generation ──────────────────────────────────────────────────────────

def skill_card_html(skill: dict) -> str:
    ic = icon(skill["slug"])
    when = skill["when_to_use"].replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;') if skill["when_to_use"] else ""
    how = skill["how_to_use"].replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;') if skill["how_to_use"] else ""
    tagline = skill["tagline"].replace('<', '&lt;').replace('>', '&gt;')
    when_badge = (
        f'<div class="trigger-tag"><span class="trigger-label">When to use</span>'
        f'<p class="trigger-text">{when}</p></div>'
    ) if when else ""
    how_block = (
        f'<div class="how-section"><h4 class="how-label">How it works</h4>'
        f'<p class="how-text">{how[:300]}{"…" if len(how) > 300 else ""}</p></div>'
    ) if how else ""

    return f"""
      <article class="card" data-name="{skill['name']}" data-category="{skill['category']}">
        <div class="card-header">
          <span class="card-icon">{ic}</span>
          <div class="card-title-group">
            <h3 class="card-name">{skill['name']}</h3>
            <span class="cat-badge {skill['category']}">{skill['category']}</span>
          </div>
        </div>
        <p class="card-tagline">{tagline}</p>
        {when_badge}
        <details class="card-details">
          <summary class="card-summary">More details</summary>
          {how_block}
          <a class="skill-link" href="{skill['path']}" target="_blank">Open SKILL.md →</a>
        </details>
      </article>
"""


def generate_html(skills: dict) -> str:
    all_skills = skills.get("engineering", []) + skills.get("productivity", [])
    eng_count = len(skills.get("engineering", []))
    prod_count = len(skills.get("productivity", []))
    total = eng_count + prod_count
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    cards_html = "".join(skill_card_html(s) for s in all_skills)

    # serialise for JS search/filter
    skills_json = json.dumps(
        [{"name": s["name"], "slug": s["slug"], "category": s["category"],
          "description": s["description"], "when_to_use": s["when_to_use"]}
         for s in all_skills],
        ensure_ascii=False,
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Agent Skills Dashboard</title>
  <style>
    /* ── tokens ── */
    :root {{
      --bg:          #faf9f7;
      --surface:     #ffffff;
      --surface-2:   #f5f3f0;
      --border:      #e8e4de;
      --border-2:    #d5d0c8;
      --text:        #1a1814;
      --text-muted:  #6b6560;
      --text-subtle: #9b948c;
      --accent:      #d97757;
      --accent-2:    #bf5e3e;
      --accent-bg:   #fdf2ee;
      --eng-color:   #5b6af0;
      --eng-bg:      #eef0fd;
      --prod-color:  #2ea87e;
      --prod-bg:     #e8f7f2;
      --radius:      12px;
      --radius-sm:   8px;
      --shadow:      0 1px 4px rgba(0,0,0,.06), 0 4px 16px rgba(0,0,0,.04);
      --shadow-hover:0 4px 12px rgba(0,0,0,.10), 0 12px 32px rgba(0,0,0,.06);
      --font:        -apple-system, BlinkMacSystemFont, "Segoe UI", "Inter", system-ui, sans-serif;
      --mono:        "JetBrains Mono", "Fira Code", "Cascadia Code", ui-monospace, monospace;
      --transition:  0.2s ease;
    }}

    /* ── reset ── */
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      font-family: var(--font);
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
      min-height: 100vh;
    }}

    /* ── header ── */
    .site-header {{
      background: var(--text);
      color: #fff;
      padding: 0 2rem;
      position: sticky;
      top: 0;
      z-index: 100;
      display: flex;
      align-items: center;
      justify-content: space-between;
      height: 58px;
      box-shadow: 0 1px 0 rgba(255,255,255,.1);
    }}
    .site-logo {{
      display: flex;
      align-items: center;
      gap: .6rem;
      font-weight: 700;
      font-size: 1.05rem;
      letter-spacing: -.01em;
      color: #fff;
      text-decoration: none;
    }}
    .logo-dot {{
      width: 28px;
      height: 28px;
      border-radius: 8px;
      background: var(--accent);
      display: grid;
      place-items: center;
      font-size: 15px;
      flex-shrink: 0;
    }}
    .header-meta {{
      font-size: .78rem;
      color: rgba(255,255,255,.45);
    }}

    /* ── hero ── */
    .hero {{
      padding: 3.5rem 2rem 2.5rem;
      text-align: center;
      max-width: 680px;
      margin: 0 auto;
    }}
    .hero-eyebrow {{
      display: inline-flex;
      align-items: center;
      gap: .4rem;
      background: var(--accent-bg);
      color: var(--accent-2);
      border: 1px solid #f3d0c2;
      border-radius: 999px;
      font-size: .78rem;
      font-weight: 600;
      padding: .25rem .75rem;
      margin-bottom: 1.25rem;
      letter-spacing: .02em;
    }}
    .hero h1 {{
      font-size: clamp(1.8rem, 4vw, 2.6rem);
      font-weight: 800;
      letter-spacing: -.03em;
      line-height: 1.15;
      color: var(--text);
      margin-bottom: .75rem;
    }}
    .hero h1 span {{ color: var(--accent); }}
    .hero p {{
      color: var(--text-muted);
      font-size: 1.05rem;
      max-width: 500px;
      margin: 0 auto 2rem;
    }}

    /* ── stats row ── */
    .stats {{
      display: flex;
      justify-content: center;
      gap: 1.5rem;
      flex-wrap: wrap;
      margin-bottom: 2.5rem;
    }}
    .stat-pill {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 999px;
      padding: .4rem 1rem;
      font-size: .85rem;
      display: flex;
      align-items: center;
      gap: .5rem;
      color: var(--text-muted);
      font-weight: 500;
    }}
    .stat-pill strong {{ color: var(--text); }}

    /* ── controls ── */
    .controls {{
      max-width: 900px;
      margin: 0 auto 2rem;
      padding: 0 2rem;
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }}
    .search-wrap {{
      position: relative;
    }}
    .search-wrap svg {{
      position: absolute;
      left: 14px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-subtle);
      pointer-events: none;
    }}
    #search {{
      width: 100%;
      padding: .7rem 1rem .7rem 2.75rem;
      border: 1.5px solid var(--border);
      border-radius: var(--radius-sm);
      font-size: .95rem;
      font-family: var(--font);
      background: var(--surface);
      color: var(--text);
      outline: none;
      transition: border-color var(--transition), box-shadow var(--transition);
    }}
    #search:focus {{
      border-color: var(--accent);
      box-shadow: 0 0 0 3px rgba(217,119,87,.15);
    }}
    #search::placeholder {{ color: var(--text-subtle); }}

    .filter-tabs {{
      display: flex;
      gap: .5rem;
      flex-wrap: wrap;
    }}
    .tab {{
      padding: .4rem 1rem;
      border-radius: 999px;
      border: 1.5px solid var(--border);
      background: var(--surface);
      color: var(--text-muted);
      font-size: .85rem;
      font-weight: 500;
      cursor: pointer;
      transition: all var(--transition);
      font-family: var(--font);
    }}
    .tab:hover {{ border-color: var(--accent); color: var(--accent); }}
    .tab.active {{
      background: var(--text);
      border-color: var(--text);
      color: #fff;
    }}
    .tab.active.eng {{ background: var(--eng-color); border-color: var(--eng-color); }}
    .tab.active.prod {{ background: var(--prod-color); border-color: var(--prod-color); }}

    /* ── grid ── */
    .grid-wrap {{
      max-width: 1180px;
      margin: 0 auto;
      padding: 0 2rem 4rem;
    }}
    .empty-state {{
      text-align: center;
      padding: 4rem 2rem;
      color: var(--text-muted);
      display: none;
    }}
    .empty-state svg {{ opacity: .3; margin-bottom: .75rem; }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 1.25rem;
    }}

    /* ── card ── */
    .card {{
      background: var(--surface);
      border: 1.5px solid var(--border);
      border-radius: var(--radius);
      padding: 1.4rem;
      display: flex;
      flex-direction: column;
      gap: .85rem;
      transition: box-shadow var(--transition), border-color var(--transition), transform var(--transition);
      cursor: default;
    }}
    .card:hover {{
      box-shadow: var(--shadow-hover);
      border-color: var(--border-2);
      transform: translateY(-2px);
    }}
    .card.hidden {{ display: none; }}

    .card-header {{
      display: flex;
      align-items: flex-start;
      gap: .85rem;
    }}
    .card-icon {{
      font-size: 1.6rem;
      line-height: 1;
      flex-shrink: 0;
      width: 42px;
      height: 42px;
      background: var(--surface-2);
      border-radius: var(--radius-sm);
      display: grid;
      place-items: center;
      border: 1px solid var(--border);
    }}
    .card-title-group {{
      display: flex;
      flex-direction: column;
      gap: .25rem;
    }}
    .card-name {{
      font-size: 1rem;
      font-weight: 700;
      color: var(--text);
      line-height: 1.25;
      font-family: var(--mono);
      letter-spacing: -.01em;
    }}
    .cat-badge {{
      display: inline-block;
      padding: .15rem .5rem;
      border-radius: 4px;
      font-size: .7rem;
      font-weight: 600;
      letter-spacing: .04em;
      text-transform: uppercase;
    }}
    .cat-badge.engineering  {{ background: var(--eng-bg);  color: var(--eng-color);  }}
    .cat-badge.productivity {{ background: var(--prod-bg); color: var(--prod-color); }}

    .card-tagline {{
      font-size: .875rem;
      color: var(--text-muted);
      line-height: 1.55;
    }}

    .trigger-tag {{
      background: var(--accent-bg);
      border: 1px solid #f3d0c2;
      border-radius: var(--radius-sm);
      padding: .65rem .85rem;
    }}
    .trigger-label {{
      font-size: .7rem;
      font-weight: 700;
      letter-spacing: .06em;
      text-transform: uppercase;
      color: var(--accent-2);
      display: block;
      margin-bottom: .3rem;
    }}
    .trigger-text {{
      font-size: .83rem;
      color: #7a4030;
      line-height: 1.5;
    }}

    /* ── details / accordion ── */
    .card-details {{ margin-top: auto; }}
    .card-summary {{
      font-size: .82rem;
      font-weight: 600;
      color: var(--text-subtle);
      cursor: pointer;
      list-style: none;
      display: flex;
      align-items: center;
      gap: .35rem;
      padding: .3rem 0;
      user-select: none;
      transition: color var(--transition);
    }}
    .card-summary::-webkit-details-marker {{ display: none; }}
    .card-summary::before {{
      content: "▶";
      font-size: .65rem;
      transition: transform var(--transition);
    }}
    details[open] .card-summary::before {{ transform: rotate(90deg); }}
    .card-summary:hover {{ color: var(--accent); }}

    .how-section {{
      margin-top: .85rem;
      padding-top: .85rem;
      border-top: 1px solid var(--border);
    }}
    .how-label {{
      font-size: .72rem;
      font-weight: 700;
      letter-spacing: .06em;
      text-transform: uppercase;
      color: var(--text-subtle);
      margin-bottom: .45rem;
    }}
    .how-text {{
      font-size: .82rem;
      color: var(--text-muted);
      line-height: 1.6;
      white-space: pre-wrap;
    }}

    .skill-link {{
      display: inline-block;
      margin-top: .85rem;
      font-size: .8rem;
      font-weight: 600;
      color: var(--accent);
      text-decoration: none;
    }}
    .skill-link:hover {{ text-decoration: underline; }}

    /* ── footer ── */
    footer {{
      border-top: 1px solid var(--border);
      padding: 1.5rem 2rem;
      text-align: center;
      color: var(--text-subtle);
      font-size: .8rem;
    }}
    footer a {{ color: var(--accent); text-decoration: none; }}
    footer a:hover {{ text-decoration: underline; }}

    /* ── responsive ── */
    @media (max-width: 600px) {{
      .hero {{ padding: 2rem 1rem 1.5rem; }}
      .controls, .grid-wrap {{ padding-left: 1rem; padding-right: 1rem; }}
      .grid {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>

<!-- ── header ─────────────────────────────────────────────── -->
<header class="site-header">
  <a class="site-logo" href="#">
    <span class="logo-dot">⚡</span>
    Agent Skills
  </a>
  <span class="header-meta">Generated {generated_at}</span>
</header>

<!-- ── hero ───────────────────────────────────────────────── -->
<section class="hero">
  <div class="hero-eyebrow">
    <span>🧩</span> gagangoswami/skills
  </div>
  <h1>Agent <span>Skills</span> Dashboard</h1>
  <p>All {total} reusable AI agent skills — find what you need fast, understand when and how to use each one.</p>
  <div class="stats">
    <span class="stat-pill"><strong>{total}</strong> total skills</span>
    <span class="stat-pill"><strong>{eng_count}</strong> engineering</span>
    <span class="stat-pill"><strong>{prod_count}</strong> productivity</span>
  </div>
</section>

<!-- ── controls ────────────────────────────────────────────── -->
<div class="controls">
  <div class="search-wrap">
    <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
      <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
    </svg>
    <input id="search" type="search" placeholder="Search skills, descriptions, triggers…" autocomplete="off" />
  </div>
  <div class="filter-tabs">
    <button class="tab active" data-filter="all">All ({total})</button>
    <button class="tab eng" data-filter="engineering">Engineering ({eng_count})</button>
    <button class="tab prod" data-filter="productivity">Productivity ({prod_count})</button>
  </div>
</div>

<!-- ── grid ────────────────────────────────────────────────── -->
<div class="grid-wrap">
  <div class="empty-state" id="emptyState">
    <svg width="48" height="48" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
      <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
    </svg>
    <p>No skills match your search.</p>
  </div>
  <div class="grid" id="grid">
{cards_html}
  </div>
</div>

<!-- ── footer ──────────────────────────────────────────────── -->
<footer>
  Auto-generated by <code>scripts/generate-dashboard.py</code> &nbsp;·&nbsp;
  <a href="https://github.com/GaganGoswami/skills" target="_blank">GaganGoswami/skills</a>
  &nbsp;·&nbsp; {generated_at}
</footer>

<!-- ── search + filter JS ──────────────────────────────────── -->
<script>
  const SKILLS = {skills_json};

  const searchEl  = document.getElementById('search');
  const gridEl    = document.getElementById('grid');
  const emptyEl   = document.getElementById('emptyState');
  const cards     = Array.from(gridEl.querySelectorAll('.card'));
  const tabs      = Array.from(document.querySelectorAll('.tab'));

  let activeFilter = 'all';
  let searchQuery  = '';

  function normalize(s) {{ return s.toLowerCase(); }}

  function applyFilters() {{
    let visible = 0;
    cards.forEach((card, i) => {{
      const skill    = SKILLS[i];
      const catMatch = activeFilter === 'all' || skill.category === activeFilter;
      const q        = normalize(searchQuery);
      const textMatch = !q
        || normalize(skill.name).includes(q)
        || normalize(skill.description).includes(q)
        || normalize(skill.when_to_use).includes(q);

      if (catMatch && textMatch) {{
        card.classList.remove('hidden');
        visible++;
      }} else {{
        card.classList.add('hidden');
      }}
    }});
    emptyEl.style.display = visible === 0 ? 'block' : 'none';
  }}

  searchEl.addEventListener('input', e => {{
    searchQuery = e.target.value.trim();
    applyFilters();
  }});

  tabs.forEach(tab => {{
    tab.addEventListener('click', () => {{
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      activeFilter = tab.dataset.filter;
      applyFilters();
    }});
  }});
</script>
</body>
</html>
"""


# ─── entry point ──────────────────────────────────────────────────────────────

def main() -> int:
    skills = collect_skills()
    html = generate_html(skills)
    OUTPUT.write_text(html, encoding="utf-8")
    total = sum(len(v) for v in skills.values())
    print(f"✓ dashboard.html regenerated — {total} skills across "
          f"{', '.join(f'{len(v)} {k}' for k, v in skills.items())}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
