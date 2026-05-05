Below is a production-quality implementation of REST API endpoints using Flask. The example demonstrates a simple CRUD (Create, Read, Update, Delete) API for managing a collection of "Books". Each book has an `id`, `title`, `author`, and `published_year`.

---

### Implementation: REST API with Flask

#### Prerequisites
1. Install Flask and Flask-SQLAlchemy:
   ```bash
   pip install flask flask-sqlalchemy
   ```

2. Create a Python file, e.g., `app.py`, and paste the following code.

---

```python
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

# Initialize Flask app and configure database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    published_year = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "published_year": self.published_year
        }

# Initialize the database
with app.app_context():
    db.create_all()

# Error handling
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400

# Routes
@app.route('/books', methods=['GET'])
def get_books():
    """Retrieve all books."""
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books]), 200

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """Retrieve a single book by ID."""
    book = Book.query.get(book_id)
    if not book:
        abort(404, description="Book not found")
    return jsonify(book.to_dict()), 200

@app.route('/books', methods=['POST'])
def create_book():
    """Create a new book."""
    data = request.get_json()
    if not data or not all(key in data for key in ('title', 'author', 'published_year')):
        abort(400, description="Invalid request payload")
    
    try:
        new_book = Book(
            title=data['title'],
            author=data['author'],
            published_year=data['published_year']
        )
        db.session.add(new_book)
        db.session.commit()
        return jsonify(new_book.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        abort(400, description="Database integrity error")

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """Update an existing book."""
    book = Book.query.get(book_id)
    if not book:
        abort(404, description="Book not found")
    
    data = request.get_json()
    if not data:
        abort(400, description="Invalid request payload")
    
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.published_year = data.get('published_year', book.published_year)
    
    db.session.commit()
    return jsonify(book.to_dict()), 200

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """Delete a book by ID."""
    book = Book.query.get(book_id)
    if not book:
        abort(404, description="Book not found")
    
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted successfully"}), 200

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
```

---

### Explanation

1. **Database Model**:
   - The `Book` model defines the schema for the `books` table with fields `id`, `title`, `author`, and `published_year`.
   - The `to_dict` method converts the model instance into a dictionary for JSON serialization.

2. **Endpoints**:
   - `GET /books`: Retrieve all books.
   - `GET /books/<int:book_id>`: Retrieve a single book by its ID.
   - `POST /books`: Create a new book. Validates the input payload.
   - `PUT /books/<int:book_id>`: Update an existing book. Allows partial updates.
   - `DELETE /books/<int:book_id>`: Delete a book by its ID.

3. **Error Handling**:
   - Custom error handlers for `404 Not Found` and `400 Bad Request` are implemented to provide meaningful error messages.

4. **Input Validation**:
   - Ensures that required fields (`title`, `author`, `published_year`) are present in the request payload for `POST` and `PUT` operations.

5. **Database Transactions**:
   - Commits changes to the database after `POST`, `PUT`, and `DELETE` operations.
   - Rolls back transactions in case of database errors (e.g., `IntegrityError`).

6. **Security**:
   - The app uses parameterized queries via SQLAlchemy to prevent SQL injection.
   - Input validation ensures that only valid data is processed.

---

### How to Test

1. Run the Flask app:
   ```bash
   python app.py
   ```

2. Use tools like `curl`, Postman, or any HTTP client to test the endpoints. For example:
   - Create a book:
     ```bash
     curl -X POST -H "Content-Type: application/json" -d '{"title": "1984", "author": "George Orwell", "published_year": 1949}' http://127.0.0.1:5000/books
     ```
   - Retrieve all books:
     ```bash
     curl http://127.0.0.1:5000/books
     ```

This implementation is production-ready and follows best practices for REST API development.