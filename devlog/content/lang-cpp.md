# C++

[C](lang-c.html) extended with classes, templates, and modern memory-safety tools (smart pointers, RAII) — used heavily in game engines, systems software, and performance-critical applications.

## Setup

```bash
g++ --version    # or clang++ --version
```

```bash
g++ main.cpp -o main -std=c++20 -Wall -Wextra
./main
```

## Core syntax

```cpp
#include <iostream>
#include <vector>
#include <string>

int add(int a, int b) { return a + b; }

int main() {
    std::string name = "Ada";
    int count = 0;

    std::cout << "Hello, " << name << "! Count: " << count << "\n";

    std::vector<int> nums = {1, 2, 3};
    for (int n : nums) {
        std::cout << n * 2 << "\n";
    }
    return 0;
}
```

## Classes

```cpp
class Animal {
public:
    Animal(std::string name) : name_(std::move(name)) {}
    std::string speak() const { return name_ + " makes a sound."; }

private:
    std::string name_;
};

Animal dog("Rex");
std::cout << dog.speak();
```

## RAII & smart pointers (the modern alternative to manual `new`/`delete`)

```cpp
#include <memory>

class Resource {
public:
    Resource() { std::cout << "Acquired\n"; }
    ~Resource() { std::cout << "Released\n"; } // runs automatically on scope exit
};

void useResource() {
    auto res = std::make_unique<Resource>(); // freed automatically, even on exception
} // "Released" prints here
```

`std::unique_ptr` and `std::shared_ptr` are the modern default over raw `new`/`delete` — the destructor runs deterministically when the smart pointer goes out of scope, eliminating most manual memory bugs.

## Templates (generic programming)

```cpp
template <typename T>
T maxOf(T a, T b) {
    return a > b ? a : b;
}

int main() {
    std::cout << maxOf(3, 7) << "\n";
    std::cout << maxOf(2.5, 1.1) << "\n";
}
```

## STL containers you'll reach for constantly

```cpp
#include <vector>
#include <map>
#include <string>

std::vector<int> nums;
std::map<std::string, int> ages = {{"Ada", 30}, {"Bob", 25}};

for (const auto& [name, age] : ages) {
    std::cout << name << ": " << age << "\n";
}
```

## Popular use / build tools

| Purpose | Common choice |
|---|---|
| Build system | CMake |
| Package manager | vcpkg, Conan |
| Game engines | Unreal Engine (uses C++ directly) |
| Testing | Google Test (gtest) |

## Common gotchas

- A raw pointer returned from a function that owns the data it points to (rather than a smart pointer or reference) is a classic dangling-pointer bug — prefer returning by value or a smart pointer.
- Passing large objects by value (instead of by `const&`) triggers unnecessary copies — pass by reference for anything beyond a primitive.
- Undefined behavior (out-of-bounds access, use-after-free) can "work" in testing and fail unpredictably elsewhere — this class of bug is exactly why smart pointers and container bounds-checked accessors (`.at()` instead of `[]`) exist.
