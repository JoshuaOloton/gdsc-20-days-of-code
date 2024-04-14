from . import books
from ..models import Book
from api import db
from datetime import datetime
from flask import jsonify, request
from flask_jwt_extended import jwt_required
from operator import itemgetter
from sqlalchemy import func


@books.route('/books/', methods=['GET'])
@jwt_required()
def get_books():
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books]), 200


@books.route('/books/<int:id>', methods=['GET'])
@jwt_required()
def get_book(id):
    book = Book.query.get(id)
    if book is None:
        return jsonify({'error': 'Book not found'}), 404
    return jsonify(book.to_dict()), 200


@books.route('/books/', methods=['POST'])
@jwt_required()
def post_book():
    try:
        name = request.json.get('name')
        author = request.json.get('author')
        date_published = request.json.get('date_published')
        price = request.json.get('price')
        in_stock = request.json.get('in_stock')

        # Check if book already exists 
        book = Book.query.filter(func.lower(Book.name) == name.lower(), Book.author == author).first()
        if book:
            return jsonify({'error': 'Book already exists'}), 400

        book = Book(
            name=name,
            author=author,
            date_published=datetime.strptime(date_published, "%Y-%m-%dT%H:%M:%S"),
            price=price,
            in_stock=in_stock
        )
        db.session.add(book)
        db.session.commit()

        return jsonify(book.to_dict()), 201
    except ValueError:
        return jsonify({'error': 'Invalid date format, follow this format %Y-%m-%dT%H:%M:%S'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@books.route('/books/<int:id>', methods=['PUT'])
@jwt_required()
def put_book(id):
    try:
        book = Book.query.get(id)
        if book is None:
            return jsonify({'error': 'Book not found'}), 404
        
        name, author, date_published, price, in_stock = itemgetter('name', 'author', 'date_published', 'price', 'in_stock')(request.json)
        book.name = name
        book.author = author
        book.date_published = datetime.strptime(date_published, "%Y-%m-%dT%H:%M:%S")
        book.price = price
        book.in_stock = in_stock
        
        db.session.commit()
        return jsonify(book.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500  


@books.route('/books/<int:id>', methods=['PATCH'])
@jwt_required()
def patch_book(id):
    try:
        book = Book.query.get(id)
        if book is None:
            return jsonify({'error': 'Book not found'}), 404
        
        data = request.json
        for key, value in data.items():
            if hasattr(book, key):
                if key != 'id':
                    if key == 'date_published':
                        value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
                    setattr(book, key, value)
                
        db.session.commit()
        return jsonify(book.to_dict()), 200
    except ValueError:
        return jsonify({'error': 'Invalid date format, follow this format %Y-%m-%dT%H:%M:%S'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@books.route('/books/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_book(id):
    book = Book.query.get(id)
    if book is None:
        return jsonify({'error': 'Book not found'}), 404
    
    db.session.delete(book)
    db.session.commit()

    return jsonify({'message': 'Book deleted'}), 200

