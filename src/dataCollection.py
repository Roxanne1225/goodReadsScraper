"""The Data Collection class
This script provide functions to interact with the database

"""
import pymongo

class DataCollection():
    """The Data Collection class
    """
    def __init__(self, connection_string, database_name, collection_name):
        self.database_name = database_name
        self.collection_name = collection_name
        self.connection_string = connection_string
        # connect to database
        self.client = pymongo.MongoClient(self.connection_string)
        self.database = self.client[self.database_name]
        self.collection = self.database[self.collection_name]
        # self.collection.create_index("book_id", unique=True)

    def push_to_collection(self, book_data):
        """Add an entry to database

        Args:
            book_data (dictionary): information of a book
        """
        if 'url' in book_data:
            if not self.url_already_exist(book_data['url']):
                self.collection.insert_one(book_data)

    def get_collection(self):
        """Get collection name of DataCollection

        Returns:
            str: Collection name
        """
        return self.collection

    def empty_data_collection(self):
        """Empty a data collection in the remote database
        """
        self.collection.delete_many({})
        # self.create_collection()

    def url_already_exist(self, url):
        """Check if an url of a book/author is already in the database

        Args:
            url (str): url

        Returns:
            Boolean: True if already exist, false otherwise
        """
        query = {"url": url}
        return self.collection.count_documents(query) != 0

    def get_all_entries(self):
        """Get all data in the database

        Returns:
            [Dictionary]: A list of dictionaries containing all information
                          in the database
        """
        return self.collection.find()

    def document_already_exist(self, document):
        """Check if an entry is already in the database

        Args:
            document (dictionary): A dictionary containing information of a book/author

        Returns:
            Boolean: True if document already exist, false otherwise
        """
        return self.collection.count_documents(document)

    def get_collection_size(self):
        """Get the number of documents in the database

        Returns:
            int : The size of database
        """
        return self.collection.count_documents({})

    def find_by_id(self, id):
        if(self.collection_name == 'book'):
            return self.collection.find_one({'book_id':id})
        if(self.collection_name == 'author'):
            return self.collection.find_one({'authorID':id})
    
    def find_by_query(self, query):
        return self.collection.find(query)
