# PHP

A server-side scripting language built specifically for the web — still powers a huge share of it (WordPress alone accounts for a large fraction of all websites).

## Setup

```bash
php -v
php -S localhost:8000     # built-in dev server, no Apache/Nginx needed locally
```

Install Composer (the package manager) for anything beyond a single script:

```bash
curl -sS https://getcomposer.org/installer | php
php composer.phar init
```

## Core syntax

```php
<?php

$name = "Ada";
$count = 0;

function add(int $a, int $b): int {
    return $a + $b;
}

// arrays (both indexed and associative use the same type)
$nums = [1, 2, 3];
$user = ["name" => "Ada", "age" => 30];

echo "Hello, {$user['name']}!\n";

// classes
class Animal {
    public function __construct(private string $name) {}
    public function speak(): string {
        return "{$this->name} makes a sound.";
    }
}

$dog = new Animal("Rex");
echo $dog->speak();
```

## Control flow & match

```php
$grade = 85;

$letter = match (true) {
    $grade >= 90 => "A",
    $grade >= 80 => "B",
    $grade >= 70 => "C",
    default => "F",
};
```

`match` (PHP 8+) uses strict comparison and has no fallthrough, unlike `switch` — prefer it for value-mapping logic.

## Working with a database (PDO)

```php
$pdo = new PDO("mysql:host=localhost;dbname=app", "user", "pass");
$stmt = $pdo->prepare("SELECT * FROM users WHERE id = ?");
$stmt->execute([$id]);
$user = $stmt->fetch(PDO::FETCH_ASSOC);
```

Always use prepared statements (`?` placeholders) — string-concatenating user input into SQL is the classic PHP injection vector.

## Popular frameworks

| Purpose | Common choice |
|---|---|
| Full framework | Laravel (by far the most common modern choice), Symfony |
| CMS | WordPress |
| API-only | Slim, Laravel in API mode |
| Testing | PHPUnit, Pest |

## A tiny Laravel route (for context)

```php
Route::get('/users/{id}', function ($id) {
    return User::findOrFail($id);
});
```

Laravel's Eloquent ORM (`User::findOrFail($id)`) replaces most raw PDO code above in real applications.

## Common gotchas

- `==` performs type juggling (`"abc" == 0` was `true` before PHP 8, and some looser comparisons still surprise people) — prefer `===`.
- Array functions are inconsistent about parameter order (`in_array($needle, $haystack)` vs `array_map($callback, $array)`) — there's no shortcut but experience; keep the docs open.
- Superglobals (`$_GET`, `$_POST`, `$_SESSION`) are global mutable state — modern frameworks wrap them in request objects for a reason; avoid touching them directly outside small scripts.
