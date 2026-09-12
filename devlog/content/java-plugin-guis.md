# Inventory GUI Menus

The classic "custom GUI" in a Bukkit/Paper plugin is a chest inventory you open, fill with `ItemStack`s as buttons, and intercept clicks on. There's no special "GUI API" in vanilla Bukkit — it's the inventory system, repurposed.

## Creating and opening a menu

```java
import org.bukkit.Bukkit;
import org.bukkit.Material;
import org.bukkit.entity.Player;
import org.bukkit.inventory.Inventory;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.meta.ItemMeta;

public class KitMenu {
    public static Inventory create() {
        Inventory inv = Bukkit.createInventory(null, 27, "§8Choose a Kit");

        inv.setItem(11, namedItem(Material.IRON_SWORD, "§aWarrior"));
        inv.setItem(13, namedItem(Material.BOW, "§eArcher"));
        inv.setItem(15, namedItem(Material.DIAMOND_PICKAXE, "§bMiner"));

        return inv;
    }

    private static ItemStack namedItem(Material mat, String name) {
        ItemStack item = new ItemStack(mat);
        ItemMeta meta = item.getItemMeta();
        meta.setDisplayName(name);
        item.setItemMeta(meta);
        return item;
    }

    public static void open(Player player) {
        player.openInventory(create());
    }
}
```

## Handling clicks

**Always cancel the click event** for a GUI, or players can pull items straight out of your menu:

```java
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.inventory.InventoryClickEvent;
import org.bukkit.entity.Player;

public class KitMenuListener implements Listener {
    @EventHandler
    public void onClick(InventoryClickEvent event) {
        if (!"§8Choose a Kit".equals(event.getView().getTitle())) return;
        event.setCancelled(true);

        if (event.getClickedInventory() == null) return;
        Player player = (Player) event.getWhoClicked();

        switch (event.getSlot()) {
            case 11 -> giveKit(player, "warrior");
            case 13 -> giveKit(player, "archer");
            case 15 -> giveKit(player, "miner");
            default -> { return; }
        }
        player.closeInventory();
    }
}
```

Matching on the **title string** is the simplest approach but gets fragile with many menus. Once you have more than two or three screens, switch to a registry pattern (below).

## A reusable menu framework

Most projects converge on the same shape: a `Menu` interface with `getInventory()` and `onClick(slot, player)`, tracked in a map keyed by the open `Inventory` instance so the listener can dispatch generically instead of string-matching titles:

```java
public interface Menu {
    Inventory getInventory();
    void onClick(int slot, Player player);
}

public class MenuManager implements Listener {
    private final Map<Inventory, Menu> openMenus = new HashMap<>();

    public void open(Player player, Menu menu) {
        openMenus.put(menu.getInventory(), menu);
        player.openInventory(menu.getInventory());
    }

    @EventHandler
    public void onClick(InventoryClickEvent event) {
        Menu menu = openMenus.get(event.getInventory());
        if (menu == null) return;
        event.setCancelled(true);
        menu.onClick(event.getSlot(), (Player) event.getWhoClicked());
    }

    @EventHandler
    public void onClose(InventoryCloseEvent event) {
        openMenus.remove(event.getInventory());
    }
}
```

Each concrete menu (e.g. `KitMenu`) implements `Menu` and builds its own `ItemStack`s — no more title-string matching, and menus can hold their own state (pagination index, selected filters, etc.) as instance fields.

## Popular libraries that do this for you

Writing this by hand is a great learning exercise, but for real projects most devs pull in a small menu library rather than reinventing pagination/animation:

- **[Triumph GUI](https://github.com/TriumphTeam/triumph-gui)** — fluent Kotlin/Java API, very popular for new projects.
- **[IF (Inventory Framework)](https://github.com/DevNatan/inventory-framework)** — component-based, supports nested/paginated views.

Add via Maven (shaded, since these aren't on the server already):

```xml
<dependency>
  <groupId>dev.triumphteam</groupId>
  <artifactId>triumph-gui</artifactId>
  <version>3.1.10</version>
</dependency>
```

Next: [Economy, Permissions & Commands](java-plugin-common-systems.html).
