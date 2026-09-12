# SQL

The language for querying and manipulating relational databases (PostgreSQL, MySQL, SQLite, SQL Server), syntax varies slightly between engines, but the core is near-universal.

## Creating tables

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    total NUMERIC(10, 2) NOT NULL
);
```

`SERIAL` is Postgres-specific auto-increment syntax; MySQL uses `AUTO_INCREMENT`, SQLite uses `INTEGER PRIMARY KEY AUTOINCREMENT`, this kind of small dialect difference is common across engines.

## CRUD basics

```sql
-- Create
INSERT INTO users (name, email) VALUES ('Ada', 'ada@example.com');

-- Read
SELECT id, name FROM users WHERE email = 'ada@example.com';

-- Update
UPDATE users SET name = 'Ada Lovelace' WHERE id = 1;

-- Delete
DELETE FROM users WHERE id = 1;
```

## Joins

```sql
SELECT users.name, orders.total
FROM users
INNER JOIN orders ON orders.user_id = users.id
WHERE orders.total > 100
ORDER BY orders.total DESC;
```

| Join type | Returns |
|---|---|
| `INNER JOIN` | only rows with a match in both tables |
| `LEFT JOIN` | all rows from the left table, matched rows (or `NULL`) from the right |
| `RIGHT JOIN` | mirror of `LEFT JOIN` |
| `FULL OUTER JOIN` | all rows from both, matched where possible |

## Aggregation

```sql
SELECT user_id, COUNT(*) AS order_count, SUM(total) AS total_spent
FROM orders
GROUP BY user_id
HAVING SUM(total) > 500
ORDER BY total_spent DESC;
```

`WHERE` filters rows before grouping; `HAVING` filters groups after aggregation, a common point of confusion since both look like a filter clause.

## Subqueries & CTEs

```sql
WITH big_spenders AS (
    SELECT user_id, SUM(total) AS spent
    FROM orders
    GROUP BY user_id
    HAVING SUM(total) > 500
)
SELECT users.name, big_spenders.spent
FROM users
JOIN big_spenders ON big_spenders.user_id = users.id;
```

A CTE (`WITH ... AS (...)`) names a subquery so it can be referenced like a temporary table, usually more readable than deeply nested subqueries.

## Indexes

```sql
CREATE INDEX idx_orders_user_id ON orders(user_id);
```

Indexes speed up lookups/joins on that column at the cost of slightly slower writes and extra storage, add them on columns you filter/join on frequently, not on every column.

## Common gotchas

- `NULL` doesn't equal anything, including itself, use `IS NULL` / `IS NOT NULL`, never `= NULL`.
- `SELECT *` in application code breaks silently when someone adds a column, name columns explicitly in production queries.
- String concatenation of user input into a query is the classic SQL-injection vector, always use parameterized queries/prepared statements from your application language instead of building SQL strings by hand.
