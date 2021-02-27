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
        self.testDB.emptyDataCollection()
        test = {"url":1, "test":2}
        self.testDB.pushToCollection(test)
        self.assertEqual(True, self.testDB.documentAlreadyExist(test))
    
    def testEmptyDataCollection(self):
        self.testDB.emptyDataCollection()
        self.assertEqual(0, self.testDB.getSizeOfCollection())
    
    def testGetSizeOfCollection(self):
        self.testDB.emptyDataCollection()
        test1 = {"url":3, "test":2}
        test2 = {"url":1, "test":1}
        self.testDB.pushToCollection(test1)
        self.testDB.pushToCollection(test2)
        self.assertEqual(2, self.testDB.getSizeOfCollection())


if __name__ == '__main__':
    unittest.main()