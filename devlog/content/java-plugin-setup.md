# Maven Project Setup (Spigot / Paper Plugins)

Java Minecraft server plugins target the Bukkit API, implemented by **Spigot** and its modern fork **Paper** (almost every new project should target Paper, it's a drop-in superset with better performance and a richer API).

## Prerequisites

- JDK 21 (Paper 1.20.5+ requires it; check your target Minecraft version's required Java version before picking one).
- Maven (`mvn -v` to confirm it's installed) or Gradle, this guide uses Maven since it's still the more common default in tutorials.

## Project layout

```
my-plugin/
  pom.xml
  src/
    main/
      java/com/example/myplugin/MyPlugin.java
      resources/
        plugin.yml
```

## pom.xml

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.example</groupId>
  <artifactId>my-plugin</artifactId>
  <version>1.0.0</version>
  <packaging>jar</packaging>

  <properties>
    <maven.compiler.source>21</maven.compiler.source>
    <maven.compiler.target>21</maven.compiler.target>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
  </properties>

  <repositories>
    <repository>
      <id>papermc</id>
      <url>https://repo.papermc.io/repository/maven-public/</url>
    </repository>
  </repositories>

  <dependencies>
    <dependency>
      <groupId>io.papermc.paper</groupId>
      <artifactId>paper-api</artifactId>
      <version>1.21-R0.1-SNAPSHOT</version>
      <scope>provided</scope>
    </dependency>
  </dependencies>

  <build>
    <finalName>${project.artifactId}</finalName>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-shade-plugin</artifactId>
        <version>3.5.3</version>
        <executions>
          <execution>
            <phase>package</phase>
            <goals><goal>shade</goal></goals>
          </execution>
        </executions>
      </plugin>
    </plugins>
  </build>
</project>
```

`scope=provided` matters: the server already has the API classes at runtime, so you don't want to bundle them into your jar.

## plugin.yml

```yaml
name: MyPlugin
version: '1.0.0'
main: com.example.myplugin.MyPlugin
api-version: '1.21'
author: you
commands:
  hello:
    description: Says hello
```

## Main class

```java
package com.example.myplugin;

import org.bukkit.plugin.java.JavaPlugin;

public class MyPlugin extends JavaPlugin {
    @Override
    public void onEnable() {
        getLogger().info("MyPlugin enabled!");
    }

    @Override
    public void onDisable() {
        getLogger().info("MyPlugin disabled.");
    }
}
```

## A first command handler

```java
package com.example.myplugin;

import org.bukkit.command.Command;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;

public class HelloCommand {
    public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
        if (!(sender instanceof Player player)) {
            sender.sendMessage("Players only.");
            return true;
        }
        player.sendMessage("§aHello, " + player.getName() + "!");
        return true;
    }
}
```

Wire it up in `onEnable()`:

```java
getCommand("hello").setExecutor(new HelloCommand()::onCommand);
```

## Registering an event listener

```java
package com.example.myplugin;

import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.player.PlayerJoinEvent;

public class JoinListener implements Listener {
    @EventHandler
    public void onJoin(PlayerJoinEvent event) {
        event.setJoinMessage("§7» " + event.getPlayer().getName() + " joined");
    }
}
```

```java
getServer().getPluginManager().registerEvents(new JoinListener(), this);
```

Next: [Building & Uploading to a Server](java-plugin-build-deploy.html).
