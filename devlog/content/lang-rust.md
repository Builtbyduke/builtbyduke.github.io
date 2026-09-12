# Rust

A compiled systems language that guarantees memory safety without a garbage collector, enforced at compile time by the **borrow checker** — a common choice when you want C++-level performance with far fewer memory bugs.

## Setup

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
cargo --version
```

## Project setup with Cargo

```bash
cargo new my-app
cd my-app
cargo run
cargo build --release
```

## Core syntax

```rust
fn add(a: i32, b: i32) -> i32 {
    a + b // no semicolon = this is the return value
}

fn main() {
    let name = "Ada";
    let mut count = 0; // immutable by default — mut required to reassign
    count += 1;

    println!("Hello, {name}! Count: {count}");

    let nums = vec![1, 2, 3];
    let doubled: Vec<i32> = nums.iter().map(|n| n * 2).collect();
}
```

## Ownership — the core concept

```rust
fn main() {
    let s1 = String::from("hello");
    let s2 = s1; // s1 is MOVED into s2 — s1 is no longer valid

    // println!("{s1}"); // compile error: value borrowed after move
    println!("{s2}"); // fine

    let s3 = String::from("world");
    print_it(&s3); // borrow, not move — s3 still usable after
    println!("{s3}");
}

fn print_it(s: &String) {
    println!("{s}");
}
```

Every value has exactly one owner; when the owner goes out of scope, the value is freed automatically (like C++ RAII, but enforced by the compiler rather than convention) — this is what eliminates use-after-free and double-free bugs at compile time.

## Structs, enums, and pattern matching

```rust
struct Animal { name: String }

impl Animal {
    fn speak(&self) -> String {
        format!("{} makes a sound.", self.name)
    }
}

enum Shape {
    Circle(f64),
    Rectangle(f64, f64),
}

fn area(shape: &Shape) -> f64 {
    match shape {
        Shape::Circle(r) => std::f64::consts::PI * r * r,
        Shape::Rectangle(w, h) => w * h,
    }
}
```

## Error handling — `Result`, no exceptions

```rust
fn divide(a: f64, b: f64) -> Result<f64, String> {
    if b == 0.0 {
        return Err("division by zero".to_string());
    }
    Ok(a / b)
}

fn main() {
    match divide(10.0, 0.0) {
        Ok(result) => println!("{result}"),
        Err(e) => println!("Error: {e}"),
    }

    // or propagate with ? inside a function that also returns Result
}
```

## Popular crates (libraries)

| Purpose | Common choice |
|---|---|
| Async runtime | Tokio |
| Web framework | Axum, Actix Web |
| Serialization | serde |
| CLI parsing | clap |
| Error handling helpers | anyhow, thiserror |

Add with `cargo add <crate>` (e.g. `cargo add tokio --features full`).

## Common gotchas

- The borrow checker rejects code that would be memory-unsafe even if it "would have worked" at runtime — the fix is almost always to restructure ownership (clone, use a reference, or restructure lifetimes), not to fight the compiler.
- `unwrap()` panics immediately on an `Err`/`None` — fine for prototypes and tests, but production code should handle the `Result`/`Option` explicitly or use `?` to propagate it.
- Integer overflow panics in debug builds but silently wraps in release builds by default — use checked/wrapping arithmetic methods explicitly if you need consistent behavior across both.
