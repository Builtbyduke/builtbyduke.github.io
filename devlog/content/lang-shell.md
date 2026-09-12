# Shell / Bash

The scripting language of the terminal — automates the commands you'd otherwise type by hand. `bash` is the most common shell on Linux and (via WSL/Git Bash) widely used on Windows too; macOS ships `zsh` by default but is largely bash-compatible for scripting purposes.

## Running a script

```bash
#!/usr/bin/env bash
set -euo pipefail   # exit on error, undefined var, or failed pipe — put this in almost every script

echo "Hello, world"
```

```bash
chmod +x script.sh
./script.sh
```

`set -euo pipefail` is close to a universal best practice: without it, a script silently continues past a failed command, which is rarely what you want.

## Variables

```bash
name="Ada"
count=0

echo "Hello, $name! Count: $count"
echo "Hello, ${name}!"   # braces avoid ambiguity when concatenating

# command substitution
current_dir=$(pwd)
files=$(ls | wc -l)
```

No spaces around `=` in assignment — `name = "Ada"` is a syntax error (Bash parses it as running a command called `name` with arguments).

## Conditionals

```bash
if [ -f "config.yml" ]; then
    echo "Config found"
elif [ -d "config" ]; then
    echo "Config directory found"
else
    echo "No config"
fi

# [[ ]] is the more modern, more forgiving test syntax
if [[ "$name" == "Ada" && -n "$count" ]]; then
    echo "Match"
fi
```

## Loops

```bash
for file in *.txt; do
    echo "Processing $file"
done

for i in {1..5}; do
    echo "Iteration $i"
done

while read -r line; do
    echo "Line: $line"
done < input.txt
```

## Functions

```bash
greet() {
    local name="$1"   # local scopes the variable to the function
    echo "Hello, $name!"
}

greet "Ada"
```

## Pipes and redirection

```bash
cat access.log | grep "ERROR" | wc -l     # pipe output between commands
echo "log line" >> output.log             # append
echo "log line" > output.log              # overwrite
command 2> errors.log                     # redirect stderr only
command > all.log 2>&1                    # redirect both stdout and stderr
```

## Argument handling

```bash
#!/usr/bin/env bash
echo "Script name: $0"
echo "First arg: $1"
echo "All args: $@"
echo "Arg count: $#"
```

## Common gotchas

- Unquoted variables (`$name` instead of `"$name"`) break on spaces/glob characters in the value — quote variables almost everywhere, including in `[ ]` tests.
- `rm -rf $dir` with an empty or unset `$dir` can expand to `rm -rf /` in the worst case — always quote, and consider `set -u` to fail loudly on unset variables instead.
- Exit codes matter for scripting logic (`0` = success, non-zero = failure) — check `$?` or use `if command; then` directly rather than parsing command output to detect failure.
