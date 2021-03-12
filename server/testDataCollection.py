import unittest
from dataCollection import DataCollection
import os 
from dotenv import load_dotenv
load_dotenv()

class TestDataCollection(unittest.TestCase):
    def setUp(self):
        self.start_url = "https://www.goodreads.com/book/show/53175355-many-points-of-me"
        self.connection_string = os.getenv('MONGO_CONNECTION_STRING')
        self.testDB = DataCollection(self.connection_string, "testDatabase", "testCollection")
        

    def testPushToBookCollection(self):
        self.testDB.empty_data_collection()
        test = {"url":1, "test":2}
        self.testDB.push_to_collection(test)
        self.assertEqual(True, self.testDB.document_already_exist(test))
    
    def testempty_data_collection(self):
        self.testDB.empty_data_collection()
        self.assertEqual(0, self.testDB.get_collection_size())
    
    def testget_collection_size(self):
        self.testDB.empty_data_collection()
        test1 = {"url":3, "test":2}
        test2 = {"url":1, "test":1}
        self.testDB.push_to_collection(test1)
        self.testDB.push_to_collection(test2)
        self.assertEqual(2, self.testDB.get_collection_size())

    def testdocument_already_exist(self):
        self.testDB.empty_data_collection()
        test1 = {"url":3, "test":2}
        test2 = {"url":1, "test":1}
        self.testDB.push_to_collection(test1)
        self.assertEqual(True, self.testDB.document_already_exist(test1))
        self.assertEqual(False, self.testDB.document_already_exist(test2))


if __name__ == '__main__':
    unittest.main()