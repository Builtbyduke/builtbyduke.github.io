# Economy, Permissions & Commands, the systems everyone builds

A handful of systems show up in nearly every serious Bukkit/Paper server. Rather than reinventing them, the ecosystem converges on a few standard plugins with public APIs your plugin hooks into.

## Economy, Vault + an economy plugin

**Vault** is not an economy plugin itself, it's an abstraction layer. You code against Vault's `Economy` interface, and server owners install whichever real economy plugin they prefer (EssentialsX, CMI, etc.) underneath it.

```xml
<repository>
  <id>jitpack.io</id>
  <url>https://jitpack.io</url>
</repository>
```
```xml
<dependency>
  <groupId>com.github.MilkBowl</groupId>
  <artifactId>VaultAPI</artifactId>
  <version>1.7.3</version>
  <scope>provided</scope>
</dependency>
```

`plugin.yml`, declare the soft dependency:

```yaml
softdepend: [Vault]
```

Hooking in on enable:

```java
import net.milkbowl.vault.economy.Economy;
import org.bukkit.plugin.RegisteredServiceProvider;

private Economy econ;

private boolean setupEconomy() {
    RegisteredServiceProvider<Economy> rsp = getServer().getServicesManager().getRegistration(Economy.class);
    if (rsp == null) return false;
    econ = rsp.getProvider();
    return true;
}
```

Usage:

```java
econ.depositPlayer(player, 100.0);
econ.withdrawPlayer(player, 50.0);
double balance = econ.getBalance(player);
```

## Permissions, LuckPerms

Most servers run **LuckPerms**. You rarely need its full API just to *check* a permission, Bukkit's own permission check already respects whatever LuckPerms grants:

```java
if (player.hasPermission("myplugin.admin")) {
    // allowed
}
```

Declare defaults in `plugin.yml` so server owners see them:

```yaml
permissions:
  myplugin.admin:
    description: Full plugin access
    default: op
  myplugin.use:
    description: Basic command access
    default: true
```

For deeper integration (reading a player's LuckPerms groups/prefix directly), add the LuckPerms API as a `provided` dependency and fetch the `LuckPerms` service the same way as Vault's `Economy` above.

## Commands, Brigadier / modern command frameworks

Plain `CommandExecutor` (shown in [setup](java-plugin-setup.html)) is fine for one-off commands, but tab completion, subcommands, and argument validation get repetitive fast. Two common upgrades:

**Paper's Brigadier integration** (built in, no extra dependency) gives you typed arguments and real tab-completion:

```java
import io.papermc.paper.command.brigadier.Commands;
import io.papermc.paper.plugin.lifecycle.event.types.LifecycleEvents;

@Override
public void onEnable() {
    this.getLifecycleManager().registerEventHandler(LifecycleEvents.COMMANDS, event -> {
        event.registrar().register(
            Commands.literal("heal")
                .requires(src -> src.getSender().hasPermission("myplugin.heal"))
                .executes(ctx -> {
                    ctx.getSource().getSender().sendMessage("Healed!");
                    return 1;
                })
                .build()
        );
    });
}
```

**Third-party frameworks** like **[Cloud Command Framework](https://github.com/Incendo/cloud)** work across Bukkit, Paper, Velocity, and Discord (JDA) with one annotation-driven API, worth it once a plugin has more than a few commands with subcommands/permissions/arguments to manage.

## Config files, YAML

Bukkit's built-in config wraps Bukkit's YAML implementation; every plugin uses roughly this pattern:

```java
@Override
public void onEnable() {
    saveDefaultConfig(); // copies config.yml from resources/ if missing
    int cooldown = getConfig().getInt("kit-cooldown-seconds", 30);
}
```

`src/main/resources/config.yml`:

```yaml
kit-cooldown-seconds: 30
enabled-kits: [warrior, archer, miner]
```

## Data persistence, SQLite/MySQL via HikariCP

For anything beyond simple config values (player balances, stats, homes), most plugins reach for **HikariCP** (connection pooling) over either SQLite (single server) or MySQL (shared across a network via BungeeCord/Velocity):

```xml
<dependency>
  <groupId>com.zaxxer</groupId>
  <artifactId>HikariCP</artifactId>
  <version>5.1.0</version>
</dependency>
```

```java
HikariConfig config = new HikariConfig();
config.setJdbcUrl("jdbc:sqlite:" + getDataFolder() + "/data.db");
HikariDataSource dataSource = new HikariDataSource(config);
```

These four, Vault economy, permission checks, a real command framework, and pooled SQL storage, cover the large majority of "how do I add X system" questions in plugin development.
