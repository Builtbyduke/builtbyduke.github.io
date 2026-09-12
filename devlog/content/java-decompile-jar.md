# Decompiling a .jar to .java

Sometimes you need to see how a compiled plugin (yours from years ago with lost source, or a third-party one you have permission to inspect/patch) actually works. A `.jar` is just a zip of `.class` bytecode files — a **decompiler** turns that bytecode back into readable, mostly-recompilable Java source.

> **Only decompile jars you have the right to inspect** — your own lost-source projects, open-source plugins, or anything whose license explicitly allows it. Decompiling to redistribute or bypass a paid plugin's licensing violates most plugin marketplace terms.

## Option 1: CFR (simplest, single jar, no GUI)

[CFR](https://www.benf.org/other/cfr/) is a single-file decompiler — good for scripting/batch use.

```bash
# download cfr-0.152.jar from the CFR site into your working folder, then:
mkdir out
java -jar cfr-0.152.jar my-plugin.jar --outputdir out
```

That dumps a full `.java` source tree into `out/`, mirroring the original package structure.

## Option 2: Fernflower (what most IDEs use internally)

IntelliJ IDEA ships Fernflower and will decompile automatically the moment you open a `.class` file from inside a jar — no setup needed:

1. **File → Open** the `.jar` itself (IntelliJ browses it like a folder).
2. Navigate to any `.class` file and double-click it.
3. IntelliJ decompiles on the fly and shows readable Java (with a banner noting it's decompiled).
4. Right-click the package → **Extract to `.java` files** isn't automatic, but you can copy the decompiled text into new `.java` files under `src/` if you want a real, editable tree.

For a full batch export without opening a whole project, the standalone Fernflower jar works the same way as CFR:

```bash
java -jar fernflower.jar my-plugin.jar out/
```

## Option 3: JD-GUI (visual browsing)

[JD-GUI](https://java-decompiler.github.io/) is a lightweight desktop app — drag a `.jar` onto it, click through the package tree in a Swing UI, and use **File → Save All Sources** to export a `.jar` of decompiled `.java` files (unzip that to get real files on disk).

## Option 4: bytecode-viewer (all of the above, one tool)

[Bytecode Viewer](https://github.com/Konloch/bytecode-viewer) bundles CFR, Fernflower, Procyon, and a bytecode/ASM view side-by-side — useful when one decompiler produces broken output (common with heavily obfuscated jars) and you want to cross-check against another.

## Turning the output into a working Maven project

Once you have a `src/` tree of `.java` files:

1. Create a fresh Maven project (see [plugin setup](java-plugin-setup.html)) with a matching `paper-api` dependency version.
2. Copy the decompiled tree into `src/main/java/...`, preserving package folders.
3. Expect compile errors — decompilers approximate lambdas, generics, and switch expressions, and any code the plugin loaded from other dependency jars won't resolve unless you also add those as Maven dependencies.
4. Fix errors top-down; decompiled code is a **starting point**, not guaranteed to compile as-is.

## Obfuscated jars

If class/method names come out as `a`, `b`, `c` — the jar was obfuscated (commonly with ProGuard). Decompilers still produce valid-ish Java, just with meaningless names; a deobfuscation mapping file (if the author ever published one) is the only way to get real names back. Without one, expect to manually rename things as you understand what they do.

Next: [Inventory GUI Menus](java-plugin-guis.html).
