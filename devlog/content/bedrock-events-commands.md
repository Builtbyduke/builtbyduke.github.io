# Custom Commands & Events

Two systems drive almost every Bedrock add-on: **events** (react to something that happened) and **custom commands** (let a player or another script trigger your logic on demand).

## Common world events

```js
import { world } from "@minecraft/server";

world.afterEvents.entityHurt.subscribe((e) => {
  console.warn(`${e.hurtEntity.typeId} took ${e.damage} damage`);
});

world.afterEvents.blockPlace.subscribe((e) => {
  if (e.block.typeId === "minecraft:diamond_block") {
    e.player.sendMessage("§bNice.");
  }
});

world.beforeEvents.chatSend.subscribe((e) => {
  if (e.message.startsWith("!")) {
    e.cancel = true; // swallow the chat message
    // handle it as a pseudo-command yourself
  }
});
```

`beforeEvents` run synchronously and can cancel/mutate; `afterEvents` are read-only notifications after the fact. Most gameplay logic belongs in `afterEvents` — `beforeEvents` are reserved for the handful of events that support cancellation.

## Slash commands via `/scriptevent`

The cleanest way to expose a command players (or command blocks / functions) can call is `system.afterEvents.scriptEventReceive`, paired with a namespace so it doesn't collide with other add-ons:

```js
import { system } from "@minecraft/server";

system.afterEvents.scriptEventReceive.subscribe((event) => {
  const { id, message, sourceEntity } = event;
  if (id !== "myaddon:kit") return;

  const kit = message; // e.g. "/scriptevent myaddon:kit starter"
  giveKit(sourceEntity, kit);
});
```

Register the namespace in `manifest.json` so `/scriptevent` autocompletes it:

```json
"metadata": {
  "authors": ["you"],
  "namespace": "myaddon"
}
```

## Custom commands (1.21+ `@minecraft/server` command registry)

Newer API versions let scripts register real slash commands (no `/scriptevent` prefix needed) via the experimental custom-commands API:

```js
import { system, CustomCommandStatus, CustomCommandParamType } from "@minecraft/server";

system.beforeEvents.startup.subscribe(({ customCommandRegistry }) => {
  customCommandRegistry.registerCommand(
    {
      name: "myaddon:heal",
      description: "Heal yourself",
      permissionLevel: 0,
      optionalParameters: [{ name: "amount", type: CustomCommandParamType.Integer }]
    },
    (origin, amount) => {
      const player = origin.sourceEntity;
      player?.runCommand(`effect @s instant_health 1 ${amount ?? 1}`);
      return { status: CustomCommandStatus.Success };
    }
  );
});
```

This must run inside the `startup` event — command registration is only allowed before the world finishes loading.

## Running vanilla commands from script

```js
player.runCommand("give @s diamond 1");
// or, queued and error-safe across ticks:
system.run(() => player.runCommandAsync("give @s diamond 1"));
```

Prefer `runCommandAsync` for anything that might legally fail (e.g. `/tp` into an unloaded chunk) since it returns a promise instead of throwing synchronously.

## A practical pattern: custom item with a triggered ability

```js
import { world } from "@minecraft/server";

world.afterEvents.itemUse.subscribe((e) => {
  if (e.itemStack.typeId !== "myaddon:thunder_wand") return;
  const player = e.source;
  const loc = player.getViewDirection();
  player.dimension.createExplosion(
    { x: player.location.x + loc.x * 5, y: player.location.y, z: player.location.z + loc.z * 5 },
    2
  );
});
```

Next: [Forms & UI](bedrock-forms-ui.html).
