# Kotlin

A statically typed language that runs on the JVM (fully interoperable with [Java](lang-java.html)) — the default choice for modern Android development and increasingly popular for backend services too.

## Setup

```bash
kotlinc -version
```

Most projects use Gradle rather than calling `kotlinc` directly:

```bash
gradle init   # choose Kotlin application
gradle run
```

## Core syntax

```kotlin
fun add(a: Int, b: Int): Int = a + b

fun main() {
    val name = "Ada"   // immutable
    var count = 0      // mutable

    println("Hello, $name! Count: $count")

    val nums = listOf(1, 2, 3)
    val doubled = nums.map { it * 2 }
}
```

`val` (immutable reference) vs `var` (mutable) — same immutable-by-default philosophy as Swift and Rust.

## Null safety

```kotlin
var maybeName: String? = null // must explicitly opt into nullability

val length = maybeName?.length ?: 0   // safe call + Elvis operator for a default
```

Like Swift's optionals, the type system distinguishes `String` (never null) from `String?` (may be null) — the compiler refuses to let a nullable value be used where a non-null one is required without a check first.

## Classes and data classes

```kotlin
class Animal(val name: String) {
    fun speak() = "$name makes a sound."
}

// data class — auto-generates equals/hashCode/toString/copy
data class Point(val x: Int, val y: Int)

val p1 = Point(1, 2)
val p2 = p1.copy(y = 5)
```

## When expressions (Kotlin's switch, but an expression)

```kotlin
fun describe(x: Any): String = when (x) {
    is Int -> "an integer: $x"
    is String -> "a string of length ${x.length}"
    else -> "something else"
}
```

## Coroutines (structured concurrency)

```kotlin
import kotlinx.coroutines.*

suspend fun fetchUser(id: Int): String {
    delay(100) // non-blocking "sleep"
    return "User $id"
}

fun main() = runBlocking {
    val user = fetchUser(1)
    println(user)
}
```

`suspend` functions are Kotlin's alternative to callback-heavy or thread-heavy async code — they read like synchronous code but don't block the underlying thread.

## Popular use

| Purpose | Common choice |
|---|---|
| Android development | Jetpack Compose (UI), the modern default over XML layouts |
| Backend | Ktor, Spring Boot (fully supports Kotlin) |
| Build tool | Gradle (Kotlin DSL, `build.gradle.kts`) |
| Minecraft plugins | Also usable via the same Maven/Gradle + Paper API setup as [Java plugins](java-plugin-setup.html) |

## Common gotchas

- `==` in Kotlin checks *structural* equality by default (calls `.equals()`), unlike Java where `==` on objects checks reference identity — use `===` in Kotlin specifically for reference comparison.
- Extension functions (adding methods to existing classes, e.g. `fun String.shout() = uppercase() + "!"`) are resolved statically at compile time based on the declared type, not the runtime type — this can surprise people expecting virtual-style dispatch.
- Platform types from Java interop (no nullability info from Java's type system) can slip past Kotlin's null checks — annotate Java APIs with `@Nullable`/`@NonNull` where you control them.
