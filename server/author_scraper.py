"""The Author Scraper class
This script provide functions to scrape authors from the goodreads website

This can be imported and contains the following functions:
    * scrape_one_author - scrapes one url and put scraped information into
                        the database
    * scrape_authors - scrapes multiple authors and put information into
                     the database
"""

import os
import re
import time
import random
import requests
from bs4 import BeautifulSoup
from dataCollection import DataCollection
from dotenv import load_dotenv

HEADERS = os.getenv('HEADERS')
class AuthorScraper:
    """The Author Scraper class
    """
    def __init__(self, data_collection):
        self.headers = {'user-agent': HEADERS}
        self.data_collection = data_collection
        self.url_to_explore = set()

    def get_author_books(self, book_list_url):
        """Get the books written by author

        Args:
            book_list_url (str): url pointing to the page of books of author

        Returns:
            [str]: a list of urls of books
        """
        req = requests.get(book_list_url, headers = self.headers).content
        soup = BeautifulSoup(req, 'html5lib')
        soupbody = soup.body
        books = []
        left_container = soupbody.find('div', attrs={'class':'leftContainer'})
        if left_container:
            table = left_container.find('tbody')
            if table:
                for subrow in table.find_all('tr'):
                    link = subrow.find('a', attrs={'class':'bookTitle'})['href']
                    books.append(link)
        return books

    def get_related_authors(self, related_author_url):
        """Get a list of related authors

        Args:
            related_author_url (str): url point to the page of related authors

        Returns:
            [str]: a list of urls of authors
        """
        req = requests.get(related_author_url, headers = self.headers).content
        soup = BeautifulSoup(req, 'html5lib')
        soupbody = soup.body
        authors = []
        containers = soupbody.find_all('div',
         attrs={'data-react-class':'ReactComponents.SimilarAuthorsList'})
        if containers:
            for container in containers:
                for similar_author in container.find_all('div',
                 attrs={'class':'listWithDividers__item'}):
                    link = similar_author.find('a')['href']
                    authors.append(link)
        return authors

    def scrape_one_author(self, url):
        """Scrape the give url point to an author

        Args:
            url (str): The url to scrape
        """
        if url in self.url_to_explore:
            self.url_to_explore.remove(url)
        req = requests.get(url, headers = self.headers).content
        soup = BeautifulSoup(req, 'html5lib')
        soupbody = soup.body

        authorData = {}
        # get book url
        authorURL = url
        authorData["url"] = authorURL

        #  get author name
        container_of_name = soupbody.find('div',
         attrs={'class':'rightContainer'})
        if container_of_name:
            author_name_h1 = container_of_name.find('h1',
             attrs={'class':'authorName'})
            if author_name_h1:
                author_name = author_name_h1.find('span').text.strip()
                authorData["author_name"] = author_name

        # get author id
        reg = 'https://www.goodreads.com/author/show/([0-9]+)'
        authorID = re.search(reg, url).group(1)
        authorData["id"] = authorID

        # get author books
        book_list_url = 'https://www.goodreads.com/author/list/' + authorID
        author_books = self.get_author_books(book_list_url)
        authorData["author_books"] = author_books

        # get author rating and review
        anchor = soupbody.find('a',
         attrs={'class':'js-ratingDistTooltip'}, text=re.compile('(^ *)avg rating:'))
        reg = 'avg rating:([0-9, .]+)'
        if anchor:
            rating = re.search(reg, anchor.text).group(1)
            authorData["rating"] = rating

        anchor = soupbody.find('a', text=re.compile('(^ *[0-9]+) ratings'))
        if anchor:
            reg = '(^ *[0-9]+) ratings'
            num_ratings = re.search(reg, anchor.text).group(1)
            authorData["rating_count"] = num_ratings

        anchor = soupbody.find('a', text=re.compile('(^ *[0-9]+) reviews'))
        if anchor:
            reg = '(^ *[0-9]+) reviews'
            num_reviews = re.search(reg, anchor.text).group(1)
            authorData["review_count"] = num_reviews

        # get author image
        image_tag = soupbody.find('img', attrs = {'alt':author_name})
        if image_tag:
            image_src = image_tag['src']
            authorData["authorImage"] = image_src

        # get related authors
        related_authors_url = 'https://www.goodreads.com/author/similar/' + authorID

        similars = self.get_related_authors(related_authors_url)
        authorData["similar_authors"] = similars
        for author in similars:
            self.url_to_explore.add(author)

        self.data_collection.push_to_collection(authorData)
        print("Author successfully scraped: " + author_name)

    def scrapeAuthors(self, start_url, target_number):
        next_url = start_url
        self.scrape_one_author(next_url)

        i = 0
        while i < target_number-1:
            if not self.data_collection.url_already_exist(next_url):
                interval = random.randint(2, 12)
                print("sleeping for " + str(interval) + " seconds")
                time.sleep(interval)
                self.scrape_one_author(next_url)
                i+=1
            next_url = self.url_to_explore.pop()
