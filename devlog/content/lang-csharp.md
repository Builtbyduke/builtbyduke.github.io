# C#

A statically typed, object-oriented language from Microsoft, running on .NET — used for web backends, desktop apps, and game development (Unity).

## Setup

```bash
dotnet --version
dotnet new console -o my-app
cd my-app
dotnet run
```

## Core syntax

```csharp
var name = "Ada";
int count = 0;

int Add(int a, int b) => a + b;

var nums = new List<int> { 1, 2, 3 };
var doubled = nums.Select(n => n * 2).ToList();

var user = new { Name = "Ada", Age = 30 }; // anonymous type
Console.WriteLine($"{user.Name} is {user.Age}");
```

## Classes and records

```csharp
public class Animal
{
    public string Name { get; }
    public Animal(string name) => Name = name;
    public string Speak() => $"{Name} makes a sound.";
}

// records — immutable data with value equality built in
public record Point(int X, int Y);

var p1 = new Point(1, 2);
var p2 = new Point(1, 2);
Console.WriteLine(p1 == p2); // true — value equality, unlike a class
```

## Nullable reference types

```csharp
#nullable enable

string? maybeNull = GetName(); // explicitly nullable
string definitelyNotNull = maybeNull ?? "default";
```

With `#nullable enable` (standard in modern projects), the compiler warns if you dereference a possibly-null reference without checking — catches a large class of null-reference bugs at compile time.

## LINQ (query-style collection processing)

```csharp
var adults = people
    .Where(p => p.Age >= 18)
    .OrderBy(p => p.Name)
    .Select(p => p.Name)
    .ToList();

// or query syntax
var adults2 = from p in people
              where p.Age >= 18
              orderby p.Name
              select p.Name;
```

## Async/await

```csharp
public async Task<User> GetUserAsync(int id)
{
    var response = await httpClient.GetAsync($"/api/users/{id}");
    response.EnsureSuccessStatusCode();
    return await response.Content.ReadFromJsonAsync<User>();
}
```

## Popular frameworks

| Purpose | Common choice |
|---|---|
| Web/API | ASP.NET Core |
| Game development | Unity |
| Desktop | WPF, MAUI, WinForms (legacy) |
| ORM | Entity Framework Core |
| Testing | xUnit, NUnit |

## A minimal ASP.NET Core endpoint

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/users/{id}", (int id) => new { Id = id, Name = "Ada" });

app.Run();
```

## Common gotchas

- `struct` (value type, copied) vs `class` (reference type) — passing a large struct around by value can be a surprising performance cost if you expected reference semantics.
- `string` comparison with `==` works correctly (operator overloaded for value comparison), unlike Java — but reference comparisons for other types still need `.Equals()` or `record` types for value semantics.
- Forgetting `await` on a `Task` doesn't error — it just fires the async operation without waiting, a common source of race conditions ("fire and forget" bugs).
