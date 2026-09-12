# TypeScript

JavaScript with a static type system layered on top, compiled (or transpiled) down to plain JS. Nearly the default choice for new JS projects of any size now.

## Setup

```bash
npm install -D typescript
npx tsc --init
```

Run directly during development without a manual compile step via `tsx` or `ts-node`:

```bash
npm install -D tsx
npx tsx src/index.ts
```

## Core syntax

```ts
// basic types
let age: number = 30;
let name: string = "Ada";
let active: boolean = true;
let tags: string[] = ["a", "b"];
let tuple: [string, number] = ["x", 1];

// interfaces vs type aliases
interface User {
  id: number;
  name: string;
  email?: string; // optional
}

type ID = string | number; // union type

// functions
function add(a: number, b: number): number {
  return a + b;
}

// generics
function firstOf<T>(items: T[]): T | undefined {
  return items[0];
}

// enums
enum Role { Admin, Editor, Viewer }
```

## Narrowing

```ts
function printLength(value: string | string[]) {
  if (Array.isArray(value)) {
    console.log(value.length); // TS knows it's an array here
  } else {
    console.log(value.length); // TS knows it's a string here
  }
}
```

## Utility types worth knowing

```ts
type PartialUser = Partial<User>;      // all fields optional
type UserName = Pick<User, "name">;    // subset of fields
type WithoutEmail = Omit<User, "email">;
type ReadonlyUser = Readonly<User>;
```

## tsconfig.json essentials

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  }
}
```

`strict: true` is the single highest-value setting — it turns on `strictNullChecks`, `noImplicitAny`, and friends together.

## Popular use

Almost everywhere plain [JavaScript](lang-javascript.html) is used today — [React](lang-react.html)/Next.js apps, [Node](lang-node.html) backends (Express, NestJS), and CLI tooling — increasingly defaults to TypeScript rather than JS.

## Common gotchas

- Types are erased at compile time — they don't exist at runtime, so you can't `typeof` a custom type or interface.
- `any` disables checking entirely for that value — prefer `unknown` when you genuinely don't know the type, and narrow it before use.
- A `.ts` file importing a `.js`-only library sometimes needs `@types/<package>` (`npm i -D @types/lodash`, for example) for type info.
