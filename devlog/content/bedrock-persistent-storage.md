# Saving Data (Dynamic Properties)

Scripts don't have filesystem access, so persistence goes through **dynamic properties**, key/value data Mojang stores in the world save for you, attached to the world itself, an entity, or an item stack.

## Register properties at startup

You must declare properties (name + type) before you can use them:

```js
import { world, system } from "@minecraft/server";

system.beforeEvents.startup.subscribe(({ propertyRegistry }) => {
  propertyRegistry.registerWorldDynamicProperties(
    new DynamicPropertiesDefinition()
      .defineNumber("myaddon:coins_total")
      .defineString("myaddon:event_name", 32)
  );
});
```

*(Newer API revisions relaxed this and let you set properties directly on `world`/entities without pre-registration, check the changelog for the API version pinned in your manifest.)*

## World-level data (global save, e.g. a shared economy total)

```js
world.setDynamicProperty("myaddon:coins_total", 500);
const total = world.getDynamicProperty("myaddon:coins_total") ?? 0;
```

## Per-player data

```js
function getCoins(player) {
  return player.getDynamicProperty("myaddon:coins") ?? 0;
}
function addCoins(player, amount) {
  player.setDynamicProperty("myaddon:coins", getCoins(player) + amount);
}
```

## Storing structured data (objects, arrays)

Dynamic properties only store primitives (number, string, boolean), for anything richer, serialize to JSON. Mind the string length limit (currently ~32,767 chars per property):

```js
function saveInventoryBackup(player, items) {
  player.setDynamicProperty("myaddon:inv_backup", JSON.stringify(items));
}
function loadInventoryBackup(player) {
  const raw = player.getDynamicProperty("myaddon:inv_backup");
  return raw ? JSON.parse(raw) : [];
}
```

## Scoreboards as a lightweight alternative

For simple numeric data you also want visible to players (leaderboards, sidebar), a vanilla scoreboard objective is often simpler than dynamic properties and survives without any registration step:

```js
player.runCommand("scoreboard objectives add coins dummy Coins");
player.runCommand(`scoreboard players set @s coins ${amount}`);
```

Read it back with `/scoreboard players get`, though there's no direct script "get" for scoreboard values, you'd parse a command's output or keep the source of truth in a dynamic property and mirror it to the scoreboard for display only.

## A minimal per-player currency system

```js
import { world } from "@minecraft/server";

world.afterEvents.entityDie.subscribe((e) => {
  if (e.deadEntity.typeId !== "minecraft:zombie") return;
  const killer = e.damageSource.damagingEntity;
  if (killer?.typeId !== "minecraft:player") return;
  addCoins(killer, 10);
  killer.sendMessage(`§e+10 coins §7(total: ${getCoins(killer)})`);
});

function getCoins(p) { return p.getDynamicProperty("myaddon:coins") ?? 0; }
function addCoins(p, n) { p.setDynamicProperty("myaddon:coins", getCoins(p) + n); }
```

That's the whole loop: register once at startup, read/write with `get`/`setDynamicProperty`, JSON-encode anything non-primitive, and reach for scoreboards only when you specifically need vanilla UI (sidebar, tab list) to show the number.
