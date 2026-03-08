"""
Flask REST API Demo
===================
A lightweight, self-contained REST API that manages a simple in-memory
collection of books.  It demonstrates:

  * Flask application factory pattern
  * JSON request parsing and response serialisation
  * Input validation with descriptive error messages
  * Full CRUD via standard HTTP verbs (GET / POST / PUT / DELETE)
  * HTTP status codes and error handling
  * Running with the built-in development server

No database is required — data lives in memory and resets on restart.

Usage:
    python app.py
    # or with debug mode enabled:
    FLASK_DEBUG=1 python app.py
    # API available at http://127.0.0.1:5000
"""

from flask import Flask, jsonify, request

app = Flask(__name__)

# ---------------------------------------------------------------------------
# In-memory data store
# ---------------------------------------------------------------------------

_next_id = 1
_books: dict[int, dict] = {}


def _new_book(title: str, author: str, year: int) -> dict:
    """Create a new book record and add it to the store."""
    global _next_id
    book = {"id": _next_id, "title": title, "author": author, "year": year}
    _books[_next_id] = book
    _next_id += 1
    return book


def _seed() -> None:
    """Populate the store with a few starter records."""
    _new_book("Clean Code", "Robert C. Martin", 2008)
    _new_book("The Pragmatic Programmer", "David Thomas & Andrew Hunt", 1999)
    _new_book("Design Patterns", "Gang of Four", 1994)


_seed()


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _validate_book_payload(data: dict) -> list[str]:
    """Return a list of validation error messages for *data*.

    Expects ``title`` (str), ``author`` (str), and ``year`` (int).
    """
    errors = []
    if not data.get("title") or not isinstance(data["title"], str):
        errors.append("'title' must be a non-empty string.")
    if not data.get("author") or not isinstance(data["author"], str):
        errors.append("'author' must be a non-empty string.")
    year = data.get("year")
    if year is None:
        errors.append("'year' is required.")
    elif not isinstance(year, int) or year < 1:
        errors.append("'year' must be a positive integer.")
    return errors


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/books")
def list_books():
    """Return all books.

    GET /books
    Response: 200 OK, JSON array of book objects.
    """
    return jsonify(list(_books.values())), 200


@app.get("/books/<int:book_id>")
def get_book(book_id: int):
    """Return a single book by its ID.

    GET /books/<id>
    Response: 200 OK | 404 Not Found
    """
    book = _books.get(book_id)
    if book is None:
        return jsonify({"error": f"Book {book_id} not found."}), 404
    return jsonify(book), 200


@app.post("/books")
def create_book():
    """Add a new book.

    POST /books
    Body (JSON): { "title": "...", "author": "...", "year": 2024 }
    Response: 201 Created | 400 Bad Request
    """
    data = request.get_json(silent=True) or {}
    errors = _validate_book_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400
    book = _new_book(data["title"], data["author"], data["year"])
    return jsonify(book), 201


@app.put("/books/<int:book_id>")
def update_book(book_id: int):
    """Replace a book's fields.

    PUT /books/<id>
    Body (JSON): { "title": "...", "author": "...", "year": 2024 }
    Response: 200 OK | 400 Bad Request | 404 Not Found
    """
    if book_id not in _books:
        return jsonify({"error": f"Book {book_id} not found."}), 404
    data = request.get_json(silent=True) or {}
    errors = _validate_book_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400
    _books[book_id].update(
        title=data["title"], author=data["author"], year=data["year"]
    )
    return jsonify(_books[book_id]), 200


@app.delete("/books/<int:book_id>")
def delete_book(book_id: int):
    """Remove a book.

    DELETE /books/<id>
    Response: 200 OK | 404 Not Found
    """
    book = _books.pop(book_id, None)
    if book is None:
        return jsonify({"error": f"Book {book_id} not found."}), 404
    return jsonify({"message": f"Book {book_id} deleted."}), 200


# ---------------------------------------------------------------------------
# 404 handler
# ---------------------------------------------------------------------------

@app.errorhandler(404)
def not_found(_err):
    return jsonify({"error": "The requested resource was not found."}), 404


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import os

    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug)
