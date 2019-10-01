from flask import Flask, jsonify, request, Response
from flask_sqlalchemy import SQLAlchemy
import json
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/books'
db = SQLAlchemy(app)

class book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(80), unique =True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer())

    def __init__(self, isbn, name, price):
        self.isbn = isbn
        self.name = name
        self.price = price
    def __repr__(self):
        return '<book %r' % self.isbn

print(__name__)

books = [
    {
        'name': 'Rwandan Cultural',
        'price': 9032,
        'isbn': 90293029
    },
    {
        'name': 'USA Culture',
        'price': 9032,
        'isbn': 90293029
    }
]


def validBookObject(bookObject):
    if("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
        return True
    else:
        return False


@app.route('/')
def helloWorld():
    return 'Hello World'


@app.route('/books')
def get_books():
    return jsonify({'books': books})


@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = {}
    for book in books:
        if book['isbn'] == isbn:
            return_value = {
                'name': book['name'],
                'price': book['price']
            }
    return jsonify(return_value)


@app.route('/books/', methods=['POST'])
def add_book():
    # return jsonify(request.get_json())
    request_data = request.get_json()
    if(validBookObject(request_data)):
        new_book = {
            "name": request_data['name'],
            "price": request_data['price'],
            "isbn": request_data['isbn'],
        }
        books.insert(0, new_book)
        response = Response('', 201, mimetype='application/json')
        response.headers['Location'] = "/books/" + str(new_book['isbn'])
        return response
    else:
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in request",
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg),
                            status=400, mimetype="application/json")
        return response


@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()
    new_book = {
        'name': request_data['name'],
        'price': request_data['price'],
        'isbn': isbn
    }
    i = 0
    for book in books:
        currentIsbn = book["isbn"]
        if currentIsbn == isbn:
            books[i] = new_book
        i += 1
    response = Response("", status=204)
    return new_book


@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    updated_book = {}
    if("name" in request_data):
        updated_book["name"] = request_data['name']
    for book in books:
        if book["isbn"] == isbn:
            book.update(updated_book)  
    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(isbn)
    return response


app.run(port=5000)
