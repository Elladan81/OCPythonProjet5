#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

# Name of the database
DATABASE = "openfoodfacts"
# Name of the user
USER = "OpenClassrooms"
# Password uses to connect the user
PASSWORD = "Projet5openclassrooms"
# Host connected
HOST = "localhost"
# Description of the tables
TABLES = {}
TABLES['Categories'] = (
    "CREATE TABLE IF NOT EXISTS Categories ("
    " id SMALLINT(6) unsigned NOT NULL AUTO_INCREMENT,"
    " name VARCHAR(200) NOT NULL,"
    " PRIMARY KEY(id),"
    " UNIQUE KEY name (name)"
    " ) ENGINE=InnoDB;")

TABLES['Products'] = (
    "CREATE TABLE IF NOT EXISTS Products ("
    " id INT unsigned NOT NULL AUTO_INCREMENT,"
    " name VARCHAR(200),"
    " id_category SMALLINT(6) unsigned NOT NULL,"
    " brands VARCHAR(100),"
    " nutriscore CHAR(1),"
    " link VARCHAR(200),"
    " shop VARCHAR(100),"
    " country TEXT,"
    " PRIMARY KEY(id),"
    " UNIQUE KEY name (name),"
    " CONSTRAINT fk_categories_id FOREIGN KEY (id_category)"
    " REFERENCES Categories(id) ON DELETE CASCADE"
    " ) ENGINE=InnoDB;")

TABLES['Saved'] = (
    "CREATE TABLE IF NOT EXISTS Saved ("
    " id SMALLINT(6) unsigned NOT NULL AUTO_INCREMENT,"
    " name_orig VARCHAR(200),"
    " nutri_orig CHAR(1),"
    " name_sub VARCHAR(200),"
    " nutri_sub CHAR(1),"
    " shop_sub VARCHAR(100),"
    " link_sub VARCHAR(200),"
    " PRIMARY KEY(id),"
    " CONSTRAINT fk_products_name FOREIGN KEY (name_orig)"
    " REFERENCES Products(name) ON DELETE CASCADE,"
    " CONSTRAINT fk_products_name_sub FOREIGN KEY (name_sub)"
    " REFERENCES Products(name) ON DELETE CASCADE"
    " ) ENGINE=INNoDB;")

# URL used to get the products
PRODUCTS_URL = "https://fr.openfoodfacts.org/cgi/search.pl?"

# Params for the url_prod
PAYLOAD = {
    "search_simple": '1',
    "action": 'process',
    "tagtype_0": 'categories',
    "tag_contains_0": 'contains',
    "page": 1,
    "page_size": 100,
    "json": '1'
}

# Page number for the request, increase "PAGE_MAX" to get more products
PAGE_MIN = 1
PAGE_MAX = 10

# Variables used for some SQL requests
LIMIT = 10
OFFSET = 0
