import unittest
from dataCollection import DataCollection
from book_scraper import BookScraper
from author_scraper import AuthorScraper
import os 
from dotenv import load_dotenv
load_dotenv()

class TestScraper(unittest.TestCase):
    def setUp(self):
        self.testDB = DataCollection(os.getenv('MONGO_CONNECTION_STRING'), "testDatabase", "testCollection")
        self.bookScraper = BookScraper(self.testDB)
        self.authroScraper = AuthorScraper(self.testDB)
    
    def testBookScraper(self):
        self.testDB.empty_data_collection()
        testurl = "https://www.goodreads.com/book/show/6185.Wuthering_Heights"
        self.bookScraper.scrape_one_book(testurl)
        self.assertEqual(1, self.testDB.get_collection_size())

    def testAuthorScraper(self):
        self.testDB.empty_data_collection()
        testurl = "https://www.goodreads.com/author/show/6485178.Fredrik_Backman"
        self.authroScraper.scrape_one_author(testurl)
        self.assertEqual(1, self.testDB.get_collection_size())

if __name__ == '__main__':
    unittest.main()