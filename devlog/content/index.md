# dev.log

<div class="hero">
<span class="prompt">$</span> <span class="out">whoami</span><br>
a build-notes site for Minecraft add-ons/plugins, Discord bots, and the languages behind them.
</div>

This is a personal reference wiki, not a course — short, practical write-ups you can skim while you're actually building something, with real commands and copy-pasteable code instead of theory.

## What's inside

<div class="card-grid">

<div class="card">
<span class="tag mc">bedrock</span><br>
<a href="pages/bedrock-getting-started.html">Bedrock Script API</a>
<p>Behavior packs, manifests, and the @minecraft/server module.</p>
</div>

<div class="card">
<span class="tag mc">bedrock</span><br>
<a href="pages/bedrock-forms-ui.html">Bedrock Forms & UI</a>
<p>ActionFormData, ModalFormData, MessageFormData and custom menu screens.</p>
</div>

<div class="card">
<span class="tag java">java plugins</span><br>
<a href="pages/java-plugin-setup.html">Spigot/Paper + Maven</a>
<p>Project layout, pom.xml, and your first plugin.</p>
</div>

<div class="card">
<span class="tag java">java plugins</span><br>
<a href="pages/java-decompile-jar.html">Decompiling a .jar</a>
<p>Turning compiled bytecode back into readable .java files.</p>
</div>

<div class="card">
<span class="tag discord">discord</span><br>
<a href="pages/discord-jda-setup.html">JDA Bot Setup</a>
<p>A Java Discord bot from zero, with slash commands.</p>
</div>

<div class="card">
<span class="tag lang">languages</span><br>
<a href="pages/lang-typescript.html">18 language references</a>
<p>JS, TS, HTML/CSS, PHP, React, Go, Python, Java, C#, C, C++, Rust, Swift, Kotlin, SQL, shell &amp; Node.</p>
</div>

</div>

## Sections

- **Minecraft: Bedrock Scripting** — the `@minecraft/server` and `@minecraft/server-ui` APIs: events, custom commands, forms/GUIs, custom item & block components, and saving data with dynamic properties.
- **Minecraft: Java Plugins** — Maven project setup, building and uploading `.jar` files to a real server, decompiling `.jar` files back to source, custom inventory GUIs, and the "everyone builds this eventually" systems: economy, permissions, commands.
- **Discord Bots (Java)** — setting up JDA with Maven, and the slash-command / button / embed systems almost every bot needs.
- **Language References** — a fast-start cheat sheet per language: toolchain setup, core syntax, the libraries people actually reach for, and one worked example.

> These pages assume you're comfortable in a terminal and have a code editor (VS Code is the common choice across every section here). Version numbers move fast — treat exact numbers in code blocks as "as of writing" and check the linked docs if something's changed.

## Contributing

The whole site builds from plain Markdown files in `content/`. Clone the repo, add a `.md` file, wire it into `MANIFEST` in `build.py`, run `python3 build.py`, and open a pull request.
