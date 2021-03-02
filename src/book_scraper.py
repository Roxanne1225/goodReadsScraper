"""The Book Scraper class
This script provide functions to scrape books from the goodreads website

This can be imported and contains the following functions:
    * scrape_one_book - scrapes one url and put scraped information into
                        the database
    * scrape_books - scrapes multiple books and put information into
                     the database
"""

import re
import os
import time
import random
import requests
from bs4 import BeautifulSoup

HEADERS = os.getenv('HEADERS')
class BookScraper:
    """The BookScraper class
    """

    def __init__(self, data_collection):
        self.headers = {'user-agent': HEADERS}
        self.data_collection = data_collection
        self.url_to_explore = set()

    def scrape_one_book(self, url):
        """Scrape the give url point to a book

        Args:
            url (str): The url to scrape
        """

        if url in self.url_to_explore:
            self.url_to_explore.remove(url)
        req = requests.get(url, headers = self.headers).content
        soup = BeautifulSoup(req, 'html5lib')
        soupbody = soup.body

        book_data = {}
        # get book url
        book_url = url
        book_data["url"] = book_url

        #  get book title
        book_title = soupbody.find('h1', attrs={'id':'bookTitle'}).text.strip()
        if book_title:
            book_data["title"] = book_title

        # # get book id
        reg = 'https://www.goodreads.com/book/show/([0-9]+)'
        book_id = re.search(reg, url).group(1)
        book_data["book_id"] = book_id

        # get book ISBN
        book_databox = soupbody.find('div', attrs={'id':'bookDataBox'})
        if book_databox:
            all_float_divs = book_databox.find_all('div',
            attrs = {'class' : 'clearFloats'})
            book_isbn = ''
            for div in all_float_divs:
                title = div.find('div',
                attrs = {'class':'infoBoxRowTitle'}).text.strip()
                if title == 'ISBN':
                    book_isbn = div.find('div',
                    attrs = {'class':'infoBoxRowItem'}).contents[0].strip()
            book_data["ISBN"] = book_isbn

        # get book author url and author name
        author_name_container = soupbody.find('div',
         attrs = {'class':"authorName__container"})
        if author_name_container:
            all_authors = author_name_container.find_all('a',
             href = True, attrs = {'class':"authorName"})
            cur_author_url = []
            cur_author_name = []
            for author in all_authors:
                cur_author_url.append(author['href'])
                name = author.find('span', attrs = {'itemprop':'name'}).text.strip()
                cur_author_name.append(name)
            book_data["authorURLs"] = cur_author_url
            book_data["author_names"] = cur_author_name

        # get book rating and review
        book_meta = soupbody.find('div', attrs = {'id':'bookMeta'})
        if book_meta:
            rating = book_meta.find('span',
             attrs = {'itemprop':'ratingValue'}).text.strip()
            book_data["rating"] = rating

        book_rating_count_container = book_meta.find('meta',
         attrs = {'itemprop':'ratingCount'})
        if book_rating_count_container:
            book_rating_count = book_rating_count_container['content']
            book_data["rating_count"] = book_rating_count

        book_review_count_container = book_meta.find('meta',
         attrs = {'itemprop':'reviewCount'})
        if book_review_count_container:
            book_review_count = book_review_count_container['content']
            book_data["review_count"] = book_review_count

        # get book image
        image_tag = soupbody.find('img', attrs = {'id':'coverImage'})
        if image_tag:
            image_src = image_tag['src']
            book_data["bookImage"] = image_src
        # print(authorLink.span.text)

        # get related_books
        related_works_container = soupbody.find('div', id=re.compile('relatedWorks-'))
        if related_works_container:
            related_books_div = related_works_container.find('div', class_='bigBoxBody')
            if related_books_div:
                related_books_carousel = related_books_div.find('div', class_='bookCarousel')
                if related_books_carousel:
                    carousel_row = related_books_carousel.find('div', class_='carouselRow')
                    if carousel_row:
                        related_books_list_li = carousel_row.find('ul').find_all('li')
                        related_books = []
                        for item in related_books_list_li:
                            link = item.find('a', href = True)['href']
                            self.url_to_explore.add(link)
                            related_books.append(link)
                        book_data["similar_books"] = related_books

        self.data_collection.push_to_collection(book_data)
        print("Book successfully scraped: " + book_title)

    def scrapeBooks(self, start_url, target_number):
        """Scrape multiple books starting from the given url

        Args:
            start_url (str): The url to start scraping from
            target_number (int): number of books to scrape
        """
        next_url = start_url
        self.scrape_one_book(next_url)

        i = 0
        while i < target_number-1:
            if not self.data_collection.url_already_exist(next_url):
                interval = random.randint(2, 12)
                print("sleeping for " + str(interval) + " seconds")
                time.sleep(interval)
                self.scrape_one_book(next_url)
                i+=1
            next_url = self.url_to_explore.pop()
