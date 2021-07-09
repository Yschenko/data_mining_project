import csv
import json
from bs4 import BeautifulSoup
import lxml
import requests
import os
from sys import argv
import argparse

# This code scrape internet page, search for relevant data and write tha data to a scv file.
# There is option to print the data to the screen instead write it to csv file.

CONFIG_DICT = {'URL_PAGE': 'https://il.ebay.com/b/Electric-Guitars/33034/bn_2312182',
               'NUM_PAGES': 30,
               'CSV_PATH': {'goitars_csv': 'ebay_guitars_scrape.csv', 'sellers_csv': 'ebay_sellers_guitars_scrape.csv'},
               'COLUMNS_DICT': {'guitars': {'id': 'u-flL iti-act-num itm-num-txt', 'title': 'it-ttl',
                                            'price': 'mainPrice','brand': '', 'string_configuration': '',
                                            'model_year': '', 'seller': ''},
                                'sellers': {'name': '', 'positive_feedback': '', 'member_since': '', 'location': '',
                                            'items_for_sell': ''}
                                }
               }

class Scraper:
    """
    this class scrap tada of electric guitars from ebay. it collects data of the guitar it self and of the seller.
    there are 3 important methods in this class. first 'get_urls' that finds the urls of the pagers to scrap.
    the second is 'write_to_csv_guitar' that collects the data of each guitar, and erite it to csv file.
    'write_to_csv_guitar' also call 'write_to_csv_sellers' to find the seller name.
    'write_to_csv_sellers' is the third method that collects data of the seller of each guitar.
    it returns to 'write_to_csv_guitar' the name of the seller.
    """
    def __init__(self, consts, args):
        """
        initializing the method with the config data.
        """
        self._url_page = consts['URL_PAGE']
        self._csv_path = consts['CSV_PATH']
        self._columns_dict = consts['COLUMNS_DICT']
        self._num_pages = consts['NUM_PAGES']
        self.args = args

    def create_csv_files(self):
        """
        create the csv file to write the data into them.
        """
        for name, l in zip(self._csv_path.keys(), self._columns_dict.keys()):
            with open(self._csv_path[name], 'w', encoding="utf-8") as csv_file:
                csv_writer = csv.writer(csv_file)
                # create the columns titles
                print(self._columns_dict[l].keys())
                csv_writer.writerow([column for column in self._columns_dict[l].keys()])

    def make_soup(self, url):
        """
        with requests and BeautifulSoup, create the html data to scan.
        :param url: url to make a soup
        :return: BeautifulSoup
        """
        source = requests.get(url).text
        return BeautifulSoup(source, 'lxml')

    def find_details(self, details, string):
        """
        find data from the detailed page of guitar. as string (text) of data
        :param details: the string to scan
        :param string: the data to find
        :return: the data if exists, or None
        """
        if details.find(string) != -1:  # check if the data exists
            return details[details.find(string) + len(string + ': '):  # find the relevant data
                           details.find(' ', details.find(string) + len(string + ': '))].lower()
        else:
            return None

    def get_urls(self):
        """
        get url, and pass all relevant tags to the 'write' functions.
        """
        for page_num in range(1, self._num_pages):
            if self.args.p:
                print(page_num)  # just to have some information about the process.

            soup = self.make_soup(self._url_page + f"?rt=nc&_dmd=2&_pgn={page_num}")
            # collect the data from the page
            data_for_url = (soup.find_all('div', class_='s-item__wrapper clearfix'))
            # call 'write_to_csv_guitar'
            self.write_to_csv_guitar(data_for_url[::2]) # any 'div' of find_all in the last line appears twice, so I take only 1.

    def write_to_sellers_csv(self, url):
        """
        get url from 'write_to_csv_guitar' and collect the data of the seller. return the seller's name to 'write_to_csv_guitar'
        :param url: url of the seller page
        :return: seller's name
        """
        soup = self.make_soup(url)
        # the data to collect:
        name = soup.find('div', class_='mbg').a.get('href').strip('http://www.ebay.com./user/')
        positive_feedback = soup.find('div', class_='perctg').text.strip('\n\t % positive feedback')
        member_since = soup.find('div', id='member_info', class_='mem_info').find('span', class_='info').text
        location = soup.find('div', id='member_info', class_='mem_info').find('span', class_='mem_loc').text
        items_for_sell = soup.find('div', class_='selling_info b-space2').text
        items_for_sell = items_for_sell[items_for_sell.find('(')+1:items_for_sell.find(')')]
        # make a list from all data
        row_to_csv = [name, positive_feedback, member_since, location, items_for_sell]
        # write the data into the csv file
        with open(self._csv_path['SELLERS_CSV'], 'a', encoding="utf-8") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(row_to_csv)
        return row_to_csv[0]  # return to 'write_to_csv_guitar'

    def write_to_csv_guitar(self, urls):
        """
        gets urls of guitars. write the data into the csv file.
        """
        # writing the data into the file
        for row in urls:
            soup = self.make_soup(row.a.get('href'))
            # the data to collect
            id = soup.find('div', class_='u-flL iti-act-num itm-num-txt')
            if id:
                id = id.text
            title = soup.find('h1', class_='it-ttl', id="itemTitle")
            if title:
                title = title.text.strip('Details about   ')
            price = soup.find('span', id="convbinPrice")
            if price:
                price = price.text.lstrip('ILS ').rstrip('(including shipping)')
            # find data from text od details.
            details = soup.find('div', class_='section').text.replace('\n', '').replace('\t', '')
            brand = self.find_details(details, 'Brand')
            string_configuration = self.find_details(details, 'String Configuration')
            model_year = self.find_details(details, 'Model Year')
            if self.args.store_data_seller and soup.find('div', class_='mbg vi-VR-margBtm3'):  # case of store sellers data
                seller_page = soup.find('div', class_='mbg vi-VR-margBtm3').a.get('href')
                seller = self.write_to_sellers_csv(seller_page)
                row_to_csv = [id, title, price, brand, string_configuration, model_year, seller]
            elif not self.args.store_data_seller or not self.args.store_no_data_seller:  # store without sellers data
                row_to_csv = [id, title, price, brand, string_configuration, model_year]

            with open(self._csv_path['GUITARS_CSV'], 'a', encoding="utf-8") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(row_to_csv)

    def checks(self):
        """
        check if the input us valid.
        """
        if not requests.head(self._url_page).status_code:
            raise NotImplementedError('incorrect url.')


def get_args(args):
    """
    reading the arguments from the command line. first chose if to store data on sellers,
    second if if to store data of guitars with no data on sellers.
    third- '-p' optional argument, to show the process, which page is in process now.
    """
    parser = argparse.ArgumentParser(description='scraper')
    parser.add_argument('store_data_seller', type=bool, default=1,
                        help="chose if to store data of the sellers (recommended)")
    parser.add_argument('store_no_data_seller', type=bool, default=1,
                        help='''some guitars do not have info about the seller,
                        chose whether to store data of these guitars or not.''')
    parser.add_argument("-p", '--p', action="store_true", default=1,
                        help="chose if to show the process of calculations (num of row in the files).")
    return parser.parse_args(args)


def main(arg):
    """
    download the page of URL_PAGE, get the relevant data from the page, and write the data into csv file
    """
    args = get_args(arg[1:])
    consts = json.load(open('config.json', 'r'))

    # create Scraper
    scrap = Scraper(consts, args)
    # test if all given parameters are correct and available
    try:
        scrap.checks()
    except NotImplementedError:
        print('Incorrect URL')
    except NotADirectoryError:
        print('directory for csv file in not exist')
    # if constants all parameters are correct.
    else:
        scrap.get_urls()


if __name__ == '__main__':
    main(argv)

