# Java

A statically typed, object-oriented language that compiles to bytecode run on the JVM, the same language and runtime behind [Minecraft Java plugins](java-plugin-setup.html) and [JDA Discord bots](discord-jda-setup.html).

## Setup

```bash
java -version
javac -version
```

Real projects use a build tool rather than calling `javac` by hand, [Maven](java-plugin-setup.html) or Gradle.

## Core syntax

```java
public class Main {
    public static void main(String[] args) {
        String name = "Ada";
        int count = 0;

        System.out.println("Hello, " + name + "!");

        var nums = List.of(1, 2, 3);
        var doubled = nums.stream().map(n -> n * 2).toList();
    }
}
```

## Classes, records, and interfaces

```java
public class Animal {
    private final String name;

    public Animal(String name) { this.name = name; }

    public String speak() { return name + " makes a sound."; }
}

// records (Java 16+), immutable data carriers, no boilerplate getters/equals/hashCode
public record Point(int x, int y) {}

// interfaces
public interface Shape {
    double area();
}

public class Circle implements Shape {
    private final double radius;
    public Circle(double radius) { this.radius = radius; }
    @Override public double area() { return Math.PI * radius * radius; }
}
```

## Streams (functional-style collection processing)

```java
List<String> names = List.of("Ada", "Bob", "Cy");

List<String> upper = names.stream()
    .filter(n -> n.length() > 2)
    .map(String::toUpperCase)
    .sorted()
    .toList();
```

## Pattern matching (modern Java)

```java
Object value = 42;

String description = switch (value) {
    case Integer i when i > 100 -> "big int";
    case Integer i -> "int: " + i;
    case String s -> "string: " + s;
    default -> "unknown";
};
```

## Exceptions

```java
try {
    int result = Integer.parseInt(input);
} catch (NumberFormatException e) {
    System.err.println("Invalid number: " + e.getMessage());
} finally {
    cleanup();
}
```

Checked exceptions (`throws IOException` in a method signature) must be declared or caught, a distinctly Java design choice most other languages here don't share.

## Popular frameworks

| Purpose | Common choice |
|---|---|
| Web/backend | Spring Boot |
| Build tool | Maven, Gradle |
| Testing | JUnit 5, Mockito |
| Minecraft servers | Paper/Spigot API, see [plugin setup](java-plugin-setup.html) |
| Discord bots | JDA, see [JDA setup](discord-jda-setup.html) |

## Common gotchas

- `==` compares object references, not content, use `.equals()` for strings/objects (`"a".equals(str)` avoids a NullPointerException if `str` is null).
- Autoboxing: `Integer` caches small values (-128 to 127), so `==` on boxed integers *appears* to work for small numbers and silently breaks outside that range, another reason to default to `.equals()`.
- A missing `@Override` typo (wrong method signature) silently creates a new overload instead of overriding, always annotate overrides so the compiler catches the mismatch.
