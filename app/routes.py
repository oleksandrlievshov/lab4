from flask import Blueprint, request, jsonify
from app.models import Book
from app.schemas import BookSchema
from app import db
from marshmallow import ValidationError

bp = Blueprint('routes', __name__)
book_schema = BookSchema()
book_list_schema = BookSchema(many=True)

@bp.route('/books', methods=['GET'])
def get_books():
    cursor = request.args.get('cursor', type=int)
    limit = request.args.get('limit', 10, type=int)

    query = Book.query.order_by(Book.id)
    if cursor:
        query = query.filter(Book.id > cursor)
    books = query.limit(limit).all()

    serialized_books = book_list_schema.dump(books)
    next_cursor = books[-1].id if books else None

    return jsonify({
        "data": serialized_books,
        "next_cursor": next_cursor
    }), 200

@bp.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify(book_schema.dump(book)), 200

@bp.route('/books', methods=['POST'])
def create_book():
    try:
        data = book_schema.load(request.json)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    book = Book(**data)
    db.session.add(book)
    db.session.commit()
    return jsonify(book_schema.dump(book)), 201

@bp.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted"}), 200
