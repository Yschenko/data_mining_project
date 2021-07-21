import pandas as pd
import pymysql.cursors
import json

CONSTS = json.load(open('config.json', 'r'))


class SqlWrite:
    """
    This class create sql database for scraper.py and insert to it all data that collected r=from the web pages.
    There is 1 method 'create_database'.
    3 methods to create the tables and 3 to insert the data to them.
    """
    def __init__(self, const):
        """
        gets conts from the config file, and takes only the csv files tha in there.
        """
        self.guitar_file = const['CSV_PATH']['GUITARS_CSV']
        self.sellers_file = const['CSV_PATH']['SELLERS_CSV']
        self.shipping_file = const['CSV_PATH']['SHIPPING_CSV']

    @staticmethod
    def connect():
        """
        establish connection to mysql server.
        :return: the connection to mysql.
        """
        connection = pymysql.connect(host='localhost',
                                     user=CONSTS['SQL_USER']['USER_NAME'],
                                     password=CONSTS['SQL_USER']['PASSWORD'],
                                     cursorclass=pymysql.cursors.DictCursor)
        return connection

    @staticmethod
    def make_dataframe(csv_file):
        """

        :param csv_file:
        :return:
        """
        df = pd.read_csv(csv_file)

        return df

    def create_database(self, sql_string):
        """
        create guitars database.
        """
        connection = self.connect()
        with connection.cursor() as cursor:
            cursor.execute(sql_string)

    def create_table(self, use_database, sql_make_table):
        """

        :param use_database:
        :param sql_make_table:
        :return:
        """
        connection = self.connect()
        with connection.cursor() as cursor:
            cursor.execute(use_database)
            cursor.execute(sql_make_table)

    def enter_to_sellers(self):
        """
        insert to the sellers table the data from the csv files.
        """
        sellers = self.make_dataframe(self.sellers_file)
        connection = self.connect()
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

    def enter_to_shipping(self):
        """
        insert to the shipping table the data from the csv files.
        """
        shipping = self.make_dataframe(self.shipping_file)
        connection = self.connect()
        with connection.cursor() as cursor:
            cursor.execute('USE guitars;')
            for i, row in shipping.iterrows():
                if isinstance(row['COST'], str):
                    row['COST'] = float(row['COST'].replace(',', ''))
                if str(row['COST']) == 'nan':
                    row['COST'] = -1.0
                if str(row['ITEM_LOCATION']) == 'nan':
                    row['ITEM_LOCATION'] = 'NULL'
                if str(row['SHIPPING_TO']) == 'nan':
                    row['SHIPPING_TO'] = 'NULL'
                if str(row['DELIVERY']) == 'nan':
                    row['DELIVERY'] = 'NULL'
                cursor.execute("""INSERT INTO shipping
                (cost, item_location, shipping_to, delivery)
                VALUES """ + str(tuple(row)) + ";")
            connection.commit()

    def enter_to_guitars(self):
        """
        insert to the guitars table the data from the csv files.
        """
        guitars = self.make_dataframe(self.guitar_file)
        connection = self.connect()
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
