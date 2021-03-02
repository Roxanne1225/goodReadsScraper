"""Main Entry Point for Scraper
This file runs the command line interface for the good reads scraper
"""

import os
import re
import sys
import argparse
import json
from bson.json_util import dumps
from dotenv import load_dotenv
from dataCollection import DataCollection
from book_scraper import BookScraper
from author_scraper import AuthorScraper

load_dotenv()
MONGO_CONNECTION_STRING = os.getenv('MONGO_CONNECTION_STRING')

def export(data_collection_type, file_path):
    """Export data from the database into json file

    Args:
        dataCollectionType (str): Name of data collection, either 'book' or 'author'
        file_path (str): Path of json file to export data into
    """

    if data_collection_type not in ('book', 'author'):
        print("Error: no collection named " + data_collection_type
        + ", please enter 'book' or 'author' ")
        return
    datacollection = DataCollection(MONGO_CONNECTION_STRING, 'goodReads', data_collection_type)
    data = datacollection.get_all_entries()
    data = list(data)
    json_data = dumps(data, indent = 2)

    with open(file_path, 'w') as file:
        file.write(json_data)

def import_json(data_collection_type, file_path):
    """Import information in a json file to the database

    Args:
        dataCollectionType (str): Name of data collection, either 'book' or 'author'
        file_path (str): Path of json file to extract info from
    """

    if data_collection_type not in ('book', 'author'):
        print("Error: no collection named " + data_collection_type
        + ", please enter 'book' or 'author' ")
        return
    datacollection = DataCollection(MONGO_CONNECTION_STRING, 'goodReads', data_collection_type)

    with open(file_path) as file:
        file_data = json.load(file)
    for entry in file_data:
        if "_id" in entry:
            del entry["_id"]
        if not datacollection.document_already_exist(entry):
            datacollection.push_to_collection(entry)

def scrape(data_collection_type, start_url, target_number):
    """Scrape data from goodreads starting with the starting url

    Args:
        data_collection_type (str):  Name of data collection, either 'book' or 'author'
        start_url (str): The url to start scraping from
        target_number (int): Number of books/authors to scrape
    """

    if data_collection_type == "book":
        if not re.search(r'([https://]?)www.goodreads.com/book/show/(.*)', start_url):
            print("Please provide a valid url pointing to a book in goodReads")
            sys.exit(1)
        if target_number > 200:
            print("Cannot scrape more than 200 books at once")
            sys.exit(1)
        data_collection = DataCollection(MONGO_CONNECTION_STRING, "goodReads", "book")
        book_scraper = BookScraper(data_collection)
        book_scraper.scrapeBooks(start_url, target_number)
    elif data_collection_type == "author":
        if not re.search(r'([https://]?)www.goodreads.com/author/show/(.*)', start_url):
            print("Please provide a valid url pointing to an author in goodReads")
            sys.exit(1)
        if target_number > 50:
            print("Cannot scrape more than 50 authors at once")
            sys.exit(1)
        data_collection = DataCollection(MONGO_CONNECTION_STRING, "goodReads", "author")
        author_scraper = AuthorScraper(data_collection)
        author_scraper.scrapeAuthors(start_url, target_number)
    else:
        print("Error: no collection named " + data_collection_type
        + ", please enter 'book' or 'author' ")
        return

def clear_database(data_collection_type):
    """Clear the specified data collection in the database

    Args:
        data_collection_type (str):  Name of data collection, either 'book' or 'author'
    """
    collection_name = data_collection_type
    if collection_name not in ('book', 'author'):
        print("Error: no collection named " + data_collection_type
         + ", please enter 'book' or 'author' ")
        return
    database = DataCollection(MONGO_CONNECTION_STRING, "goodReads", collection_name)
    database.empty_data_collection()


def main():
    """The main method
    """
    parser = argparse.ArgumentParser(description = "Web scraper for goodReads")

    parser.add_argument("-s", "--scrape", type = str, nargs = 3,
                        metavar = ("book_or_author", "start_url", "target_number"), default = None,
                        help = "scrape data")

    parser.add_argument("-e", "--export", type = str, nargs = 2,
                        metavar = ('book_or_author','path'), default = None,
                        help = "export data to json file")
    parser.add_argument("-i", "--importJSON", type = str, nargs = 2,
                        metavar = ('book_or_author','path'), default = None,
                        help = "import data from json")

    parser.add_argument("--clear", type = str, nargs = 1,
                        metavar = ('book_or_author'), default = None,
                        help = "clear database")


    args = parser.parse_args()
    if args.scrape is not None:
        scrape(args.scrape[0], args.scrape[1], int(args.scrape[2]))
    if args.export is not None:
        export(args.export[0], args.export[1])
    if args.importJSON is not None:
        import_json(args.importJSON[0], args.importJSON[1])
    if args.clear is not None:
        clear_database(args.clear[0])

if __name__ == "__main__":
    main()
