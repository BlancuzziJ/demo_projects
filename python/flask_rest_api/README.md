# Flask REST API Demo

A lightweight, self-contained REST API built with **Flask** that manages a collection of books. This demo showcases fundamental REST API patterns using Python's most popular micro-framework.

---

## What it demonstrates

| Concept | Implementation |
|---|---|
| Application factory | `Flask(__name__)` with modular structure |
| CRUD endpoints | `GET`, `POST`, `PUT`, `DELETE` on `/books` |
| Route parameters | `/books/<int:book_id>` |
| JSON request parsing | `request.get_json()` |
| Input validation | `_validate_book_payload()` with descriptive errors |
| HTTP status codes | `200`, `201`, `400`, `404` |
| Error handling | `@app.errorhandler(404)` |
| In-memory data store | Plain Python `dict` (no database needed) |

---

## Quick start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the development server

```bash
python app.py
```

The API is now available at `http://127.0.0.1:5000`.

---

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/books` | List all books |
| `GET` | `/books/<id>` | Get a single book |
| `POST` | `/books` | Create a new book |
| `PUT` | `/books/<id>` | Update an existing book |
| `DELETE` | `/books/<id>` | Delete a book |

---

## Example requests

### List all books

```bash
curl http://127.0.0.1:5000/books
```

```json
[
  {"id": 1, "title": "Clean Code", "author": "Robert C. Martin", "year": 2008},
  {"id": 2, "title": "The Pragmatic Programmer", "author": "David Thomas & Andrew Hunt", "year": 1999},
  {"id": 3, "title": "Design Patterns", "author": "Gang of Four", "year": 1994}
]
```

### Get a single book

```bash
curl http://127.0.0.1:5000/books/1
```

```json
{"id": 1, "title": "Clean Code", "author": "Robert C. Martin", "year": 2008}
```

### Create a book

```bash
curl -X POST http://127.0.0.1:5000/books \
     -H "Content-Type: application/json" \
     -d '{"title": "Python Crash Course", "author": "Eric Matthes", "year": 2019}'
```

```json
{"id": 4, "title": "Python Crash Course", "author": "Eric Matthes", "year": 2019}
```

### Update a book

```bash
curl -X PUT http://127.0.0.1:5000/books/4 \
     -H "Content-Type: application/json" \
     -d '{"title": "Python Crash Course", "author": "Eric Matthes", "year": 2023}'
```

```json
{"id": 4, "title": "Python Crash Course", "author": "Eric Matthes", "year": 2023}
```

### Delete a book

```bash
curl -X DELETE http://127.0.0.1:5000/books/4
```

```json
{"message": "Book 4 deleted."}
```

### Validation error example

```bash
curl -X POST http://127.0.0.1:5000/books \
     -H "Content-Type: application/json" \
     -d '{"title": "", "year": "not-a-number"}'
```

```json
{
  "errors": [
    "'title' must be a non-empty string.",
    "'author' must be a non-empty string.",
    "'year' must be a positive integer."
  ]
}
```

---

## Project structure

```
flask_rest_api/
├── app.py           # Flask application with all routes
├── requirements.txt # Python dependencies
└── README.md        # This file
```

---

## Notes

- Data is stored **in memory** and resets when the server restarts. To persist data, swap the `_books` dict for a SQLite database using `flask-sqlalchemy` or the built-in `sqlite3` module.
- The `FLASK_DEBUG=1` environment variable enables the Werkzeug debugger for local development. Never set it in production.
