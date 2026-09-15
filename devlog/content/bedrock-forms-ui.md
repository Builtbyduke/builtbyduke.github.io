# Forms & UI (GUIs)

Bedrock scripting doesn't give you free-form custom screens like a resource-pack UI does, instead, `@minecraft/server-ui` gives you three **form types** that cover almost every menu you'll actually need. (If you've seen "FMBE" thrown around, it's not an official Mojang term, people usually mean this trio: **Action Form**, **Modal Form**, and **Message Form**, sometimes bundled with an event listener, which is what this page walks through.)

```bash
npm i @minecraft/server-ui
```

## ActionFormData, button menu

The one you'll use most: a title, a body, and a list of buttons (optionally with icons).

```js
import { ActionFormData } from "@minecraft/server-ui";

function showKitMenu(player) {
  const form = new ActionFormData()
    .title("Choose a Kit")
    .body("Pick your loadout for this round.")
    .button("Warrior", "textures/items/iron_sword")
    .button("Archer", "textures/items/bow")
    .button("Miner", "textures/items/diamond_pickaxe");

  form.show(player).then((response) => {
    if (response.canceled) return; // player hit Esc / closed it
    switch (response.selection) {
      case 0: giveKit(player, "warrior"); break;
      case 1: giveKit(player, "archer"); break;
      case 2: giveKit(player, "miner"); break;
    }
  });
}
```

## ModalFormData, inputs (sliders, toggles, dropdowns, text)

Use this for settings screens or anything that needs actual data back, not just a click.

```js
import { ModalFormData } from "@minecraft/server-ui";

const form = new ModalFormData()
  .title("Server Settings")
  .slider("PvP cooldown (sec)", 0, 30, 1, 5)
  .toggle("Enable friendly fire", false)
  .dropdown("Difficulty", ["Peaceful", "Easy", "Normal", "Hard"], 2)
  .textField("Welcome message", "Type here...", "Welcome!");

form.show(player).then((response) => {
  if (response.canceled) return;
  const [cooldown, friendlyFire, difficultyIndex, welcomeMsg] = response.formValues;
  saveSettings({ cooldown, friendlyFire, difficultyIndex, welcomeMsg });
});
```

The results always come back as a **positional array** matching the order fields were added, that trips people up more than anything else in this API.

## MessageFormData, confirm / two-button dialog

```js
import { MessageFormData } from "@minecraft/server-ui";

new MessageFormData()
  .title("Leave Game?")
  .body("Progress since your last save will be lost.")
  .button1("Cancel")
  .button2("Leave")
  .show(player)
  .then((r) => {
    if (!r.canceled && r.selection === 1) player.runCommand("kick @s Left the game");
  });
```

## Handling `canceled` correctly

A form counts as canceled if the player presses Escape, if their inventory closes for another reason (server hiccup, chunk unload), or on some platforms if two forms are shown too close together. **Always** check `response.canceled` before reading `.selection` / `.formValues`, reading them on a canceled response throws.

```js
form.show(player).then((response) => {
  if (response.canceled) {
    console.warn(`Form closed: ${response.cancelationReason}`);
    return;
  }
  // safe to use response.selection / response.formValues here
});
```

## Building a simple menu system (multi-screen)

Chain forms by calling the next `show()` from inside the previous `.then()`, this is how you build multi-step wizards (pick a kit → confirm → receive):

```js
function openMainMenu(player) {
  new ActionFormData()
    .title("Main Menu")
    .button("Kits")
    .button("Settings")
    .show(player)
    .then((res) => {
      if (res.canceled) return;
      if (res.selection === 0) showKitMenu(player);
      if (res.selection === 1) showSettingsMenu(player);
    });
}
```

## Beyond forms: actual on-screen HUD

For persistent HUD elements (not click-through menus), use `player.onScreenDisplay.setActionBar(text)` for a one-line action-bar message, or a resource-pack-driven custom UI (`ui/hud_screen.json`) if you need a real always-visible overlay, that lives in the resource pack, not the script API, and is a much bigger topic on its own.

Next: [Custom Items & Blocks](bedrock-custom-components.html).
