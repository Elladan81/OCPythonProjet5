#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

# Programme Python 3 Type
# Autor: Mickael Lalevée 2019

# Informations:

import mysql.connector
from mysql.connector import errorcode

import config
import database
import view
import requests
import api


class MainProgram:
    """this class is the main program. It will use api.py to create a list of categories and a list of products.
    it use database.py to create a database with mySQL"""

    def __init__(self):
        # test a conection with the database
        try:
            print("Trying to connect to the database : '{}".format(config.DATABASE))
            self.database = mysql.connector.connect(user=config.USER,
                                                    password=config.PASSWORD,
                                                    host=config.HOST)
            print("\tConnection etablished")
        # if there is an error :
        except mysql.connector.Error as error:
            if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("user'sname or password is wrong")
            elif error.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print("Connection with database failed: \n Detected error : \n%s" % error)

        else:
            print("creating cursor ...")
            self.cursor = self.database.cursor()
            print("cursors created !")

        # this variable access to api
        self.api_access = api.Api(self.cursor)

        # This variable access to database.py
        self.db_access = database.Database(self.cursor)

        # This variable access to view.py
        self.request_access = view.View(self.cursor, self.database)

    def make_database(self):
        """
            This method will initiate the database.
            Create the database and tables.
            Then save the changement
        """
        print("Use of the database ...")
        self.db_access.use_database(config.DATABASE)
        print("Creating tables ...")
        self.db_access.create_tables(config.TABLES, self.database)

    def get_data(self):
        """
            This method uses the apiOpenFoodfacts class.
            It does the queries via the API, sorts the collected
            data and insert them into the database
        """
        print("Loading the JSON's file ...")
        self.api_access.load_id_countries()
        print("Getting products from the API ...")
        self.api_access.get_products()
        print("Deleting superfluous categories for the products ...")
        self.api_access.keep_one_cat()
        print("Replace and sort categories from the request ...")
        self.api_access.replace_sort_categories()
        print("Insert the categories into the database ...")
        self.api_access.insert_categories(self.database)
        print("Uploading products to the database ...")
        self.api_access.add_products(self.database)

    def loop_for_user_choice(self):
        """
            This method contains the loop for displaying
            products and product's categories. It also
            allows to search and find saved products.
        """
        # Loop for the main menu with multiple choices
        while 1:
            # Display the main menu
            print(config.MAIN_MENU)
            print("\t", config.Y_CHOICE, end=' ')
            try:
                ch = int(input())
                print("\n")
                # User's choices
                if ch == 1:
                    self.request_access.find_substitute(
                        config.LIMIT, config.OFFSET, config.TABLES
                    )
                elif ch == 2:
                    self.request_access.find_products()

                elif ch == 3:
                    self.request_access.show_all_categories(
                        config.LIMIT, config.OFFSET, config.TABLES
                    )
                elif ch == 4:
                    self.request_access.show_all_products(
                        config.LIMIT, config.OFFSET, config.TABLES
                    )
                elif ch == 5:
                    break
            except ValueError:
                print("Entrez un chiffre qui correspond ...")
                pass

    def main_loop(self):
        """ This method is the main loop """
        try:
            self.db_access.mycursor.execute("USE {};".format(config.DATABASE))
            print("\nTrying to use the database ...")
            self.cursor.execute("USE %s;" % config.DATABASE)
            print("\tDatabase used")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                # if database doesn't exist ...
                self.make_database()
                self.get_data()
                self.loop_for_user_choice()
        else:
            self.loop_for_user_choice()


if __name__ == '__main__':
    program = MainProgram()
    program.main_loop()
