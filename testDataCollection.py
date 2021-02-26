import unittest
from dataCollection import DataCollection


class TestDataCollection(unittest.TestCase):
    def testPushToCollection(self):
        TEMP_START_URL = "https://www.goodreads.com/book/show/53175355-many-points-of-me"
        c = "mongodb+srv://Roxanne1225:SanToria0515@cluster0.vgct4.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        dataCollection = DataCollection(c, "goodReads", "book")
        test = {"test":1, "url":"kk"}
        result = dataCollection.pushToCollection(test)


if __name__ == '__main__':
    unittest.main()