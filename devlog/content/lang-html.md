# HTML

The markup language that defines structure and content for every web page — pairs with [CSS](lang-css.html) for appearance and [JavaScript](lang-javascript.html) for behavior.

## Minimal document

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Page Title</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <h1>Hello, world</h1>
  <script src="app.js" defer></script>
</body>
</html>
```

`defer` on `<script>` matters: it delays execution until the DOM is parsed without blocking parsing while the file downloads — the right default for almost every script tag.

## Semantic structure

Prefer elements that describe *meaning*, not just appearance — it's better for accessibility and SEO than an ocean of `<div>`s:

```html
<header>...</header>
<nav>...</nav>
<main>
  <article>
    <h2>Post title</h2>
    <p>Content...</p>
  </article>
  <aside>Related links</aside>
</main>
<footer>...</footer>
```

## Forms

```html
<form action="/submit" method="POST">
  <label for="email">Email</label>
  <input type="email" id="email" name="email" required>

  <label for="plan">Plan</label>
  <select id="plan" name="plan">
    <option value="free">Free</option>
    <option value="pro">Pro</option>
  </select>

  <button type="submit">Sign up</button>
</form>
```

Built-in validation attributes (`required`, `type="email"`, `pattern`, `minlength`) catch a lot of cases before any JavaScript runs.

## Accessibility basics

- Every `<img>` needs `alt` text (empty `alt=""` if it's purely decorative).
- Use real `<button>`/`<a>` elements for interactive controls instead of a `<div onclick>` — you get keyboard focus and screen-reader semantics for free.
- One `<h1>` per page, and don't skip heading levels just for font size (use CSS for that instead).

## `<template>` and custom elements

```html
<template id="row-template">
  <li class="row"><span class="name"></span></li>
</template>
```

```js
const tpl = document.getElementById("row-template");
const clone = tpl.content.cloneNode(true);
clone.querySelector(".name").textContent = "Ada";
document.querySelector("ul").appendChild(clone);
```

## Common gotchas

- Block vs inline elements affects what CSS properties (like `width`/`height`) actually apply — a `<span>` ignores them until you change its `display`.
- `<script>` at the very bottom of `<body>` was the old fix for blocking; `defer` in `<head>` is the modern equivalent and keeps script tags out of markup you might template dynamically.
- Self-closing tags (`<img />`) are optional in HTML5 (unlike strict XHTML) — `<img>` alone is valid.
