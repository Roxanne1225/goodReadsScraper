import os
from flask import Flask, request, abort
from dotenv import load_dotenv
from dataCollection import DataCollection

load_dotenv()
MONGO_CONNECTION_STRING = os.getenv('MONGO_CONNECTION_STRING')

# def create_app():

app = Flask(__name__)

book_data_collection = DataCollection(MONGO_CONNECTION_STRING, "goodReads", 'book')
author_data_collection = DataCollection(MONGO_CONNECTION_STRING, "goodReads", 'author')

def list_to_dict(input_list):
    return {"data":input_list}

# api/book?id={attr_value} Example: /book?id=3735293
@app.route('/api/book', methods=['GET'])
def get_book():
    args = request.args
    if(len(args) == 0):  # no field params passed in, return all book data
        books = list(book_data_collection.get_all_entries())
        for book in books:
            book['_id'] = str(book['_id'])
        return list_to_dict(books)
    else:
        if args['id']:
            book_info = book_data_collection.find_by_id(args['id'])
            if(book_info is None):
                abort(404)
            book_info['_id'] = str(book_info['_id'])
            return book_info
    return
    # return args['id']




@app.route('/')
def hello_world():
    return 'Hello, Roxanne!'

if __name__ == "__main__":
    app.run(debug=True)