import os
from flask import Flask, request, abort
from dotenv import load_dotenv
from dataCollection import DataCollection
from query_parser import *

load_dotenv()
MONGO_CONNECTION_STRING = os.getenv('MONGO_CONNECTION_STRING')

# def create_app():

app = Flask(__name__)

book_data_collection = DataCollection(MONGO_CONNECTION_STRING, "goodReads", 'book')
author_data_collection = DataCollection(MONGO_CONNECTION_STRING, "goodReads", 'author')

def list_to_dict(input_list):
    return {"data":input_list}

def get_data(args, data_collection):
    if(len(args) == 0):  # no field params passed in, return all data
        all_data = list(data_collection.get_all_entries())
        for entry in all_data:
            entry['_id'] = str(entry['_id'])
        return list_to_dict(all_data)
    else:
        if 'id' in args:
            data_info = data_collection.find_by_id(args['id'])
            if(data_info is None):
                abort(404)
            data_info['_id'] = str(data_info['_id'])
            return list_to_dict(data_info)
        abort(400)

# api/book?id={attr_value} Example: /book?id=3735293
@app.route('/api/book', methods=['GET'])
def get_book():
    args = request.args
    return get_data(args, book_data_collection)

@app.route('/api/book', methods=['PUT'])
def put_book():
    args = request.args
    book_data_collection.update_by_id(args['id'], args.to_dict())
    return "success"

@app.route('/api/author', methods=['GET'])
def get_author():
    args = request.args
    return get_data(args, author_data_collection)

@app.route('/api/author', methods=['PUT'])
def put_author():
    args = request.args
    author_data_collection.update_by_id(args['id'], args.to_dict())
    return "success"

@app.route('/api/search', methods=['GET'])
def search():
    args = request.args
    if(len(args)!= 1):
        print("wrong number of arguments")
    if 'q' not in args:
        abort(400)
    query = args['q']
    results = list(eval_query(query))
    for entry in results:
            entry['_id'] = str(entry['_id'])
    return list_to_dict(results)

def post_data(data_collection, json_data):
    for entry in json_data:
        if "_id" in entry:
            del entry["_id"]
        print(entry)
        data_collection.push_to_collection(entry)

@app.route('/api/book', methods=['POST'])
def post_one_book():
    json_data = request.json
    print(json_data)
    post_data(book_data_collection, json_data)
    return "success"

@app.route('/api/books', methods=['POST'])
def post_books():
    json_data = request.json
    post_data(book_data_collection, json_data)
    return "success"

@app.route('/api/author', methods=['POST'])
def post_one_author():
    json_data = request.json
    post_data(author_data_collection, json_data)
    return "success"

@app.route('/api/authors', methods=['POST'])
def post_authors():
    json_data = request.json
    post_data(author_data_collection, json_data)
    return "success"


@app.route('/')
def hello_world():
    return 'Hello, Roxanne!'

if __name__ == "__main__":
    app.run(debug=True)