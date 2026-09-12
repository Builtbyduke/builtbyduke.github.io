# React

A JavaScript/TypeScript UI library built around components and a declarative render model: describe what the UI should look like for a given state, and React handles updating the DOM to match.

## Setup

```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install
npm run dev
```

Vite has largely replaced `create-react-app` as the default starter for its much faster dev server and build times.

## A component

```tsx
function Greeting({ name }: { name: string }) {
  return <h1>Hello, {name}!</h1>;
}
```

JSX compiles to `React.createElement(...)` calls, it looks like HTML but is real JavaScript, so `{}` drops back into JS expressions anywhere.

## State, `useState`

```tsx
import { useState } from "react";

function Counter() {
  const [count, setCount] = useState(0);
  return (
    <button onClick={() => setCount(count + 1)}>
      Clicked {count} times
    </button>
  );
}
```

`setCount` triggers a re-render; state updates are not applied instantly/synchronously, so don't rely on `count` being updated immediately after calling `setCount`.

## Effects, `useEffect`

```tsx
import { useEffect, useState } from "react";

function UserProfile({ id }: { id: string }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    let cancelled = false;
    fetch(`/api/users/${id}`)
      .then(res => res.json())
      .then(data => { if (!cancelled) setUser(data); });
    return () => { cancelled = true; }; // cleanup on unmount / id change
  }, [id]); // re-run only when id changes

  if (!user) return <p>Loading...</p>;
  return <p>{user.name}</p>;
}
```

The dependency array is the most common source of bugs, omitting a value used inside the effect leads to stale closures; the `eslint-plugin-react-hooks` rule catches most of these automatically.

## Lists & keys

```tsx
function TodoList({ items }: { items: { id: string; text: string }[] }) {
  return (
    <ul>
      {items.map(item => <li key={item.id}>{item.text}</li>)}
    </ul>
  );
}
```

`key` must be stable and unique per item (an ID, not the array index) so React can correctly track which DOM node maps to which data across re-renders.

## Sharing state, Context (for a handful of values)

```tsx
const ThemeContext = React.createContext("light");

function App() {
  return (
    <ThemeContext.Provider value="dark">
      <Toolbar />
    </ThemeContext.Provider>
  );
}

function Toolbar() {
  const theme = useContext(ThemeContext);
  return <div className={theme}>...</div>;
}
```

For larger apps, a dedicated state library (Zustand, Redux Toolkit, Jotai) usually replaces ad-hoc Context once you have more than a few cross-cutting pieces of state.

## Popular ecosystem

| Purpose | Common choice |
|---|---|
| Routing | React Router, or Next.js's file-based router |
| Full framework | Next.js, Remix |
| Styling | Tailwind CSS, CSS Modules |
| Server state/data fetching | TanStack Query (React Query) |
| Forms | React Hook Form |

## Common gotchas

- Mutating state directly (`user.name = "x"`) doesn't trigger a re-render, always create a new object/array (`setUser({ ...user, name: "x" })`).
- Every component re-renders when its state changes, and by default its children re-render too, `React.memo`, `useMemo`, `useCallback` exist for the cases where that becomes measurably slow, not as a default habit.
