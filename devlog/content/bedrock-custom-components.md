# Custom Items & Blocks

Custom items and blocks are defined mostly in **JSON** (data-driven), with the Script API used to add behavior JSON alone can't express.

## Custom item (data-driven)

`items/thunder_wand.json` in your behavior pack:

```json
{
  "format_version": "1.21.0",
  "minecraft:item": {
    "description": { "identifier": "myaddon:thunder_wand", "menu_category": { "category": "equipment" } },
    "components": {
      "minecraft:max_stack_size": 1,
      "minecraft:icon": "thunder_wand",
      "minecraft:hand_equipped": true,
      "minecraft:durability": { "max_durability": 50 }
    }
  }
}
```

Then hook behavior via `world.afterEvents.itemUse` as shown in the [events page](bedrock-events-commands.html).

## Custom item components (script-registered, 1.20.60+)

For logic that needs to run *per tick* or *per stack* rather than per-use, register a **custom component**:

```js
import { system } from "@minecraft/server";

system.beforeEvents.startup.subscribe(({ itemComponentRegistry }) => {
  itemComponentRegistry.registerCustomComponent("myaddon:cooldown_glow", {
    onUse(event) {
      const { source, itemStack } = event;
      source.addEffect("glowing", 60);
    }
  });
});
```

Reference it from the item JSON:

```json
"components": {
  "minecraft:custom_components": ["myaddon:cooldown_glow"]
}
```

## Custom blocks

`blocks/reinforced_stone.json`:

```json
{
  "format_version": "1.21.0",
  "minecraft:block": {
    "description": {
      "identifier": "myaddon:reinforced_stone",
      "states": { "myaddon:charge": [0, 1, 2, 3] }
    },
    "components": {
      "minecraft:destructible_by_mining": { "seconds_to_destroy": 8 },
      "minecraft:destructible_by_explosion": { "explosion_resistance": 1000 },
      "minecraft:geometry": "geometry.reinforced_stone",
      "minecraft:material_instances": {
        "*": { "texture": "reinforced_stone", "render_method": "opaque" }
      }
    }
  }
}
```

**Block states** (`myaddon:charge` above) are the mechanism for "the same block but with variants", think redstone repeater delay settings. Read/write them from script:

```js
const block = player.dimension.getBlock(loc);
const state = block.permutation.getState("myaddon:charge");
block.setPermutation(block.permutation.withState("myaddon:charge", (state + 1) % 4));
```

## Custom block components

Same registration pattern as items, but for blocks, commonly used for `onPlayerInteract`, `onTick`, or `onPlace`:

```js
system.beforeEvents.startup.subscribe(({ blockComponentRegistry }) => {
  blockComponentRegistry.registerCustomComponent("myaddon:overcharge", {
    onTick(event) {
      const { block } = event;
      const charge = block.permutation.getState("myaddon:charge");
      if (charge >= 3) block.dimension.createExplosion(block.location, 3);
    },
    onPlayerInteract(event) {
      event.player.sendMessage("You touched the reinforced block.");
    }
  });
});
```

Blocks need a `"minecraft:tick"` component in JSON with an interval range for `onTick` to actually fire:

```json
"minecraft:tick": { "interval_range": [20, 20], "looping": true }
```

## Rule of thumb

- **Pure visuals/stats** (durability, stack size, textures, hardness) → JSON components, no script needed.
- **"Something should happen when X occurs"** → script event (`itemUse`, `blockPlace`) or a registered custom component if it needs per-tick or per-instance logic.
- **"This block/item needs several states that change over time"** → block states + `setPermutation`.

Next: [Saving Data (Dynamic Properties)](bedrock-persistent-storage.html).
