#! usr/bin/env python3
# -*- Coding: UTF-8 -*-


import os
import sys
import string

import mysql.connector
from mysql.connector import errorcode

import config


class View:
    """
        View class is the connection
        between the user and the program.
    """

    def __init__(self, cursor, database):
        self.mycursor = cursor
        self.database = database
        # Etablishment of the connection with the database
        self.run = 0
        self.u_choice = ''
        self.count = []
        self.offset = 0

    def show_all_categories(self, lim, off, table):
        """ This method shows all the categories."""
        self.run = 1
        # change the limit and the offset for the table Categories
        self.offset = off
        while self.run:
            # Get the name of the table Categories
            name_table = list(table.keys())
            cat = name_table[0]

            # Count items in the table Categories
            self.mycursor.execute("SELECT COUNT(*) FROM %s;" % cat)
            for number in self.mycursor.fetchone():
                tt_element = number

            req = ("SELECT * FROM %s ORDER BY id LIMIT %s\
                OFFSET %s;" % (cat, lim, self.offset))

            self.display(
                req, lim, self.offset, cat, tt_element,
                config.SS_MENU, config.ERROR_1)

            if self.u_choice == 'q' or self.u_choice == 'Q':
                self.clear()
                self.run = 0
            elif self.u_choice.isdecimal():
                self.show_all_products(self.u_choice, off, table)

    def show_all_products(self, lim, off, table):
        """ shows all the products """
        self.run = 1
        # change the limit and the offset for the table Products
        self.offset = off
        while self.run:
            # Get the name of the table Products
            name_table = list(table.keys())
            cat = name_table[1]

            # Count how many items are there in the table Categories
            self.mycursor.execute("SELECT COUNT(*) FROM %s;" % cat)
            for number in self.mycursor.fetchone():
                tt_element = number

            req = ("SELECT id, name, brands FROM %s ORDER BY id LIMIT %s\
                OFFSET %s;" % (cat, lim, self.offset))

            self.display(
                req, lim, self.offset, cat, tt_element,
                config.SS_MENU_2, config.ERROR_1)

            if self.u_choice == 'q' or self.u_choice == 'Q':
                self.clear()
                self.run = 0
            elif self.u_choice.isdecimal():
                self.more_information(self.u_choice)

    def find_substitute(self, lim, off, table):
        """
            allowing the user to find a better food
            with a higher nutriscore
        """
        self.run = 1
        self.offset = off
        while self.run:
            name_table = list(table.keys())
            cat = name_table[0]
            self.mycursor.execute("SELECT COUNT(*) FROM %s;" % cat)
            for number in self.mycursor.fetchone():
                tt_element = number

            req = ("SELECT * FROM %s ORDER BY id LIMIT %s\
                OFFSET %s;" % (cat, lim, self.offset))

            # print("\t\t Choisir une catégorie, svp ...")
            self.display(
                req, lim, self.offset, cat, tt_element,
                config.MENU_CHOOSE_CAT, config.ERROR_2)

            # if user wants to quit, then quit
            if self.u_choice == 'q' or self.u_choice == 'Q':
                self.clear()
                self.run = 0
            # or continue ...
            elif self.u_choice.isdecimal():
                self.join_products_categories(self.u_choice, lim, cat)

    def join_products_categories(self, user, lim, cat):

        self.run = 1
        # Reset self.offset
        self.offset = 0

        while self.run:
            self.u_choice = user
            # Count the total of products from a category
            self.mycursor.execute("SELECT COUNT(*)\
                FROM Products WHERE id_category = %s;" % self.u_choice)
            for number in self.mycursor.fetchone():
                tt_element = number

            # Select the name of the category used
            self.mycursor.execute("SELECT name\
                FROM Categories WHERE id = %s;" % self.u_choice)
            for name in self.mycursor.fetchone():
                print("\t", config.YOUR_CAT % name)

            # Show all the products from the selected category
            req = ("SELECT Products.id, Products.name, brands,\
                nutriscore FROM Products INNER JOIN Categories\
                ON Products.id_category = Categories.id\
                WHERE Categories.id = %s\
                ORDER BY Products.id LIMIT %s OFFSET %s;" % (
                self.u_choice, lim, self.offset))

            self.category = self.u_choice

            self.display(
                req, lim, self.offset, cat, tt_element,
                config.MENU_CHOOSE_PROD, config.ERROR_2)

            # if user wants to quit, then quit
            if self.u_choice == 'q' or self.u_choice == 'Q':
                self.run = 0
                self.clear()
            # or continue ...
            elif self.u_choice.isdecimal():
                self.find_better_product(self.u_choice, self.category)

    def find_better_product(self, product, category):

        try:
            # Get the product and save it in a variable into a dict
            self.mycursor.execute("SELECT * FROM Products\
                WHERE Products.id = " + product)
            information = self.mycursor.fetchone()
            name_prod = str(information[1])
            nutriscore = str(information[4])

            # This dictionnaire will be used for the table Saved
            dc = {}
            dc['id_cat'] = category
            dc['name'] = name_prod
            dc['code'] = nutriscore

            # Show products with a better nutriscore
            self.mycursor.execute("SELECT Products.id, Products.name, Products.nutriscore,\
                Products.shop, Products.brands, Products.link\
                FROM Products INNER JOIN Categories \
                ON Products.id_category = Categories.id\
                WHERE Categories.id = %(id_cat)s \
                AND Products.nutriscore <= %(code)s \
                ORDER BY Products.nutriscore, rand() LIMIT 5", dc)
            # List of index to display
            index = [config.ID, config.NAME, config.NUTRISCORE,
                     config.SHOP, config.BRAND, config.LINK]
            # This loop will display the index and the information related to
            for substitute in self.mycursor.fetchall():
                count = 0
                x = 0
                while count < len(substitute):
                    while x < len(index):
                        print(index[x], substitute[count], end='\t')
                        count += 1
                        x += 1
                        if x == 5:
                            # Put the LINK under the others informations
                            print("\n", end=' ')
                print("\n\n")

            # Display the menu
            print(config.MENU_SAVE)
            print("\t Votre choix:", end=' ')
            user_saved = input()
            # Two possibilites, continue or quit
            if user_saved == "O" or user_saved == "o":
                self.saved_products_choice(dc)
            elif user_saved == "N" or user_saved == "n":
                pass
        except:
            print("Ce numéro ne correspond pas.\n Recommencez ...")
            pass

    def saved_products_choice(self, sub):

        self.run = 1
        while self.run:
            # User's choice
            print("\n Veuillez entrer le numéro du produit à sauvegarder.\n\
                Votre choix: ", end=' ')
            svd_prod = int(input())
            # User wants to save his search
            if svd_prod != -1:
                substitut = str(svd_prod)
                # Get the product and save it in a variable then a dict
                self.mycursor.execute("SELECT * FROM Products\
                    WHERE Products.id = " + substitut)
                information = self.mycursor.fetchone()
                name_sub = information[1]
                nutriscore_sub = information[4]
                shop_sub = information[6]
                link_sub = information[5]
                sub['sub'] = name_sub
                sub['sub_code'] = nutriscore_sub
                sub['shop'] = shop_sub
                sub['link'] = link_sub
                # Insert the product into the table "Saved"
                self.mycursor.execute("INSERT INTO Saved (\
                    name_orig, nutri_orig, name_sub, nutri_sub,\
                    shop_sub, link_sub) VALUES (%(name)s, %(code)s,\
                     %(sub)s, %(sub_code)s, %(shop)s, %(link)s);", sub)
                # Save changement
                self.database.commit()
                self.run = 0
            elif svd_prod == -1:
                self.run = 0

    def find_products(self):
        """ displays saved data """
        self.run = 1
        while self.run:
            self.mycursor.execute("SELECT * FROM Saved;")
            index = [config.N_SEARCH, config.PRODUCT, config.NUTRISCORE,
                     config.SUBSTITUT, config.NUTRISCORE, config.BRAND, config.LINK]
            # This loop display the index and the information related to
            for item in self.mycursor.fetchall():
                count = 0
                x = 0
                while count < len(item):
                    while x < len(index):
                        print(index[x], item[count], end='\t')
                        count += 1
                        x += 1
                        if x == 3:
                            print("\n\t", end='\t\t')
                        elif x == 6:
                            # Put the LINK under the others informations
                            print("\n", end=' ')
                print("\n\n")
            # Display the second menu
            print(config.MENU_INF)
            print("\t", config.Y_CHOICE, end=' ')
            back = input()
            if back == 'q' or back == 'Q':
                self.run = 0
            else:
                pass

    def more_information(self, number):
        """
            displays more informations about a choosen product
        """
        self.run = 1
        while self.run:
            self.mycursor.execute("SELECT * FROM Products\
                WHERE id = %s" % number)
            print("\n")

            # Display more informations
            for row in self.mycursor:
                count = 0
                while count < len(row):
                    print(row[count], end='\t')
                    count += 1
                print("\n")

            # Display the menu
            print(config.MENU_INF)
            print(config.Y_CHOICE, end=' ')

            # User's choice
            back = input()
            if back == 'q' or back == 'Q':
                self.run = 0
            else:
                pass

    def display(self, req, lim, off, cat, elem, menu, error):
        """
            display all items from 'cat',
            propose to the user to see more, less , quit
            or return self.u_choice for the next
            method.
        """
        self.run = 1
        while self.run:
            # Make the request
            self.mycursor.execute(req)

            # Display the request
            for show in self.mycursor.fetchall():
                count = 0
                while count < len(show):
                    print(show[count], end='\t')
                    count += 1
                print("\n")

            # Display the menu
            print(menu)

            # User's choice
            self.u_choice = input('Votre choix: ')

            # Show more or less
            if self.u_choice == '+' and off == 0:
                off = off + lim
                self.offset = off
                return self.offset
            elif self.u_choice == '+' and off <= elem and (off + lim) <= elem:
                off = off + lim
                self.offset = off
                return self.offset
            elif self.u_choice == '-' and off >= 10:
                off = off - lim
                self.offset = off
                return self.offset
            elif self.u_choice == '-' and off == 0:
                print("\t", config.Y_CHOICE, "\t", config.IMP, '\n')
            elif self.u_choice == '+' and (off + lim) >= elem:
                print("\t", config.Y_CHOICE, "\t", config.IMP, '\n')

            # If the user press 'enter' print an error message
            elif self.u_choice == '':
                print("\t\t", error, "\n")
                pass
            # If the user press q or Q, quit
            elif self.u_choice == 'q' or self.u_choice == 'Q' \
                    and self.u_choice.isalpha():
                return self.u_choice
            elif self.u_choice != 'q' and self.u_choice != 'Q' \
                    and self.u_choice.isalpha():
                pass
            elif self.u_choice.isdecimal():
                return self.u_choice

    def clear(self):
        """ This method allow a refresh of the screen"""
        os.system('cls')
