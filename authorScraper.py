import requests
from bs4 import BeautifulSoup 
import re
from dataCollection import DataCollection
import os
from dotenv import load_dotenv

class AuthorScraper:
    def __init__(self, dataCollection): 
        self.headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'}
        self.dataCollection = dataCollection
        # TODO: remove drop after design
        # self.dataCollection.emptyDataCollection()
        self.urlToExplore = set()

    def getAuthorBooks(self, book_list_url):
        r = requests.get(book_list_url, headers = self.headers).content
        soup = BeautifulSoup(r, 'html5lib') 
        soupbody = soup.body
        books = []
        left_container = soupbody.find('div', attrs={'class':'leftContainer'})
        table = left_container.find('tbody')

        for subrow in table.find_all('tr'):
            link = subrow.find('a', attrs={'class':'bookTitle'})['href']
            books.append(link)
        return books
    
    def getRelatedAuthors(self, related_author_url):
        r = requests.get(related_author_url, headers = self.headers).content
        soup = BeautifulSoup(r, 'html5lib') 
        soupbody = soup.body
        authors = []
        containers = soupbody.find_all('div', attrs={'data-react-class':'ReactComponents.SimilarAuthorsList'})
        for container in containers:
            for similar_author in container.find_all('div', attrs={'class':'listWithDividers__item'}):
                link = similar_author.find('a')['href']
                authors.append(link)
        return authors

    
    def scrape_one_author(self, url):
        print("scrape one called")
        if(url in self.urlToExplore):
            self.urlToExplore.remove(url)
        r = requests.get(url, headers = self.headers).content
        # r = open(url, encoding="utf8")   
        soup = BeautifulSoup(r, 'html5lib') 
        soupbody = soup.body

        authorData = {}
        # get book url
        authorURL = url
        authorData["url"] = authorURL

        #  get author name
        container_of_name = soupbody.find('div', attrs={'class':'rightContainer'})
        author_name = container_of_name.find('h1', attrs={'class':'authorName'}).find('span').text.strip()
        authorData["author_name"] = author_name

        # get author id
        reg = 'https://www.goodreads.com/author/show/([0-9]+)'
        authorID = re.search(reg, url).group(1)
        authorData["authorID"] = authorID

        # get author books
        book_list_url = 'https://www.goodreads.com/author/list/' + authorID
        author_books = self.getAuthorBooks(book_list_url)
        authorData["author_books"] = author_books

        # get author rating and review
        anchor = soupbody.find('a', attrs={'class':'js-ratingDistTooltip'}, text=re.compile('(^ *)avg rating:'))
        reg = 'avg rating:([0-9, .]+)'
        if(anchor):
            rating = re.search(reg, anchor.text).group(1)
            authorData["rating"] = rating

        anchor = soupbody.find('a', text=re.compile('(^ *[0-9]+) ratings'))
        if(anchor):
            reg = '(^ *[0-9]+) ratings'
            num_ratings = re.search(reg, anchor.text).group(1)
            authorData["rating_count"] = num_ratings

        anchor = soupbody.find('a', text=re.compile('(^ *[0-9]+) reviews'))
        if(anchor):
            reg = '(^ *[0-9]+) reviews'
            num_reviews = re.search(reg, anchor.text).group(1)
            authorData["review_count"] = num_reviews

        # get author image
        imageTag = soupbody.find('img', attrs = {'alt':author_name})
        imageSrc = imageTag['src']
        authorData["authorImage"] = imageSrc

        # get related authors
        related_authors_url = 'https://www.goodreads.com/author/similar/' + authorID
        
        similars = self.getRelatedAuthors(related_authors_url)
        authorData["similar_authors"] = similars
        for author in similars:
            self.urlToExplore.add(author)

        
        self.dataCollection.pushToCollection(authorData)

    def scrapeAuthors(self, start_url, target_number):
        next_url = start_url
        self.scrape_one_author(next_url)
        
        i = 0
        while i < target_number:
            if(not self.dataCollection.urlAlreadyExist(next_url)):
                self.scrape_one_author(next_url)
                i+=1                
            next_url = self.urlToExplore.pop()
