#! usr/bin/env python3
# -*- Coding: UTF8 -*-

import json

import requests
import mysql.connector
from mysql.connector import Error

import config


class Api:
    """
        This class will use the API from OpenFoodfacts.
        It make several requests to find all the categories of products
        and then all the products.
        The list will be saved and insert into the database.
    """

    def __init__(self, cursor):
        self.categories = list()
        self.sorted_cat = list()
        self.cleaned_categories = list()
        self.cleaned_products = list()
        self.id_countries = list()
        self.id_name = list()
        self.change_pages = config.PAYLOAD
        self.mycursor = cursor

    def load_id_countries(self):
        """
            load all the id's countries
            from id_countries.json into a variable.
        """
        try:
            with open("id_countries.json", "r") as read_file:
                self.id_countries = json.load(read_file)
        except Error as e:
            print("Error while loading the JSON's file! ", e)
        else:
            print("\t Ok")

    def get_products(self):
        """
            make request via the API
            to get a list of products.
        """
        # Make the request via the API.
        for page in range(config.PAGE_MIN, config.PAGE_MAX):
            self.change_pages['page'] = page
            products_request = requests.get(
                config.PRODUCTS_URL,
                params=config.PAYLOAD
            )
            products = products_request.json()
            # Take only usefull informations
            for element in products['products']:
                if not all(tag in element for tag in (
                        "product_name", "brands", "nutrition_grade_fr", "url",
                        "stores", "countries", "categories")):
                    continue
                elif element['categories'][:3] in self.id_countries:
                    continue
                self.cleaned_products.append(element)
            page += 1
            print("Page(s): {} on {}".format(page, config.PAGE_MAX))

        print("\t Ok")

    def keep_one_cat(self):
        """
            deletes superfluous data and keeps one category per product.
        """
        try:
            text = list()
            for x in self.cleaned_products:
                # Partition() splits the string
                head, sep, tail = x['categories'].partition(',')
                text.append(head)

            counter = 0
            while counter < (len(text) - 1):
                for z in self.cleaned_products:
                    z['categories'] = text[counter]
                    counter += 1

        except Error as e:
            print("Error while deleting superfluous categories", e)
        else:
            print("\t Ok")

    def replace_sort_categories(self):
        """
            replace ' by a whitespace and sorted the categories
        """
        categories = list()
        for element in self.cleaned_products:
            if "'" in element['categories']:
                x = element['categories'].replace("'", " ")
                categories.append(x)
            else:
                categories.append(element['categories'])

        self.sorted_cat = sorted(set(categories))
        print("\t Ok")
        return self.sorted_cat

    def insert_categories(self, database):
        """
            insert the categories into the database,
            and save them
        """
        for element in self.sorted_cat:
            self.mycursor.execute("INSERT IGNORE INTO Categories(\
                   name) VALUES ('%s')" % (element))
        database.commit()
        print("\t Ok")

    def using_categories_for_products(self):
        """
            put id's and name's categories
            in a list for an utilisation in the adding_product's
            method.
        """
        self.id_name = list()
        count = 0
        while count < len(self.sorted_cat):
            category = str(count + 1)
            self.mycursor.execute("SELECT id, name FROM Categories\
                   WHERE id = " + category)
            category_saved = self.mycursor.fetchone()
            self.id_name.append(category_saved)
            count += 1
        return self.id_name

    def changing_categories_for_products(self):
        """
            change the new name
            of categories into the list of products
        """
        self.using_categories_for_products()
        ids = range(0, len(self.id_name))

        for number in ids:
            for produit in self.cleaned_products:
                if produit['categories'] == self.id_name[number][1]:
                    # print("OUI", produit['categories'], truc[n][name])
                    produit['categories'] = self.id_name[number][0]

        return self.cleaned_products

    def add_products(self, database):
        """
            put product into the database
        """
        self.changing_categories_for_products()

        try:
            for element in self.cleaned_products:
                self.mycursor.execute("INSERT IGNORE INTO Products(\
                       name, id_category, brands, nutriscore,\
                       link, shop, country) VALUES(\
                       %s, %s, %s, %s, %s, %s, %s)", (
                    element['product_name'], element['categories'],
                    element['brands'], element['nutrition_grade_fr'],
                    element['url'], element['stores'],
                    element['countries']))
        except Error as e:
            print("\t Failed", e)
        else:
            print("\t Ok")
            database.commit()
