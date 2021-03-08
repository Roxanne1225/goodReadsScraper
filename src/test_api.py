import pytest
import requests
import os
from dataCollection import DataCollection
from dotenv import load_dotenv
BAES_URL = "http://127.0.0.1:5000/api"

load_dotenv()
MONGO_CONNECTION_STRING = os.getenv('MONGO_CONNECTION_STRING')


book_data_collection = DataCollection(MONGO_CONNECTION_STRING, "goodReads", 'book')
author_data_collection = DataCollection(MONGO_CONNECTION_STRING, "goodReads", 'author')

def test_connect_to_api():
     response = requests.get(BAES_URL)
     assert response.status_code == 200

def test_get_book():
    book = {"url": "testurl2", "id":"testid2"}
    book_data_collection.push_to_collection(book)
    response = requests.get(BAES_URL + '/book?id=testid2')
    assert response.status_code == 200

def test_get_author():
    author = {"url": "testurl2", "id":"testid2"}
    author_data_collection.push_to_collection(author)
    response = requests.get(BAES_URL + '/author?id=testid2')
    assert response.status_code == 200
    
def test_put_author():
    author = {"url": "testurl2", "id":"testid2"}
    author_data_collection.push_to_collection(author)
    response = requests.put(BAES_URL + "/author?id=testid2", json={"url":"urltesting"})
    assert response.status_code == 200
    response = requests.get(BAES_URL + '/author?id=testid2')
    assert response.json()["data"]['url'] == "urltesting"

def test_post_author():
    author = [{"url": "testurl3", "id":"testid3"}]
    response = requests.post(BAES_URL+"/author", json=author)
    assert response.status_code == 200
    response = requests.get(BAES_URL + '/author?id=testid3')
    assert response.json()["data"]['url'] == "testurl3"

def test_delete_author():
    author = [{"url": "testurl3", "id":"testid3"}]
    response = requests.post(BAES_URL+"/author", json=author)
    assert response.status_code == 200
    response = requests.delete(BAES_URL + '/author?id=testid3')
    assert response.status_code == 200
    response = requests.get(BAES_URL + '/author?id=testid3')
    assert response.status_code == 404
