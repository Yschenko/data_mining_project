import csv
from bs4 import BeautifulSoup
import requests


# This code scrape internet page, search for relevant data and write tha data to a scv file.
# There is option to print the data to the screen instead write it to csv file.



URL_GUITARS = 'https://il.ebay.com/b/Electric-Guitars/33034/bn_2312182'
CSV_PATH = 'ebay_guitars_scrape.csv'
COLUMNS_NAMES = ['image', 'title', 'price']


def write_to_csv_file(csv_path, data_rows):
    """
    gets csv_path and list of data on guitars. write the data into the csv file.
    """
    csv_file = open(csv_path, 'w')
    csv_writer = csv.writer(csv_file)

    # create the columns title
    csv_writer.writerow([column for column in COLUMNS_NAMES])

    # writing the data into the file
    for row in data_rows:
        item1 = row.find(class_='s-item__image-img').get('src')
        # print(item1)

        item2 = row.find(class_='s-item__title').text
        # print(item2)

        item3 = row.find(class_='s-item__price').text
        # print(item3)

        # print()

        csv_writer.writerow([item1, item2, item3])

    csv_file.close()


def main():
    """
    download the page of URL_GUITARS, get the relevant data from the page, and write the data into csv file
    """
    # download the page
    source = requests.get(URL_GUITARS).text

    # create BeautifulSoup from the page
    soup = BeautifulSoup(source, 'html')  # 'lxml')

    # collect the data from the page
    data_for_url = soup.find_all('div', class_='s-item__wrapper clearfix')
    # print(guitars.prettify())

    # write the data into csv file
    write_to_csv_file(CSV_PATH, data_for_url)


if __name__ == '__main__':
    main()
