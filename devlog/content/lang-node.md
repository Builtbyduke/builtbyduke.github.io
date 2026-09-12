# Node.js

A JavaScript runtime (built on Chrome's V8 engine) for running JS outside the browser — servers, CLIs, build tools.

## Setup

Install via [nvm](https://github.com/nvm-sh/nvm) (Node Version Manager) rather than a system package, so you can switch versions per project:

```bash
nvm install --lts
nvm use --lts
node -v
npm -v
```

## Running a script

```bash
node index.js
```

## package.json & npm basics

```bash
npm init -y
npm install express
npm install -D nodemon   # dev-only dependency
```

```json
{
  "name": "my-app",
  "type": "module",
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon index.js"
  },
  "dependencies": { "express": "^4.19.0" }
}
```

`"type": "module"` switches the project to ES module syntax (`import`/`export`); omit it to stay on CommonJS (`require`/`module.exports`) — don't mix the two styles in one file.

## A minimal HTTP server (no framework)

```js
import { createServer } from "node:http";

const server = createServer((req, res) => {
  res.writeHead(200, { "Content-Type": "application/json" });
  res.end(JSON.stringify({ message: "hello" }));
});

server.listen(3000, () => console.log("Listening on :3000"));
```

## With Express (the common default)

```js
import express from "express";
const app = express();
app.use(express.json());

app.get("/users/:id", (req, res) => {
  res.json({ id: req.params.id, name: "Ada" });
});

app.post("/users", (req, res) => {
  const { name } = req.body;
  res.status(201).json({ id: Date.now(), name });
});

app.listen(3000, () => console.log("Listening on :3000"));
```

## File system & environment

```js
import { readFile } from "node:fs/promises";
const data = JSON.parse(await readFile("./config.json", "utf-8"));

const port = process.env.PORT ?? 3000;
```

Load `.env` files with the `dotenv` package (`npm i dotenv`, then `import "dotenv/config"` at the top of your entry file) rather than hardcoding secrets.

## Popular libraries

| Purpose | Common choice |
|---|---|
| Web framework | Express, Fastify, Hono, NestJS |
| ORM/DB | Prisma, Drizzle, Knex |
| Process manager (production) | PM2, or a systemd service |
| Testing | Vitest, Jest |

## Common gotchas

- Uncaught errors in async callbacks (not `await`ed, no `.catch()`) crash the process silently in some setups — always handle rejected promises.
- CPU-heavy synchronous work blocks the entire event loop (Node is single-threaded for JS execution) — offload it to `worker_threads` or a separate service.
- `npm install` without a lockfile committed leads to different dependency versions across machines — always commit `package-lock.json`.
