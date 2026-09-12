#!/usr/bin/env python3
import os, re, markdown, shutil, json

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(ROOT, "content")
# Writes directly back into this folder (pages/, assets/, index.html) since
# this devlog/ directory is itself the published sub-site.
OUT = ROOT

# ---- Manifest: defines nav structure & page order -------------------------
MANIFEST = [
    ("Minecraft: Bedrock Scripting", "bedrock", [
        ("bedrock-getting-started", "Getting Started with Script API"),
        ("bedrock-events-commands", "Custom Commands & Events"),
        ("bedrock-forms-ui", "Forms & UI (GUIs)"),
        ("bedrock-custom-components", "Custom Items & Blocks"),
        ("bedrock-persistent-storage", "Saving Data (Dynamic Properties)"),
    ]),
    ("Minecraft: Java Plugins", "java-plugin", [
        ("java-plugin-setup", "Maven Project Setup"),
        ("java-plugin-build-deploy", "Building & Uploading to a Server"),
        ("java-decompile-jar", "Decompiling a .jar to .java"),
        ("java-plugin-guis", "Inventory GUI Menus"),
        ("java-plugin-common-systems", "Economy, Permissions & Commands"),
    ]),
    ("Discord Bots (Java)", "discord", [
        ("discord-jda-setup", "JDA Project Setup"),
        ("discord-jda-commands", "Slash Commands, Buttons & Embeds"),
    ]),
    ("Language References", "lang", [
        ("lang-javascript", "JavaScript"),
        ("lang-typescript", "TypeScript"),
        ("lang-html", "HTML"),
        ("lang-css", "CSS"),
        ("lang-node", "Node.js"),
        ("lang-react", "React"),
        ("lang-php", "PHP"),
        ("lang-python", "Python"),
        ("lang-java", "Java"),
        ("lang-csharp", "C#"),
        ("lang-c", "C"),
        ("lang-cpp", "C++"),
        ("lang-go", "Go"),
        ("lang-rust", "Rust"),
        ("lang-swift", "Swift"),
        ("lang-kotlin", "Kotlin"),
        ("lang-sql", "SQL"),
        ("lang-shell", "Shell / Bash"),
    ]),
]

CATEGORY_ICON = {
    "bedrock": "▣",
    "java-plugin": "☕",
    "discord": "◆",
    "lang": "⌘",
}

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} · dev.log</title>
<meta name="description" content="{desc}">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 16 16%22><text y=%2213%22 font-size=%2214%22>&#9646;</text></svg>">
<link rel="stylesheet" href="{root}assets/style.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/base16/tomorrow-night.min.css">
</head>
<body>
<div class="skiplink"><a href="#main">Skip to content</a></div>
<div class="shell">
  <button id="navToggle" class="nav-toggle" aria-label="Toggle navigation" aria-expanded="false">☰ menu</button>
  <nav class="sidebar" id="sidebar">
    <a class="brand" href="{root}index.html"><span class="brand-mark">▣</span> dev.log<span class="cursor">_</span></a>
    <div class="brand-sub"># Minecraft &amp; multi-language build notes</div>
    <a class="back-home" href="{home}index.html">&larr; BuiltByDuke.github.io</a>
    {nav}
  </nav>
  <main id="main" class="content">
    <div class="titlebar"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span><span class="path">~/dev.log/{slug}</span></div>
    <article class="prose">
    {body}
    </article>
    <footer class="page-footer">
      <p>Found a mistake or want to extend this? Fork the repo and send a PR — this whole site is just markdown files under <code>content/</code>.</p>
    </footer>
  </main>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<script>hljs.highlightAll();</script>
<script src="{root}assets/nav.js"></script>
</body>
</html>
"""

def build_nav(active_slug, root_prefix):
    out = []
    for cat_title, cat_key, pages in MANIFEST:
        out.append(f'<div class="nav-group"><div class="nav-group-title">{CATEGORY_ICON.get(cat_key,"·")} {cat_title}</div><ul>')
        for slug, label in pages:
            cls = ' class="active"' if slug == active_slug else ''
            out.append(f'<li><a href="{root_prefix}pages/{slug}.html"{cls}>{label}</a></li>')
        out.append('</ul></div>')
    return "\n".join(out)

def md_to_html(md_text):
    return markdown.markdown(md_text, extensions=["fenced_code", "tables", "toc", "sane_lists"])

def first_h1_and_rest(md_text):
    lines = md_text.strip().splitlines()
    title = "Untitled"
    if lines and lines[0].startswith("# "):
        title = lines[0][2:].strip()
        lines = lines[1:]
    return title, "\n".join(lines)

def main():
    # Only clear the generated pages/ dir; leave content/, assets/, build.py etc. alone.
    pages_dir = os.path.join(OUT, "pages")
    if os.path.exists(pages_dir):
        shutil.rmtree(pages_dir)
    os.makedirs(pages_dir)
    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)

    all_pages = []
    for cat_title, cat_key, pages in MANIFEST:
        for slug, label in pages:
            all_pages.append((slug, label, cat_title))

    for slug, label, cat_title in all_pages:
        md_path = os.path.join(CONTENT, f"{slug}.md")
        if not os.path.exists(md_path):
            print(f"MISSING: {md_path}")
            continue
        with open(md_path, encoding="utf-8") as f:
            raw = f.read()
        title, rest = first_h1_and_rest(raw)
        body = md_to_html(rest)
        nav_html = build_nav(slug, "../")
        html = TEMPLATE.format(
            title=title, desc=f"{title} — {cat_title} tutorial", root="../", home="../../",
            nav=nav_html, slug=slug, body=body
        )
        with open(os.path.join(OUT, "pages", f"{slug}.html"), "w", encoding="utf-8") as f:
            f.write(html)

    # Build index.html
    with open(os.path.join(CONTENT, "index.md"), encoding="utf-8") as f:
        raw = f.read()
    title, rest = first_h1_and_rest(raw)
    body = md_to_html(rest)
    nav_html = build_nav(None, "")
    html = TEMPLATE.format(
        title="Home", desc="Minecraft Bedrock & Java plugin tutorials, Discord bots, and language references",
        root="", home="../", nav=nav_html, slug="index", body=body
    )
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(html.replace('href="assets/', 'href="assets/').replace('src="assets/', 'src="assets/'))

    # .nojekyll + README
    open(os.path.join(OUT, ".nojekyll"), "w").close()
    print("Build complete:", OUT)
    print("Pages built:", len(all_pages) + 1)

if __name__ == "__main__":
    main()
