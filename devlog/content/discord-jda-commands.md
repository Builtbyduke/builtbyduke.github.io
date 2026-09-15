# Slash Commands, Buttons & Embeds

These three, slash commands, buttons/menus, and embeds, make up the majority of what a modern Discord bot's UI actually is.

## Registering a slash command

Register commands once (globally, or instantly per-guild for testing, global commands can take up to an hour to propagate):

```java
jda.updateCommands().addCommands(
    Commands.slash("ping", "Replies with pong"),
    Commands.slash("kick", "Kick a member")
        .addOption(OptionType.USER, "target", "Who to kick", true)
        .addOption(OptionType.STRING, "reason", "Why", false)
        .setDefaultPermissions(DefaultMemberPermissions.enabledFor(Permission.KICK_MEMBERS))
).queue();
```

For instant per-guild testing instead:

```java
guild.updateCommands().addCommands(Commands.slash("ping", "Replies with pong")).queue();
```

## Handling the interaction

```java
import net.dv8tion.jda.api.events.interaction.command.SlashCommandInteractionEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;

public class CommandListener extends ListenerAdapter {
    @Override
    public void onSlashCommandInteraction(SlashCommandInteractionEvent event) {
        switch (event.getName()) {
            case "ping" -> event.reply("Pong!").queue();
            case "kick" -> handleKick(event);
        }
    }

    private void handleKick(SlashCommandInteractionEvent event) {
        var target = event.getOption("target").getAsMember();
        var reason = event.getOption("reason", "No reason", opt -> opt.getAsString());

        event.deferReply(true).queue(); // "thinking..." state, useful if the action takes time
        target.kick().reason(reason).queue(
            success -> event.getHook().sendMessage("Kicked " + target.getUser().getName()).queue(),
            failure -> event.getHook().sendMessage("Failed: " + failure.getMessage()).queue()
        );
    }
}
```

Interactions **must** get a response within 3 seconds or Discord shows "This interaction failed." `deferReply()` buys extra time for anything that hits a database or another API.

## Embeds

```java
import net.dv8tion.jda.api.EmbedBuilder;
import java.awt.Color;

EmbedBuilder embed = new EmbedBuilder()
    .setTitle("Server Stats")
    .setColor(Color.decode("#5865F2"))
    .addField("Members", String.valueOf(guild.getMemberCount()), true)
    .addField("Boosts", String.valueOf(guild.getBoostCount()), true)
    .setFooter("Updated just now")
    .setTimestamp(java.time.Instant.now());

event.replyEmbeds(embed.build()).queue();
```

## Buttons

```java
import net.dv8tion.jda.api.interactions.components.buttons.Button;

event.reply("Confirm the action?")
    .addActionRow(
        Button.success("confirm:yes", "Confirm"),
        Button.danger("confirm:no", "Cancel")
    )
    .queue();
```

Handling clicks, the **custom ID** you set is how you route the click back to logic (a common pattern: `action:payload`, split on `:`):

```java
@Override
public void onButtonInteraction(ButtonInteractionEvent event) {
    String[] parts = event.getComponentId().split(":");
    if (parts[0].equals("confirm")) {
        boolean confirmed = parts[1].equals("yes");
        event.editMessage(confirmed ? "Confirmed." : "Cancelled.").setComponents().queue();
    }
}
```

`.setComponents()` with no arguments removes the buttons after they're used, otherwise users can click "Confirm" repeatedly.

## Select menus (dropdowns)

```java
import net.dv8tion.jda.api.interactions.components.selections.StringSelectMenu;

event.reply("Pick a role:")
    .addActionRow(
        StringSelectMenu.create("role-select")
            .addOption("Member", "role_member")
            .addOption("VIP", "role_vip")
            .build()
    ).queue();
```

```java
@Override
public void onStringSelectInteraction(StringSelectInteractionEvent event) {
    String selected = event.getValues().get(0);
    // apply role based on selected value
}
```

## Modals (pop-up forms)

```java
import net.dv8tion.jda.api.interactions.components.text.TextInput;
import net.dv8tion.jda.api.interactions.components.text.TextInputStyle;
import net.dv8tion.jda.api.interactions.modals.Modal;

TextInput reason = TextInput.create("reason", "Reason", TextInputStyle.PARAGRAPH)
    .setPlaceholder("Why are you reporting this?")
    .setRequired(true)
    .build();

Modal modal = Modal.create("report-modal", "Submit a Report")
    .addActionRow(reason)
    .build();

event.replyModal(modal).queue();
```

Together, these four interaction types (slash commands, buttons, select menus, modals) are essentially the entire "UI toolkit" JDA exposes, almost every real bot feature is some combination of them.
