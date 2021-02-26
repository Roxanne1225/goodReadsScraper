from dataCollection import DataCollection
from bookScraper import BookScraper
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_CONNECTION_STRING = os.getenv('MONGO_CONNECTION_STRING')
def main():
    # TEMP_START_URL = "/Users/user/Desktop/testparser.htm"
    TEMP_START_URL = "https://www.goodreads.com/book/show/53175355-many-points-of-me"
    c = MONGO_CONNECTION_STRING
    dataCollection = DataCollection(c, "goodReads", "book")
    bookScraper = BookScraper(TEMP_START_URL, dataCollection, 1)
    # dataCollection.emptyDataCollection()
    # bookScraper.scrape_one_book(TEMP_START_URL)
    # bookScraper.scrapeBooks(TEMP_START_URL, 1)
    # test = {"hi":2}
    # dataCollection.pushToCollection(test)

if __name__ == "__main__":
    main()