# SQL Demos

SQL scripts demonstrating database schema design, data manipulation, and analytical queries.

## Files

| File | Description |
|------|-------------|
| [schema.sql](schema.sql) | Table definitions for a sample e-commerce sales database |
| [queries.sql](queries.sql) | Analytical queries: aggregations, window functions, CTEs |

## Compatibility

The scripts are written in standard SQL and tested against **PostgreSQL 15** and **SQLite 3**.  
For PostgreSQL, run:

```bash
psql -U <user> -d <database> -f schema.sql
psql -U <user> -d <database> -f queries.sql
```

For SQLite:

```bash
sqlite3 sales.db < schema.sql
sqlite3 sales.db < queries.sql
```
