# Building with Maven & Uploading to a Server

## Building the jar

From the project root (where `pom.xml` lives):

```bash
mvn clean package
```

- `clean` wipes `target/` so you're not shipping stale classes.
- `package` compiles, runs tests, and produces the jar in `target/`.

With the `maven-shade-plugin` configured (see [setup page](java-plugin-setup.html)), you'll get `target/my-plugin.jar`, this is the file the server loads. Without shading you'd get a jar missing any third-party dependencies you added (besides the provided API), which fail silently at runtime with `NoClassDefFoundError`.

Useful variants:

```bash
mvn clean package -DskipTests     # skip test phase for a quick rebuild
mvn -q clean package              # quiet output, only show errors
```

## Where the jar goes

Every Bukkit/Spigot/Paper server has a `plugins/` folder next to its own jar and `server.properties`:

```
server/
  paper-1.21.jar
  server.properties
  plugins/
    my-plugin.jar   <- goes here
```

## Uploading to a remote server

**Option 1, SFTP/SCP (most common for a VPS):**

```bash
scp target/my-plugin.jar user@your-server-ip:/path/to/server/plugins/
```

Or with an SFTP GUI client (FileZilla, WinSCP): connect with the same host/user/port your SSH access uses, navigate to `plugins/`, and drag the jar in.

**Option 2, Managed host control panel** (common on Pterodactyl-based hosts like most budget Minecraft hosts): use the panel's file manager, open `plugins/`, and use its upload button. Some panels also support SFTP directly into the same path.

**Option 3, rsync**, handy if you're iterating quickly and want to skip re-uploading unchanged files:

```bash
rsync -avz target/my-plugin.jar user@your-server-ip:/path/to/server/plugins/
```

## Reloading without a full restart

Full restarts are safer, but for quick iteration:

```
/plugins          # confirm it's loaded
/reload confirm   # Paper requires this confirmation, many devs still avoid /reload
                   # in production since it can leave old listeners registered
```

Most experienced plugin devs prefer a full `stop` + restart, or a plugin manager like **PlugMan**, over vanilla `/reload`, because `/reload` doesn't reliably tear down everything the old plugin instance registered.

## A quick scripted deploy loop (local test server)

If you run a local test server for development, a small script saves a lot of manual copying:

```bash
#!/usr/bin/env bash
set -e
mvn -q clean package
cp target/my-plugin.jar ~/mc-test-server/plugins/
echo "Deployed. Restart or /reload confirm on the test server."
```

Save as `deploy.sh`, `chmod +x deploy.sh`, then `./deploy.sh` after every change.

## Common build errors

| Error | Cause |
|---|---|
| `package org.bukkit does not exist` | Missing/misconfigured `paper-api` dependency or repository in `pom.xml` |
| Plugin loads but `NoClassDefFoundError` at runtime | Forgot the shade plugin, or a dependency was marked `provided` when it shouldn't be |
| `Unsupported class file major version` | Server's Java runtime is older than the version you compiled with, match `maven.compiler.target` to the server's actual JDK |
| Plugin doesn't appear in `/plugins` | `main:` in `plugin.yml` doesn't match your actual package/class path exactly |

Next: [Decompiling a .jar to .java](java-decompile-jar.html).
