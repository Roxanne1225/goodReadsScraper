import os 
import argparse 
from pymongo import MongoClient 
from bson.json_util import dumps, loads 
from dataCollection import DataCollection
import json
  
def export(args):
    c = "mongodb+srv://Roxanne1225:SanToria0515@cluster0.vgct4.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    dataCollectionType = args.export[0]
    if(dataCollectionType != 'book' and dataCollectionType != 'author'):
        print("Error: no collection named " + dataCollectionType + ", please enter 'book' or 'author' ")
        return
    datacollection = DataCollection(c, 'goodReads', dataCollectionType)
    
    data = datacollection.getAllEntry()
    data = list(data) 
    json_data = dumps(data, indent = 2)  

    with open(args.export[1], 'w') as file: 
        file.write(json_data)

def importJSON(args):
    print("import")
    c = "mongodb+srv://Roxanne1225:SanToria0515@cluster0.vgct4.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    dataCollectionType = args.importJSON[0]
    if(dataCollectionType != 'book' and dataCollectionType != 'author'):
        print("Error: no collection named " + dataCollectionType + ", please enter 'book' or 'author' ")
        return
    datacollection = DataCollection(c, 'goodReads', dataCollectionType)

    with open('book_data.json') as file: 
        file_data = json.load(file) 
    print(file_data[0])
    for entry in file_data:
        # print(entry)
        if("_id" in entry):
            del entry["_id"]
        if(not datacollection.documentAlreadyExist(entry)):
            print("here")
            datacollection.pushToCollection(entry)

def scrape(args):
    print(args.scrape[0])


def main(): 
# create parser object 
    parser = argparse.ArgumentParser(description = "Web scraper for goodReads")
    parser.add_argument("-s", "--scrape", type = str, nargs = 1, 
                        metavar = "boo_or_author", default = None, 
                        help = "scrape data") 
    parser.add_argument("-e", "--export", type = str, nargs = 2, 
                        metavar = ('book_or_author','path'), default = None, 
                        help = "export data to json file") 
    parser.add_argument("-i", "--importJSON", type = str, nargs = 2, 
                        metavar = ('book_or_author','path'), default = None, 
                        help = "import data from json") 


    args = parser.parse_args() 
      
    if args.scrape != None: 
        scrape(args) 
    if args.export != None:
        export(args)
    if args.importJSON != None:
        importJSON(args)





if __name__ == "__main__": 
    main() 