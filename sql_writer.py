import pandas as pd
import pymysql.cursors
import numpy as np


class SqlWrite:
    """
    This class create sql database for scraper.py and insert to it all data that collected r=from the web pages.
    """
    def __init__(self, const):
        """
        gets conts from the config file, and takes only the csv files tha in there.
        """
        self.guitar_file = const['CSV_PATH']['GUITARS_CSV']
        self.sellers_file = const['CSV_PATH']['SELLERS_CSV']
        self.shipping_file = const['CSV_PATH']['SHIPPING_CSV']

    def connect(self):
        """
        establish connection to mysql server.
        :return: the connection to mysql.
        """
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='Ysch[5752]',
                                     cursorclass=pymysql.cursors.DictCursor)
        return connection

    def create_database(self):
        """
        create guitars database with 3 tables in the database: guitars, sellers and shipping.
        """
        connection = self.connect()
        with connection.cursor() as cursor:
            cursor.execute('''CREATE DATABASE guitars;''')

            cursor.execute('USE guitars;')

            cursor.execute('''CREATE TABLE sellers (
                              seller_id INT AUTO_INCREMENT PRIMARY KEY,
                              name TEXT,
                              positive_feedback FLOAT,
                              member_since TEXT,
                              location TEXT,
                              items_for_sell INT
                              );''')

            cursor.execute('''CREATE TABLE shipping (
                                          shipping_id INT AUTO_INCREMENT PRIMARY KEY,
                                          coast FLOAT,
                                          item_location TEXT,
                                          shipping_to TEXT,
                                          delivery TEXT
                                          );''')

            cursor.execute('''CREATE TABLE guitars (guitar_id INT AUTO_INCREMENT PRIMARY KEY,
                                                    ebay_id CHAR(20),
                                                    title TEXT,
                                                    price FLOAT,
                                                    brand TEXT,
                                                    string_configuration INT,
                                                    model_year INT,
                                                    shipping INT,
                                                    seller INT
                                                    );''')

    def prepare_data(self):
        """
        make pandas dataframes from the given csv files.
        :return: the 3 pandas dataframes
        """
        guitars = pd.DataFrame(pd.read_csv(self.guitar_file))
        sellers = pd.DataFrame(pd.read_csv(self.sellers_file))
        shipping = pd.DataFrame(pd.read_csv(self.shipping_file))
        return guitars, sellers, shipping

    def enter_to_database(self):
        """
        insert to the sql tables the data from the csv files. (with the dataframes of 'prepare_data')
        """
        guitars, sellers, shipping = self.prepare_data()

        connection = self.connect()

        # sellers table
        with connection.cursor() as cursor:
            cursor.execute('USE guitars;')
            for i, row in sellers.iterrows():
                for j in range(len(row)):
                    if isinstance(row[j], str):
                        row[j] = row[j].replace(',', '')
                if str(row['NAME']) == 'nan':
                    row['NAME'] = 'NULL'
                if str(row['POSITIVE_FEEDBACK']) == 'nan':
                    row['POSITIVE_FEEDBACK'] = -1
                if str(row['MEMBER_SINCE']) == 'nan':
                    row['MEMBER_SINCE'] = 'NULL'
                if str(row['LOCATION']) == 'nan':
                    row['LOCATION'] = 'NULL'
                if str(row['ITEMS_FOR_SELL']) == 'nan':
                    row['ITEMS_FOR_SELL'] = -1
                cursor.execute("""INSERT INTO sellers
                (name, positive_feedback, member_since, location, items_for_sell)
                VALUES """ + str(tuple(row)) + ";")
            connection.commit()

        # shipping table
        with connection.cursor() as cursor:
            cursor.execute('USE guitars;')
            for i, row in shipping.iterrows():
                if isinstance(row['COAST'], str):
                    row['COAST'] = float(row['COAST'].replace(',', ''))
                if str(row['COAST']) == 'nan':
                    row['COAST'] = -1.0
                if str(row['ITEM_LOCATION']) == 'nan':
                    row['ITEM_LOCATION'] = 'NULL'
                if str(row['SHIPPING_TO']) == 'nan':
                    row['SHIPPING_TO'] = 'NULL'
                if str(row['DELIVERY']) == 'nan':
                    row['DELIVERY'] = 'NULL'
                cursor.execute("""INSERT INTO shipping
                (coast, item_location, shipping_to, delivery)
                VALUES """ + str(tuple(row)) + ";")
            connection.commit()

        # guitars table
        with connection.cursor() as cursor:
            cursor.execute('USE guitars;')
            for i, row in guitars.iterrows():
                if isinstance(row['PRICE'], str):
                    row['PRICE'] = float(row['PRICE'].replace(',', ''))
                if str(row['PRICE']) == 'nan':
                    row['PRICE'] = -1.0
                if str(row['STRING_CONGIGURATION']) == 'nan' or isinstance(row['STRING_CONGIGURATION'], str):
                    row['STRING_CONGIGURATION'] = -1
                if str(row['MODEL_YEAR']) == 'nan' or isinstance(row['MODEL_YEAR'], str):
                    row['MODEL_YEAR'] = -1
                if str(row['SHIPPING_NUM']) == 'nan' or isinstance(row['SHIPPING_NUM'], str):
                    row['SHIPPING_NUM'] = -1
                if str(row['SELLER_NUM']) == 'nan' or isinstance(row['SELLER_NUM'], str):
                    row['SELLER_NUM'] = -1
                if str(row['BRAND']) == 'nan':
                    row['BRAND'] = 'NULL'
                cursor.execute("""INSERT INTO guitars
                (ebay_id, title, price, brand, string_configuration, model_year, shipping, seller)
                VALUES """ + str(tuple(row)) + ";")
            connection.commit()




# def main():
#     consts = json.load(open('config.json', 'r'))
#
#
# if __name__ == '__main__':
#     main()