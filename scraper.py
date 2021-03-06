import csv
import json
from bs4 import BeautifulSoup
import requests
from sys import argv
import argparse
import sql_writer

CONSTS = json.load(open('config.json', 'r'))

# This code scrape internet page, search for relevant data and write tha data to a scv file.
# There is option to print the data to the screen instead write it to csv file.


class Scraper:
    """
    this class scrap data of electric guitars from ebay. it collects data of the guitar it self and of the seller.
    there are 3 important methods in this class. first 'get_urls' that finds the urls of the pagers to scrap.
    the second is 'write_to_csv_guitar' that collects the data of each guitar, and write it to csv file.
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
        create the csv file to write the data into them. Add the first line of each file.
        """
        for name, l in zip(self._csv_path.keys(), self._columns_dict.keys()):
            with open(self._csv_path[name], 'w', encoding="utf-8") as csv_file:
                csv_writer = csv.writer(csv_file)
                # create the columns titles
                csv_writer.writerow([column for column in self._columns_dict[l].keys()])

    @staticmethod
    def make_soup(url):
        """
        with requests and BeautifulSoup, create the html data to scan.
        :param url: url to make a soup
        :return: BeautifulSoup
        """
        source = requests.get(url).text
        return BeautifulSoup(source, 'lxml')

    @staticmethod
    def find_details(details, string):
        """
        find data from the detailed page of guitar. the data appears as string (text), so strings methods are in use.
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
            self.write_to_csvs(data_for_url)

    @staticmethod
    def write_csv(data, path, mode='a', encoding="utf-8"):
        """

        :param data:
        :param path:
        :param mode:
        :param encoding:
        :return:
        """
        with open(path, mode, encoding=encoding) as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(data)

    def get_sellers_data(self, url):
        """
        get url from 'write_to_csv_guitar' and collect the data of the seller. return the seller's data as list to
        'write_to_csv_guitar'
        :param url: url of the seller page
        :return: seller's details as list
        """
        soup = self.make_soup(url)
        # the data to collect:
        name = soup.find('div', class_='mbg').a.get('href').strip('http://www.ebay.com./user/')
        positive_feedback = soup.find('div', class_='perctg').text.strip('\n\t % positive feedback')
        member_since = soup.find('div', id='member_info', class_='mem_info').find('span', class_='info').text
        location = soup.find('div', id='member_info', class_='mem_info').find('span', class_='mem_loc').text
        if soup.find('div', class_='selling_info b-space2'):
            items_for_sell = soup.find('div', class_='selling_info b-space2').text
            items_for_sell = items_for_sell[items_for_sell.find('(')+1:items_for_sell.find(')')]
        else:
            items_for_sell = None
        # make a list from all data
        row_to_csv = [name, positive_feedback, member_since, location, items_for_sell]

        return row_to_csv  # return to 'write_to_csv_guitar'

    @staticmethod
    def get_shipping_data(soup):
        """
        get prepared soup from 'write_to_csv_guitar' and return list of shipping details.
        :param soup: prepared soup to scan
        """
        if (soup.find('div', class_="u-flL sh-col") and
                soup.find('div', class_="u-flL sh-col").find('span', id="convetedPriceId")):
            cost = soup.find('div', class_="u-flL sh-col").find('span', id="convetedPriceId").text.strip('ILS ')
        else:
            cost = None
        item_location = soup.find('span', itemprop="availableAtOrFrom").text if\
            soup.find('span', itemprop="availableAtOrFrom") else None
        shipping_to = soup.find('span', itemprop="areaServed").text if\
            soup.find('span', itemprop="areaServed") else None
        shipping_to = shipping_to[:shipping_to.find("|")].strip() if shipping_to else None
        delivery = soup.find('span', "vi-acc-del-range").b.text if soup.find('span', "vi-acc-del-range") else None

        row_to_csv = [cost, item_location, shipping_to, delivery]

        return row_to_csv

    def get_guitars_data(self, soup):
        """

        :param soup:
        :return:
        """
        # the data to collect
        guitar_id = soup.find('div', class_='u-flL iti-act-num itm-num-txt')
        if guitar_id:
            guitar_id = guitar_id.text
        title = soup.find('h1', class_='it-ttl', id="itemTitle")
        if title:
            title = title.text.strip('Details about  ??')
        price = soup.find('span', id="convbinPrice")
        if price:
            price = price.text.lstrip('ILS ').rstrip('(including shipping)')
        # find data from text of details.
        details = soup.find('div', class_='section').text.replace('\n', '').replace('\t', '')
        brand = self.find_details(details, 'Brand')
        string_configuration = self.find_details(details, 'String Configuration')
        model_year = self.find_details(details, 'Model Year')
        return [guitar_id, title, price, brand, string_configuration, model_year]

    def write_to_csvs(self, urls):
        """
        gets urls of guitars. write the data into the csv file.
        """
        # list to contain the data of shippings and sellers to avoid duplications.
        shipping_details = []
        sellers = []
        # collect data for guitars
        for row in urls:
            soup = self.make_soup(row.a.get('href'))
            row_to_csv = self.get_guitars_data(soup)
            # data of shipping to its own file
            shipping = self.get_shipping_data(soup)
            if shipping not in shipping_details:  # check if the row already exists
                shipping_details.append(shipping)
                shipping_num = shipping_details.index(shipping) + 1
                shipping = [shipping_num] + shipping
                self.write_csv(shipping, self._csv_path['SHIPPING_CSV'])
            else:
                shipping_num = shipping_details.index(shipping) + 1
            # sellers file
            if self.args.store_data_seller and soup.find('div', class_='mbg vi-VR-margBtm3'):  # case of store sellers
                seller_page = soup.find('div', class_='mbg vi-VR-margBtm3').a.get('href')
                seller = self.get_sellers_data(seller_page)
                if seller not in sellers:
                    sellers.append(seller)
                    seller_num = sellers.index(seller) + 1
                    seller = [seller_num] + seller
                    self.write_csv(seller, self._csv_path['SELLERS_CSV'])
                else:
                    seller_num = sellers.index(seller) + 1
            # guitars file
                row_to_csv.extend([shipping_num, seller_num])
            self.write_csv(row_to_csv, self._csv_path['GUITARS_CSV'])

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
    download the page of URL_PAGE, get the relevant data from the page, and write the data into csv file.
    then, write from the csv files to sql database.
    """
    args = get_args(arg[1:])

    # create Scraper
    scrap = Scraper(CONSTS, args)
    # test if all given parameters are correct and available
    try:
        scrap.checks()
    except NotImplementedError:
        print('Incorrect URL')
    except NotADirectoryError:
        print('directory for csv file in not exist')
    # if constants all parameters are correct.
    else:
        scrap.create_csv_files()
        scrap.get_urls()  # write to the csv files
        #  write the sql database
        db = sql_writer.SqlWrite(CONSTS)
        db.create_database(CONSTS["DATABASE"]["CREATION"])
        db.create_table(CONSTS['DATABASE']['USE'], CONSTS['TABLES']['SELLERS']['CREATION'])
        db.enter_to_sellers()
        db.create_table(CONSTS['DATABASE']['USE'], CONSTS['TABLES']['SHIPPING']['CREATION'])
        db.enter_to_shipping()
        db.create_table(CONSTS['DATABASE']['USE'], CONSTS['TABLES']['GUITARS']['CREATION'])
        db.enter_to_guitars()


if __name__ == '__main__':
    main(argv)
