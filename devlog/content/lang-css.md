# CSS

Styles and lays out [HTML](lang-html.html). Modern CSS (Grid, Flexbox, custom properties) handles most layouts without a preprocessor or framework.

## Selectors & specificity

```css
/* type, class, id, specificity increases left to right */
p { color: #222; }
.card { padding: 16px; }
#header { position: sticky; }

/* combinators */
.card > h2 { margin-top: 0; }      /* direct child */
.card p + p { margin-top: 8px; }   /* adjacent sibling */
nav a:hover { text-decoration: underline; }
```

Specificity order (low → high): type selectors → classes/attributes/pseudo-classes → IDs → inline styles → `!important`. Prefer classes over IDs for styling, and avoid `!important` except as an escape hatch against third-party CSS.

## Box model

```css
.box {
  box-sizing: border-box; /* padding/border included in width, set this globally */
  width: 300px;
  padding: 16px;
  border: 1px solid #ccc;
  margin: 8px;
}
```

```css
*, *::before, *::after { box-sizing: border-box; }
```

## Flexbox (one-dimensional layout)

```css
.row {
  display: flex;
  justify-content: space-between; /* main axis */
  align-items: center;            /* cross axis */
  gap: 12px;
}
.row > .grow { flex: 1; }
```

## Grid (two-dimensional layout)

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}
.grid .featured { grid-column: span 2; }
```

## Custom properties (CSS variables)

```css
:root {
  --brand: #5865f2;
  --radius: 8px;
}
.button {
  background: var(--brand);
  border-radius: var(--radius);
}
```

Unlike Sass variables, these are live in the DOM, you can override them per-component or with JS (`el.style.setProperty("--brand", "#ff0000")`), and they respect the cascade/inheritance.

## Responsive design

```css
.container { padding: 16px; }

@media (min-width: 768px) {
  .container { padding: 32px; }
}
```

Mobile-first (`min-width` queries, base styles for small screens) is the more common modern approach over `max-width` desktop-first queries.

## Popular tools

| Purpose | Common choice |
|---|---|
| Utility framework | Tailwind CSS |
| Preprocessor | Sass/SCSS (less necessary now that CSS has nesting & variables natively) |
| Component styling in JS frameworks | CSS Modules, styled-components |

## Common gotchas

- `z-index` only works on positioned elements (`position` other than `static`).
- Margins between two block elements can **collapse** (the larger one wins instead of both adding), a common source of "why is there extra space" bugs.
- `height: 100%` on a child does nothing unless the parent has an explicit height set somewhere up the chain.

See also: [React](lang-react.html) for how component-scoped styling typically layers on top of these fundamentals.
