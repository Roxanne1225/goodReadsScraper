import pymongo

class DataCollection():
    def __init__(self, connection_string, database_name, collection_name):
        self.database_name = database_name
        self.collection_name = collection_name
        self.connection_string = connection_string
        # connect to database
        self.client = pymongo.MongoClient(self.connection_string)
        self.db = self.client[self.database_name]
        self.collection = self.db[self.collection_name]
        # self.collection.create_index("bookID", unique=True)
    
    def create_collection(self):
        self.db = self.client[self.database_name]
        self.collection = self.db[self.collection_name]

    def pushToCollection(self, bookData):
        # result = self.collection.update(bookData, bookData, upsert = True)
        # return result['nUpserted']
        if('url' in bookData):
            if(not self.urlAlreadyExist(bookData['url'])):
                self.collection.insert(bookData)
            # # self.collection.update(bookData, bookData, upsert=True)

    def getCollection(self):
        return self.collection
    
    def emptyDataCollection(self):
        self.collection.remove({})
        # self.create_collection()

    def urlAlreadyExist(self, url):
        query = {"url": url}
        return (self.collection.find(query).count() != 0)
    
    def getAllEntry(self):
        return self.collection.find()

    def documentAlreadyExist(self, document):
        return (self.collection.find(document).count()!=0)
