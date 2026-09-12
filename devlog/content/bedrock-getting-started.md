# Getting Started with the Bedrock Script API

Minecraft Bedrock add-ons are split into **packs**: a *behavior pack* (logic, entities, scripts) and usually a matching *resource pack* (textures, models, sounds). Scripting lives inside a behavior pack and is powered by the `@minecraft/server` module, Mojang's own JavaScript/TypeScript API, run inside the game.

## Folder layout

Behavior packs live under your game's `development_behavior_packs` folder so they hot-reload with `/reload`.

```
development_behavior_packs/
  my_addon_bp/
    manifest.json
    scripts/
      main.js
    pack_icon.png
```

Find the folder:
- **Windows**: `%localappdata%\Packages\Microsoft.MinecraftUWP_8wekyb3d8bbwe\LocalState\games\com.mojang\development_behavior_packs`
- **Preview/Education editions** use a similarly named package folder, search for `com.mojang`.

## manifest.json

Every pack needs a manifest declaring its modules. A scripting-enabled behavior pack needs a `data` module **and** a `script` module, plus a dependency on the `@minecraft/server` API:

```json
{
  "format_version": 2,
  "header": {
    "name": "My Addon",
    "description": "Custom scripted systems",
    "uuid": "3f1b1e2a-2222-4c3e-9a11-000000000001",
    "version": [1, 0, 0],
    "min_engine_version": [1, 21, 0]
  },
  "modules": [
    {
      "type": "data",
      "uuid": "3f1b1e2a-2222-4c3e-9a11-000000000002",
      "version": [1, 0, 0]
    },
    {
      "type": "script",
      "language": "javascript",
      "uuid": "3f1b1e2a-2222-4c3e-9a11-000000000003",
      "version": [1, 0, 0],
      "entry": "scripts/main.js"
    }
  ],
  "dependencies": [
    { "module_name": "@minecraft/server", "version": "1.15.0" },
    { "module_name": "@minecraft/server-ui", "version": "1.2.0" }
  ]
}
```

Generate fresh UUIDs (e.g. with `uuidgen` or an online v4 generator), never reuse the sample ones above, or Minecraft will treat two different packs as the same pack.

## Your first script

```js
import { world, system } from "@minecraft/server";

world.afterEvents.playerSpawn.subscribe((event) => {
  const { player, initialSpawn } = event;
  if (initialSpawn) {
    player.sendMessage("§a[Addon]§r Welcome, " + player.name + "!");
  }
});

system.runInterval(() => {
  world.sendMessage("Tick check-in every 5 seconds");
}, 100); // 100 ticks = 5s (20 ticks/sec)
```

Enable the pack on a world (**must** turn on *Beta APIs* under Experiments), then run `/reload` in-game while you edit, no restart needed.

## TypeScript instead of raw JS

Most real projects use TypeScript + `esbuild`/`webpack` to bundle down to a single `.js` your pack loads, so you get autocomplete against Mojang's type defs.

```bash
npm init -y
npm i -D typescript esbuild @minecraft/server @minecraft/server-ui
```

`tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ES2020",
    "moduleResolution": "node",
    "strict": true,
    "outDir": "dist"
  }
}
```

Bundle command (drop the output straight into your pack's `scripts/` folder):

```bash
npx esbuild src/main.ts --bundle --outfile=development_behavior_packs/my_addon_bp/scripts/main.js --external:@minecraft/server --external:@minecraft/server-ui --format=esm
```

## Key modules you'll import constantly

| Module | What it's for |
|---|---|
| `@minecraft/server` | Core: `world`, `system`, entities, blocks, events |
| `@minecraft/server-ui` | Forms/menus (`ActionFormData`, `ModalFormData`, `MessageFormData`) |
| `@minecraft/server-gametest` | Automated testing of your logic |
| `@minecraft/server-net` | Outbound HTTP from scripts (limited, opt-in) |

## Debugging

- `console.warn(...)` / `console.error(...)` show up in the **Content Log** (enable it under Settings → Creator).
- Use the **Script Debugger** in a code editor (VS Code + the "Minecraft Bedrock Edition" extension) to set real breakpoints against a running world.
- `world.sendMessage()` is the fastest "print statement" for quick checks.

Next: [Custom Commands & Events](bedrock-events-commands.html) or straight to [Forms & UI](bedrock-forms-ui.html) if you want menus first.
