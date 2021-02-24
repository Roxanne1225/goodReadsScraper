import requests
from bs4 import BeautifulSoup 
import re

HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'}
BASE_URL = "https://www.goodreads.com/"
TEMP_START_URL = "https://www.goodreads.com/book/show/53175355-many-points-of-me"


bookURLs = []
bookTitles = []
bookIDs = []
bookISBNS = []
bookAuthorURLs = []
bookAuthorNames = []
bookRatings = []
bookRatingCounts = []
bookReviewCounts = []
bookImages = []
bookSimilarBooks = []

def scrapeBook():
    header = HEADERS
    url = TEMP_START_URL
    r = requests.get(url, headers = header)
    soup = BeautifulSoup(r.content, 'html5lib') 
    soupbody = soup.body

    # get book url
    bookURL = url
    bookURLs.append(bookURL)

    #  get book title
    bookTitle = soupbody.find('h1', attrs={'id':'bookTitle'}).text.strip()
    bookTitles.append(bookTitle)
    # print(bookurl)

    # get book id
    reg = 'https://www.goodreads.com/book/show/([0-9]+)'
    bookID = re.search(reg, url).group(1)
    bookIDs.append(bookID)
    
    # get book ISBN
    bookDataBox = soupbody.find('div', attrs={'id':'bookDataBox'})
    all_float_divs = bookDataBox.find_all('div', attrs = {'class' : 'clearFloats'})
    bookISBN = ''
    for div in all_float_divs:
        title = div.find('div', attrs = {'class':'infoBoxRowTitle'}).text.strip()
        if title == 'ISBN':
            bookISBN = div.find('div', attrs = {'class':'infoBoxRowItem'}).contents[0].strip()
    
    # get book author url and author name
    authorName_container = soupbody.find('div', attrs = {'class':"authorName__container"})
    all_authors = authorName_container.find_all('a', href = True, attrs = {'class':"authorName"})
    cur_authorURL = []
    cur_authorName = []
    for author in all_authors:
        cur_authorURL.append(author['href'])
        name = author.find('span', attrs = {'itemprop':'name'}).text.strip()
        cur_authorName.append(name)
    bookAuthorURLs.append(cur_authorURL)
    bookAuthorNames.append(cur_authorName)
    # get book rating and review
    bookMeta = soupbody.find('div', attrs = {'id':'bookMeta'})
    rating = bookMeta.find('span', attrs = {'itemprop':'ratingValue'}).text.strip()
    bookRatings.append(rating)
    print(rating)

    bookRatingCount = bookMeta.find('meta', attrs = {'itemprop':'ratingCount'})['content']
    bookRatingCounts.append(bookRatingCount)

    bookReviewCount = bookMeta.find('meta', attrs = {'itemprop':'reviewCount'})['content']
    bookReviewCounts.append(bookReviewCount)
    # get book image
    imageTag = soupbody.find('img', attrs = {'id':'coverImage'})
    imageSrc = imageTag['src']
    bookImages.append(imageSrc)
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
        relatedBooks.append(link)
    bookSimilarBooks.append(relatedBooks)
    print(bookSimilarBooks)

scrapeBook()