# JavaScript

The language of the web browser, and — via Node — of a huge share of backend and tooling code too.

## Setup

Runs natively in every browser. For local scripting/tooling, install [Node.js](lang-node.html) (`node -v` to confirm), which also gives you `npm`.

## Core syntax

```js
// variables — prefer const, use let when reassigned, avoid var
const name = "Ada";
let count = 0;

// functions
function add(a, b) { return a + b; }
const multiply = (a, b) => a * b;

// template literals
console.log(`${name} counted to ${count}`);

// arrays & objects
const nums = [1, 2, 3];
const doubled = nums.map(n => n * 2);
const user = { name: "Ada", age: 30 };
const { name: n2, age } = user; // destructuring

// async/await
async function fetchUser(id) {
  const res = await fetch(`/api/users/${id}`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

// classes
class Animal {
  constructor(name) { this.name = name; }
  speak() { return `${this.name} makes a sound.`; }
}
```

## Equality: always `===`

`==` coerces types in surprising ways (`"" == 0` is `true`). Use `===`/`!==` unless you have a specific, commented reason not to.

## Modules

```js
// math.js
export function add(a, b) { return a + b; }
export default class Calculator {}

// main.js
import Calculator, { add } from "./math.js";
```

## The event loop, briefly

JS is single-threaded with a task queue: synchronous code runs first, then microtasks (resolved Promises), then macrotasks (`setTimeout`, I/O callbacks). This is why a resolved Promise's `.then()` runs before a `setTimeout(fn, 0)`.

## Popular libraries/frameworks

| Purpose | Common choice |
|---|---|
| UI framework | [React](lang-react.html), Vue, Svelte |
| Bundler | Vite, esbuild, webpack |
| Testing | Vitest, Jest, Playwright |
| HTTP server | Express, Fastify, Hono |
| Date handling | date-fns, Luxon (avoid Moment.js — in maintenance mode) |

## Common gotchas

- `this` inside a regular function depends on how it's *called*, not where it's defined — arrow functions capture the surrounding `this` instead, which is why they're preferred for callbacks inside class methods.
- Array/object equality is by reference: `[1,2] === [1,2]` is `false`.
- Floating point: `0.1 + 0.2 !== 0.3` — use a small epsilon or a decimal library for money.

See also: [TypeScript](lang-typescript.html) for the typed superset most new projects now use by default.
