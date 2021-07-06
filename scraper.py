import csv
from bs4 import BeautifulSoup
import lxml
import requests
import os

# This code scrape internet page, search for relevant data and write tha data to a scv file.
# There is option to print the data to the screen instead write it to csv file.

CONFIG_DICT = {'URL_PAGE': 'https://il.ebay.com/b/Electric-Guitars/33034/bn_2312182',
               'CSV_PATH': 'ebay_guitars_scrape.csv',
               'COLUMNS_DICT': {'image': 's-item__image-img', 'title': 's-item__title', 'price': 's-item__price'},
               'NUM_PAGES': 30}



class Scraper:

    def __init__(self, consts):
        self._url_page = consts['URL_PAGE']
        self._csv_path = consts['CSV_PATH']
        self._columns_dict = consts['COLUMNS_DICT']
        self._num_pages = consts['NUM_PAGES']

    def get_urls(self):
        data_for_url = []
        for page_num in range(1, self._num_pages):
            # download the page
            source = requests.get(self._url_page + f"?rt=nc&_dmd=2&_pgn={page_num}").text

            # create BeautifulSoup from the page
            soup = BeautifulSoup(source, 'lxml')

            # collect the data from the page
            data_for_url += soup.find_all('div', class_='s-item__wrapper clearfix')
        return data_for_url

    def write_to_csv_file(self, data_rows):
        """
        gets csv_path and list of data on guitars. write the data into the csv file.
        """
        csv_file = open(self._csv_path, 'w', encoding="utf-8")
        csv_writer = csv.writer(csv_file)

        # create the columns titles
        csv_writer.writerow([column for column in self._columns_dict.keys()])

        # writing the data into the file
        for row in data_rows:
            # collect the data defined in COLUMNS_DICT to 'row_to_csv' list and write the list into the csv file.
            row_to_csv = []
            for item in self._columns_dict:
                # case of img
                if self._columns_dict[item].endswith('img'):
                    row_to_csv.append(row.find(class_=self._columns_dict[item]).get('src'))
                # case of text
                else:
                    row_to_csv.append(row.find(class_=self._columns_dict[item]).text)
            # print(row_to_csv)
            csv_writer.writerow(row_to_csv)
        csv_file.close()

    def checks(self):
        if not requests.head(self._url_page).status_code:
            raise NotImplementedError('incorrect url.')
        # if not os.path.split(self._csv_path)[0]:
        #     raise NotADirectoryError('directory for csv file in not exist')


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
        data_for_url = scrap.get_urls()

        # write the data into csv file
        scrap.write_to_csv_file(data_for_url)


if __name__ == '__main__':
    main()
