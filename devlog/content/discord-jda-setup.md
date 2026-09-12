# JDA Project Setup (Java Discord Bots)

**[JDA](https://github.com/discord-jda/JDA)** (Java Discord API) is the standard wrapper for building Discord bots in Java — same Maven-based workflow as a Minecraft plugin, just a different API surface.

## Create the bot application

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications) → **New Application**.
2. **Bot** tab → **Reset Token** (copy it somewhere safe — you can't view it again, only regenerate).
3. Under **Privileged Gateway Intents**, enable `MESSAGE CONTENT INTENT` if your bot reads message text (not needed for slash commands alone).
4. **OAuth2 → URL Generator**: check `bot` and `applications.commands`, pick permissions, use the generated URL to invite it to a test server.

Never commit your token to a public repo — load it from an environment variable or a git-ignored config file.

## Maven setup

```xml
<dependency>
  <groupId>net.dv8tion</groupId>
  <artifactId>JDA</artifactId>
  <version>5.0.2</version>
</dependency>
```

Use the shade plugin exactly as in the [Minecraft plugin setup](java-plugin-setup.html) — JDA isn't preinstalled anywhere, so unlike a Bukkit plugin, it needs to be bundled into your jar (don't mark it `provided`).

## Minimal bot

```java
import net.dv8tion.jda.api.JDABuilder;
import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.requests.GatewayIntent;

public class Bot {
    public static void main(String[] args) throws InterruptedException {
        String token = System.getenv("DISCORD_TOKEN");

        JDA jda = JDABuilder.createDefault(token)
            .enableIntents(GatewayIntent.MESSAGE_CONTENT)
            .addEventListeners(new MessageListener())
            .build();

        jda.awaitReady();
        System.out.println("Bot is online as " + jda.getSelfUser().getName());
    }
}
```

## A basic listener

```java
import net.dv8tion.jda.api.events.message.MessageReceivedEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;

public class MessageListener extends ListenerAdapter {
    @Override
    public void onMessageReceived(MessageReceivedEvent event) {
        if (event.getAuthor().isBot()) return;
        if (event.getMessage().getContentRaw().equalsIgnoreCase("!ping")) {
            event.getChannel().sendMessage("Pong!").queue();
        }
    }
}
```

`.queue()` matters — JDA's REST calls are async; calling `.complete()` blocks the gateway thread and will eventually cause rate-limit and latency problems at any real scale.

## Running it 24/7

A local JVM dies when your machine sleeps or reboots. For anything beyond testing:

- **A small VPS** (Java installed) running the jar under `systemd` or inside `screen`/`tmux` so it survives SSH disconnects.
- **`systemd` service** example (`/etc/systemd/system/mybot.service`):

```ini
[Unit]
Description=My Discord Bot
After=network.target

[Service]
ExecStart=/usr/bin/java -jar /opt/mybot/mybot.jar
Restart=on-failure
Environment=DISCORD_TOKEN=your_token_here
User=botuser

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable --now mybot
sudo systemctl status mybot
journalctl -u mybot -f   # live logs
```

Next: [Slash Commands, Buttons & Embeds](discord-jda-commands.html).
