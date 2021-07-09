import csv
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

    """
    def __init__(self, consts):
        """

        :param consts:
        """
        self._url_page = consts['URL_PAGE']
        self._csv_path = consts['CSV_PATH']
        self._columns_dict = consts['COLUMNS_DICT']
        self._num_pages = consts['NUM_PAGES']

    def create_csv_files(self):
        """

        :return:
        """
        for name, l in zip(self._csv_path.keys(), self._columns_dict.keys()):
            with open(self._csv_path[name], 'w', encoding="utf-8") as csv_file:
                csv_writer = csv.writer(csv_file)
                # create the columns titles
                print(self._columns_dict[l].keys())
                csv_writer.writerow([column for column in self._columns_dict[l].keys()])

    def make_soup(self, url):
        """

        :param url:
        :return:
        """
        source = requests.get(url).text

        # create BeautifulSoup from the page
        return BeautifulSoup(source, 'lxml')

    def find_details(self, details, string):
        """

        :param details:
        :param string:
        :return:
        """
        if details.find(string) != -1:
            return details[details.find(string) + len(string + ': '):
                           details.find(' ', details.find(string) + len(string + ': '))].lower()
        else:
            return None


    def get_urls(self):
        """

        :return:
        """
        data_for_url = []
        for page_num in range(1, self._num_pages):
            print(page_num)

            soup = self.make_soup(self._url_page + f"?rt=nc&_dmd=2&_pgn={page_num}")

            # collect the data from the page
            data_for_url = (soup.find_all('div', class_='s-item__wrapper clearfix'))
            self.write_to_csv_guitar(data_for_url[::2]) # any 'div' of find_all in the last line appears twice, so I take only 1.

    def write_to_sellers_csv(self, url):
        """

        :param url:
        :return:
        """
        soup = self.make_soup(url)
        name = soup.find('div', class_='mbg').a.get('href').strip('http://www.ebay.com./user/')
        positive_feedback = soup.find('div', class_='perctg').text.strip('\n\t % positive feedback')
        member_since = soup.find('div', id='member_info', class_='mem_info').find('span', class_='info').text
        location = soup.find('div', id='member_info', class_='mem_info').find('span', class_='mem_loc').text
        items_for_sell = soup.find('div', class_='selling_info b-space2').text
        items_for_sell = items_for_sell[items_for_sell.find('(')+1:items_for_sell.find(')')]

        row_to_csv = [name, positive_feedback, member_since, location, items_for_sell]
        print(row_to_csv)

        with open(self._csv_path['sellers_csv'], 'a', encoding="utf-8") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(row_to_csv)

        return row_to_csv[0]

    def write_to_csv_guitar(self, urls):
        """
        gets csv_path and list of data on guitars. write the data into the csv file.
        """
        # writing the data into the file
        for row in urls:

            soup = self.make_soup(row.a.get('href'))

            id = soup.find('div', class_='u-flL iti-act-num itm-num-txt')
            if id:
                id = id.text
            title = soup.find('h1', class_='it-ttl', id="itemTitle")
            if title:
                title = title.text.strip('Details about   ')
            price = soup.find('span', id="convbinPrice")
            if price:
                price = price.text.lstrip('ILS ').rstrip('(including shipping)')
            details = soup.find('div', class_='section').text.replace('\n', '').replace('\t', '')

            brand = self.find_details(details, 'Brand')
            string_configuration = self.find_details(details, 'String Configuration')
            model_year = self.find_details(details, 'Model Year')
            if soup.find('div', class_='mbg vi-VR-margBtm3'):
                seller_page = soup.find('div', class_='mbg vi-VR-margBtm3').a.get('href')
                seller = self.write_to_sellers_csv(seller_page)
            else:
                continue

            row_to_csv = [id, title, price, brand, string_configuration, model_year, seller]
            print(row_to_csv)
            with open(self._csv_path['goitars_csv'], 'a', encoding="utf-8") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(row_to_csv)

    def checks(self):
        """

        :return:
        """
        if not requests.head(self._url_page).status_code:
            raise NotImplementedError('incorrect url.')





def main():
    """
    download the page of URL_PAGE, get the relevant data from the page, and write the data into csv file
    """

    # create Scraper
    scrap = Scraper(CONFIG_DICT)

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
    main()

