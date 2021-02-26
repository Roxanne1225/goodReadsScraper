import requests
from bs4 import BeautifulSoup 
import re

class BookScraper:
    def __init__(self, dataCollection): 
        self.headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'}
        self.dataCollection = dataCollection
        self.urlToExplore = set()
    
    def scrape_one_book(self, url):
        if(url in self.urlToExplore):
            self.urlToExplore.remove(url)
        r = requests.get(url, headers = self.headers).content
        # r = open(url, encoding="utf8")   
        soup = BeautifulSoup(r, 'html5lib') 
        soupbody = soup.body

        bookData = {}
        # get book url
        bookURL = url
        bookData["url"] = bookURL

        #  get book title
        bookTitle = soupbody.find('h1', attrs={'id':'bookTitle'}).text.strip()
        bookData["title"] = bookTitle

        # # get book id
        reg = 'https://www.goodreads.com/book/show/([0-9]+)'
        bookID = re.search(reg, url).group(1)
        bookData["bookID"] = bookID
        
        # get book ISBN
        bookDataBox = soupbody.find('div', attrs={'id':'bookDataBox'})
        all_float_divs = bookDataBox.find_all('div', attrs = {'class' : 'clearFloats'})
        bookISBN = ''
        for div in all_float_divs:
            title = div.find('div', attrs = {'class':'infoBoxRowTitle'}).text.strip()
            if title == 'ISBN':
                bookISBN = div.find('div', attrs = {'class':'infoBoxRowItem'}).contents[0].strip()
        bookData["ISBN"] = bookISBN

        # get book author url and author name
        authorName_container = soupbody.find('div', attrs = {'class':"authorName__container"})
        all_authors = authorName_container.find_all('a', href = True, attrs = {'class':"authorName"})
        cur_authorURL = []
        cur_authorName = []
        for author in all_authors:
            cur_authorURL.append(author['href'])
            name = author.find('span', attrs = {'itemprop':'name'}).text.strip()
            cur_authorName.append(name)
        bookData["authorURLs"] = cur_authorURL
        bookData["author_names"] = cur_authorName

        # get book rating and review
        bookMeta = soupbody.find('div', attrs = {'id':'bookMeta'})
        rating = bookMeta.find('span', attrs = {'itemprop':'ratingValue'}).text.strip()
        bookData["rating"] = rating

        bookRatingCount = bookMeta.find('meta', attrs = {'itemprop':'ratingCount'})['content']
        bookData["rating_count"] = bookRatingCount

        bookReviewCount = bookMeta.find('meta', attrs = {'itemprop':'reviewCount'})['content']
        bookData["review_count"] = bookReviewCount

        # get book image
        imageTag = soupbody.find('img', attrs = {'id':'coverImage'})
        imageSrc = imageTag['src']
        bookData["bookImage"] = imageSrc
        # print(authorLink.span.text)

        # get relatedBooks
        relatedWorksContainer = soupbody.find('div', id=re.compile('relatedWorks-'))
        relatedBooksDiv = relatedWorksContainer.find('div', class_='bigBoxBody')
        relatedBooksCarousel = relatedBooksDiv.find('div', class_='bookCarousel')
        carouselRow = relatedBooksCarousel.find('div', class_='carouselRow')
        relatedBooksList_li = carouselRow.find('ul').find_all('li')
        relatedBooks = []
        for item in relatedBooksList_li:
            link = item.find('a', href = True)['href']
            self.urlToExplore.add(link)
            relatedBooks.append(link)
        bookData["similar_books"] = relatedBooks


        
        self.dataCollection.pushToCollection(bookData)

    def scrapeBooks(self, start_url, target_number):
        next_url = start_url
        self.scrape_one_book(next_url)
        
        i = 0
        while i < target_number:
            if(not self.dataCollection.urlAlreadyExist(next_url)):
                self.scrape_one_book(next_url)
                i+=1                
            next_url = self.urlToExplore.pop()
