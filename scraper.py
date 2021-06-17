import csv
from bs4 import BeautifulSoup
import requests
import os


# This code scrape internet page, search for relevant data and write tha data to a scv file.
# There is option to print the data to the screen instead write it to csv file.


URL_PAGE = 'https://il.ebay.com/b/Electric-Guitars/33034/bn_2312182'
CSV_PATH = 'ebay_guitars_scrape.csv'
COLUMNS_DICT = {'image': 's-item__image-img', 'title': 's-item__title', 'price': 's-item__price'}


def tests():
    if not requests.head(URL_PAGE).status_code:
        raise NotImplementedError('incorrect url.')
    if not os.path.isdir(CSV_PATH):
        NotADirectoryError('directory for csv file in not exist')


def write_to_csv_file(csv_path, data_rows):
    """
    gets csv_path and list of data on guitars. write the data into the csv file.
    """
    csv_file = open(csv_path, 'w', encoding="utf-8")
    csv_writer = csv.writer(csv_file)

    # create the columns title
    csv_writer.writerow([column for column in COLUMNS_DICT.keys()])

    # writing the data into the file
    for row in data_rows:
        # collect the data defined in COLUMNS_DICT to 'row_to_csv' list and write the list into the csv file.
        row_to_csv = []
        for item in COLUMNS_DICT:
            # case of img
            if COLUMNS_DICT[item].endswith('img'):
                row_to_csv.append(row.find(class_=COLUMNS_DICT[item]).get('src'))
            # case of text
            else:
                row_to_csv.append(row.find(class_=COLUMNS_DICT[item]).text)

        # print(row_to_csv)
        csv_writer.writerow(row_to_csv)

    csv_file.close()


def main():
    """
    download the page of URL_PAGE, get the relevant data from the page, and write the data into csv file
    """
    # test if all given parameters are correct and available
    try:
        tests()

    except NotImplementedError:
        print('Incorrect URL')
    except NotADirectoryError:
        print('directory for csv file in not exist')

    # if constants all parameters are correct.
    else:
        # download the page
        source = requests.get(URL_PAGE).text

        # create BeautifulSoup from the page
        soup = BeautifulSoup(source, 'html')  # 'lxml')

        # collect the data from the page
        data_for_url = soup.find_all('div', class_='s-item__wrapper clearfix')
        # print(guitars.prettify())

        # write the data into csv file
        write_to_csv_file(CSV_PATH, data_for_url)


if __name__ == '__main__':
    main()
