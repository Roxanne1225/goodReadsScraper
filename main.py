from dataCollection import DataCollection
from bookScraper import BookScraper

def main():
    # TEMP_START_URL = "/Users/user/Desktop/testparser.htm"
    TEMP_START_URL = "https://www.goodreads.com/book/show/53175355-many-points-of-me"
    c = "mongodb+srv://Roxanne1225:SanToria0515@cluster0.vgct4.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    dataCollection = DataCollection(c, "goodReads", "book")
    bookScraper = BookScraper(TEMP_START_URL, dataCollection, 1)
    dataCollection.emptyDataCollection()
    # bookScraper.scrape_one_book(TEMP_START_URL)
    bookScraper.scrapeBooks(TEMP_START_URL, 1)
    # test = {"hi":2}
    # dataCollection.pushToCollection(test)

if __name__ == "__main__":
    main()