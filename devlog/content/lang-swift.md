# Swift

Apple's language for iOS/macOS (and beyond), modern, type-safe, with optionals baked into the type system to prevent null-reference bugs.

## Setup

Xcode (macOS) includes the full toolchain. For non-Apple platforms or command-line use:

```bash
swift --version
swift run          # inside a Swift package
```

## Core syntax

```swift
let name = "Ada"       // constant
var count = 0          // variable

func add(_ a: Int, _ b: Int) -> Int {
    return a + b
}

print("Hello, \(name)! Count: \(count)")

let nums = [1, 2, 3]
let doubled = nums.map { $0 * 2 }
```

`let` vs `var` mirrors Rust/Kotlin's philosophy: immutable by default, mutable only when explicitly declared.

## Optionals, Swift's answer to null

```swift
var maybeName: String? = nil // explicitly optional

if let name = maybeName {
    print("Hello, \(name)")
} else {
    print("No name set")
}

// or with a default
let displayName = maybeName ?? "Guest"

// force-unwrap (only when you're certain it's non-nil, crashes otherwise)
// let forced = maybeName!
```

The compiler forces you to handle the `nil` case before accessing an optional's value, this is Swift's core mechanism for eliminating null-pointer crashes at compile time.

## Structs vs classes

```swift
struct Point {   // value type, copied on assignment
    var x: Int
    var y: Int
}

class Animal {   // reference type, shared on assignment
    let name: String
    init(name: String) { self.name = name }
    func speak() -> String { "\(name) makes a sound." }
}
```

Swift favors `struct` for most data types (Apple's own frameworks default to structs), reach for `class` specifically when you need shared mutable reference semantics or inheritance.

## Protocols (Swift's interfaces)

```swift
protocol Shape {
    func area() -> Double
}

struct Circle: Shape {
    let radius: Double
    func area() -> Double { .pi * radius * radius }
}
```

## Error handling

```swift
enum ValidationError: Error {
    case tooShort
}

func validate(_ password: String) throws {
    if password.count < 8 {
        throw ValidationError.tooShort
    }
}

do {
    try validate("abc")
} catch {
    print("Invalid: \(error)")
}
```

## Popular use

| Purpose | Common choice |
|---|---|
| UI framework | SwiftUI (declarative, modern default), UIKit (older, still widely used) |
| Dependency management | Swift Package Manager |
| Backend (less common but growing) | Vapor |
| Testing | XCTest, Swift Testing |

## Common gotchas

- Force-unwrapping (`!`) an optional that's actually `nil` crashes at runtime, reserve it for cases you can prove are safe, and prefer `if let`/`guard let`/`??` everywhere else.
- `struct` copy semantics mean mutating a struct property inside a function parameter doesn't affect the caller's copy unless the parameter is explicitly `inout`.
- Retain cycles (two classes holding strong references to each other) leak memory under ARC (Automatic Reference Counting), closures capturing `self` commonly need `[weak self]` to avoid this.
