
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
 
## usage - general
 
All information needed to run this project appears in 'config.json' file, attached to the project.

the config file includes the following information:
 - url to start scraping from it.
 - number of pages to scrap.
 - dictionary: "CSV_PATH" with 3 paths to 3 csv file that the program will write to them.
 - dictionary: "COLUMNS_DICT" contains 3 inner dictionaries with the columns names of the 3 csv files mentioned above.

## usage - command line

	There command line gets 3 arguments, 2 mandatory and 1 optional.
	arg 1: store_data_seller, chose whether to store data of sellers or just on guitars. this is a boolean argument, enter 1 or 0 to chose the relevant option.
			default = True
	arg 2: store_no_data_seller, chose whether to store data of guitars that do not have data of their seller or not. this is a boolean argument, enter 1 or 0 to chose the relevant option.
			default = True
	arg 3: '-p' optional, chose if to present info about the process, will show the number of page that scanned now.
			default = True

## credits

Dor Hirts
Yehuda Shvut
