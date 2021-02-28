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
        """[summary]

        Args:
            book_data ([type]): [description]
        """
        if 'url' in book_data:
            if not self.url_already_exist(book_data['url']):
                self.collection.insert_one(book_data)

    def get_collection(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self.collection

    def empty_data_collection(self):
        """[summary]
        """
        self.collection.delete_many({})
        # self.create_collection()

    def url_already_exist(self, url):
        """[summary]

        Args:
            url ([type]): [description]

        Returns:
            [type]: [description]
        """
        query = {"url": url}
        return self.collection.count_documents(query) != 0

    def get_all_entries(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self.collection.find()

    def document_already_exist(self, document):
        """[summary]

        Args:
            document ([type]): [description]

        Returns:
            [type]: [description]
        """
        return self.collection.count_documents(document)

    def get_collection_size(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self.collection.count_documents({})
