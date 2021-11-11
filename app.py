from flask import Flask, request, jsonify, json
import pymongo
from pymongo import MongoClient
from pymongo import collection
from pymongo import results
from pymongo import message

app = Flask(__name__)

cluster = MongoClient("MONGO URI")
db = cluster["Book"]
collection = db["book"]

post = {"_id": 0, "name": "Aku"}
collection.delete_one({"_id": 0})
collection.insert_one(post)


@app.route("/", methods=['GET'])
def ok():
    return {
        "message": "The API is working fine."
    }

@app.route("/book", methods=['GET'])
def read_Book():
    allBooks = []
    results = collection.find()
    for result in results:
        result['_id'] = str(result['_id'])
        allBooks.append(result)
        # print(jsonify(allBooks))
    return jsonify(allBooks)

@app.route("/book/createBook", methods=['POST'])
def create_Book():
    book_id = request.form["id"]
    book_name = request.form['name']
    book_author = request.form['author']
    book = {}
    book["_id"] = book_id
    book["name"] = book_name
    book["author"] = book_author
    collection.insert_one(book)

    return {
        "message": book_name+" added to database"
    }

@app.route("/book/deleteBook/<bookID>", methods=["DELETE"])
def delete_Book(bookID):
    book = collection.find_one({"_id": str(bookID)})
    print(book)
    collection.delete_one({"_id": str(bookID)})
    return {
        "message": book["name"] + " Deleted from Database"
    }

@app.route("/book/updateBook/<bookID>", methods=["PUT"])
def update_Book(bookID):
    book = collection.find_one({"_id": str(bookID)})
    book_name = request.form['name']
    book_author = request.form['author']
    # book = {}
    # book["name"] = book_name
    # book["author"] = book_author
    collection.update_one({"_id": str(bookID)}, {"$set": {"name": book_name, "author": book_author}})

    return {
        "message": book["name"] + " Updated"
    }



if (__name__ == "__main__"):
    app.run(debug=True)