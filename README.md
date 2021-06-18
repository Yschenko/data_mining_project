
# Data mining project

scraper is a python code to scrape web page, and write the data to csv file.

In this time we scrape page from Ebay, with electric guitars to bay. for each guitar we collects its name, price and picture.

## Installations

All needed installations are showed in requirements.txt file that added to this project.

The main package to install is bs4
Also install reuests to download the page from the Internet.

The built-in packages csv and os are also in use, mike sure you have them.

  pip install bs4
  pip install requests
 
## usage
 
	import csv
	from bs4 import BeautifulSoup
	import requests
	import os

	URL_PAGE = 'https://il.ebay.com/b/Electric-Guitars/33034/bn_2312182'
	CSV_PATH = 'ebay_guitars_scrape.csv'
	COLUMNS_DICT = {'image': 's-item__image-img', 'title': 's-item__title', 'price': 's-item__price'}


Their are 3 constants to insert in order to scrape specific web page.
The first is URL_PAGE, it is a string contains the URL address of the page the user wants to scrape.
The second in CSV_PATH, it is the path of the csv file that will contain all data that will be scraped from URL_PAGE.
Last one is COLUMNS_DICT, it is a dictionary which in its keys their are the names (strings) of the titles of the columns of the csv file,
and the values are strings, contains specific words with the relevant data to search and scrape from the page's HTML code  

## credits

Dor Hirts
Yehuda Shvut
