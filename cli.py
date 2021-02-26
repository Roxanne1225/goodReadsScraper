import os 
import argparse 
from pymongo import MongoClient 
from bson.json_util import dumps, loads 
from dataCollection import DataCollection
import json
from bookScraper import BookScraper
from authorScraper import AuthorScraper
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_CONNECTION_STRING = os.getenv('MONGO_CONNECTION_STRING')

def export(args):
    dataCollectionType = args.export[0]
    if(dataCollectionType != 'book' and dataCollectionType != 'author'):
        print("Error: no collection named " + dataCollectionType + ", please enter 'book' or 'author' ")
        return
    datacollection = DataCollection(MONGO_CONNECTION_STRING, 'goodReads', dataCollectionType)
    
    data = datacollection.getAllEntry()
    data = list(data) 
    json_data = dumps(data, indent = 2)  

    with open(args.export[1], 'w') as file: 
        file.write(json_data)

def importJSON(args):
    print("import")
    dataCollectionType = args.importJSON[0]
    if(dataCollectionType != 'book' and dataCollectionType != 'author'):
        print("Error: no collection named " + dataCollectionType + ", please enter 'book' or 'author' ")
        return
    datacollection = DataCollection(MONGO_CONNECTION_STRING, 'goodReads', dataCollectionType)

    with open(args.importJSON[1]) as file: 
        file_data = json.load(file) 
    print(file_data[0])
    for entry in file_data:
        # print(entry)
        if("_id" in entry):
            del entry["_id"]
        if(not datacollection.documentAlreadyExist(entry)):
            datacollection.pushToCollection(entry)

def scrape(args):
    target_number = int(args.scrape[2])
    start_url = args.scrape[1]
    scrapeType = ""
    if(args.scrape[0] == "book"):
        dataCollection = DataCollection(MONGO_CONNECTION_STRING, "goodReads", "book")
        bookScraper = BookScraper(dataCollection)
        bookScraper.scrapeBooks(start_url, target_number)
    elif(args.scrape[0] == "author"):
        dataCollection = DataCollection(MONGO_CONNECTION_STRING, "goodReads", "author")
        authorScraper = AuthorScraper(dataCollection)
        authorScraper.scrapeAuthors(start_url, target_number)
    else:
        print("Error: no collection named " + args.scrape[0] + ", please enter 'book' or 'author' ")
        return

def clearDatabase(args):
    collection_name = args[0]
    if(collection_name != "book" and collection_name != "author"):
        print("Error: no collection named " + args[0] + ", please enter 'book' or 'author' ")
        return
    db = DataCollection(MONGO_CONNECTION_STRING, "goodReads", collection_name)
    db.emptyDataCollection()


def main(): 
# create parser object 
#choices=["book", "author"], 
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
      
    if args.scrape != None: 
        scrape(args) 
    if args.export != None:
        export(args)
    if args.importJSON != None:
        importJSON(args)
    if args.clear != None:
        clearDatabase(args.clear)



if __name__ == "__main__": 
    main() 