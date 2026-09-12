# Python

A readable, batteries-included language used everywhere from scripting to data science to web backends.

## Setup

```bash
python3 --version
python3 -m venv .venv         # isolated environment per project
source .venv/bin/activate     # (.venv\Scripts\activate on Windows)
pip install requests
```

Always work inside a virtual environment, installing packages globally leads to version conflicts across projects.

## Core syntax

```python
name = "Ada"
count = 0

def add(a: int, b: int) -> int:
    return a + b

nums = [1, 2, 3]
doubled = [n * 2 for n in nums]        # list comprehension
squares = {n: n ** 2 for n in nums}    # dict comprehension

user = {"name": "Ada", "age": 30}
print(f"{user['name']} is {user['age']}")

class Animal:
    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        return f"{self.name} makes a sound."
```

Indentation is syntax, a block is defined by consistent indentation (4 spaces is the near-universal convention), not braces.

## Context managers (`with`)

```python
with open("data.txt") as f:
    contents = f.read()
# file is automatically closed here, even if an exception was raised
```

## Error handling

```python
try:
    value = int(user_input)
except ValueError as e:
    print(f"Invalid number: {e}")
finally:
    cleanup()
```

## Type hints (optional, widely used in real projects)

```python
from typing import Optional

def find_user(user_id: int) -> Optional[dict]:
    return database.get(user_id)
```

Type hints aren't enforced at runtime, tools like `mypy` or `pyright` check them statically, catching mismatches before you run anything.

## Popular libraries/frameworks

| Purpose | Common choice |
|---|---|
| Web framework | Django (batteries-included), FastAPI (async, typed, API-first), Flask (minimal) |
| Data/ML | pandas, NumPy, PyTorch, scikit-learn |
| Testing | pytest |
| HTTP client | requests, httpx (async) |
| Dependency management | Poetry, or `pip` + `requirements.txt` |

## A minimal FastAPI endpoint

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"id": user_id, "name": "Ada"}
```

```bash
uvicorn main:app --reload
```

## Common gotchas

- Mutable default arguments (`def f(items=[])`) are created **once** and shared across calls, use `None` and initialize inside the function instead.
- Late binding in closures: a loop variable captured in a lambda/function inside the loop reflects its *final* value, not the value at each iteration, unless explicitly bound as a default argument.
- Python 2 vs 3: Python 2 is end-of-life, any tutorial written for it (print statements without parens, etc.) is outdated.
