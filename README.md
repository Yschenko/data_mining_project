
# Data mining project

scraper is a python code to scrape web page, and write the data to csv file.

In this time we scrape page from Ebay, with electric guitars to bay.

The data that we collected this the scraper stored in MySQL database. sql_writer.py is the code that store the data in the DB. 

## Installations

All needed installations are showed in requirements.txt file that added to this project.

The main package to install is bs4
Also install requests to download the page from the Internet.

The built-in packages csv and os are also in use, mike sure you have them.

  pip install bs4
  pip install requests
  
for store the data in sql database the followed libs are needed: pandas, pymysql.cursors
 
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
			
## DataBase Documentation

The database related to this project called 'guitars'. It's contains 3 tables: guitars, sellers, shipping.

description of guitars:
- guitar_id INT PK: the index of this columns, not relay use for anything, just makes order.
- ebay_id CHAR(20): the ebay identifier.
- title TEXT: the name of the guitar.
- price FLOAT: guitar's price, in ISL.
- brand TEXT: guitar's firm.
- string_configuration INT: number of strings in the guitar.
- model_year INT: year of the guitar model.
- shipping INT: FK to the 'shipping' table.
- seller INT: FK to the 'sellers' table.

description of shipping:
- shipping_id INT  PK: id of the shipping conditions, refers to guitars.shipping.
- coast FLOAT: the shipping coast, in ISL.
- item_location TEXT: location where in guitar will send from.
- shipping_to TEXT: list of the areas in the world that the guitar can be send to. 
- delivery TEXT: time that the guitar will arrive to the costumer.

description of sellers:
- seller_id INT PK: id of the seller, refers to guitars.seller
- name TEXT: name of the seller in ebay.
- positive_feedback FLOAT: % of positive feedback from all feedback of the seller.
- member_since TEXT: the date the seller started to sell in ebay.
- location TEXT: sellere's location.
- items_for_sell INT: number of items that in the seller's shop.

![Data Base Diagram](https://github.com/Yschenko/data_mining_project/blob/main/ERD_database_dm_project.png)


## credits

Dor Hirts,
Yehuda Shvut
