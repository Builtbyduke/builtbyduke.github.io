# Go

A compiled, statically typed language from Google designed for simplicity and easy concurrency, a common choice for backend services, CLIs, and infrastructure tooling.

## Setup

```bash
go version
mkdir my-app && cd my-app
go mod init example.com/my-app
```

## Core syntax

```go
package main

import "fmt"

func add(a, b int) int {
    return a + b
}

func main() {
    name := "Ada"
    count := 0

    fmt.Printf("Hello, %s! Count: %d\n", name, count)

    nums := []int{1, 2, 3}
    for _, n := range nums {
        fmt.Println(n * 2)
    }
}
```

```bash
go run main.go
go build -o my-app     # compiles a single static binary
```

## Structs and methods

```go
type Animal struct {
    Name string
}

func (a Animal) Speak() string {
    return a.Name + " makes a sound."
}

dog := Animal{Name: "Rex"}
fmt.Println(dog.Speak())
```

Go has no classes/inheritance, behavior is attached to types via methods, and interfaces are satisfied implicitly (no `implements` keyword needed).

## Error handling, explicit, not exceptions

```go
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, fmt.Errorf("division by zero")
    }
    return a / b, nil
}

result, err := divide(10, 0)
if err != nil {
    fmt.Println("Error:", err)
    return
}
```

Every fallible function returns an `error` as its last value, checked explicitly with `if err != nil`, there's no try/catch in idiomatic Go.

## Goroutines & channels (concurrency)

```go
func worker(id int, jobs <-chan int, results chan<- int) {
    for j := range jobs {
        results <- j * 2
    }
}

func main() {
    jobs := make(chan int, 5)
    results := make(chan int, 5)

    for w := 1; w <= 3; w++ {
        go worker(w, jobs, results)
    }

    for j := 1; j <= 5; j++ { jobs <- j }
    close(jobs)

    for a := 1; a <= 5; a++ { fmt.Println(<-results) }
}
```

`go someFunc()` spawns a lightweight goroutine (not an OS thread); channels are the idiomatic way to communicate between them instead of shared-memory locking.

## Popular libraries

| Purpose | Common choice |
|---|---|
| Web framework | net/http (standard library is often enough), Gin, Echo |
| ORM | GORM, or sqlc for typed raw SQL |
| CLI | Cobra |
| Testing | built-in `testing` package |

## Common gotchas

- Unused imports and unused local variables are **compile errors**, not warnings, Go is strict about this by design.
- A `nil` slice and an empty slice (`[]int{}`) behave almost identically but aren't `==` comparable the way you might expect coming from other languages.
- Struct fields and functions starting with a lowercase letter are unexported (package-private); capitalize them to make them public, there's no separate `public`/`private` keyword.
