# Web Scraper for GoodReads

Roxanne Chen's Spring 2021 CS242 Course Assignment 2. A simple web scraper.

## Table of Contents
- [Requirements](https://gitlab.engr.illinois.edu/pc7/sp21-cs242-assignment1/-/tree/assignment-1.0#requirements)
- [Usage]

## Requirements
Make sure you have the following installed in your device to run scraper.
- [Python3](https://www.python.org/downloads/)
- Pymongo
- Beautiful Soup
- html5lib
- requests

## Command Line Interface Usage
In terminal: 
- Navigate into the cs242-assignmen2 directory
- Run ```main.py``` with parameters
#### For usage and help content, pass in the -h parameter
``` 
python3 main.py -h 
```

#### To scrape book or author data, pass in the -s or --scrape parameter
```
python3 main.py -s <book/author> <start_url> <target number> 
python3 main.py --scrape <book/author> <start_url> <target number> 
```
For example, to scrape 20 books from goodreads with the starting url of "https://www.goodreads.com/book/show/6185", run:
```
python3 main.py -s book "https://www.goodreads.com/book/show/6185" 20
```

#### To export book or author data in the database into a local json file, pass in the -e or --export parameter
```
python3 main.py -e <book/author> <path>
```
For example, to export all author information in the database to a local file name 'author.json', run:
```
python3 main.py -e author author.json
```

#### To import book or author information in a local json file to the database, pass in the -i or --importJSON parameter
```
python3 main.py -i <book/author> <path>
```

#### To clear the book or author database, pass in the --clear parameter
```
python3 main.py --clear <book/author>
```
