#! usr/bin/env python3
# -*- Coding: UTF-8 -*-


from termcolor import colored

# Name of the database
DATABASE = "openfoodfacts6"
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
PAGE_MAX = 30

# Different texts to display.
Y_CHOICE = colored('Votre choix est:', attrs=['underline'])
IMP = colored('IMPOSSIBLE', 'red', attrs=['dark', 'blink'])
LOWER_YES = colored('o', 'green', attrs=['bold'])
UPPER_YES = colored('O', 'green', attrs=['bold'])
LOWER_NO = colored('n', 'red', attrs=['bold'])
UPPER_NO = colored('N', 'red', attrs=['bold'])
PLUS = colored('+', 'green', attrs=['bold'])
LESS = colored('-', 'yellow', attrs=['bold'])
QUIT = colored('q', 'cyan', attrs=['bold'])
ID = colored('N°: ', 'cyan')
NAME = colored('Nom: ', 'red')
NUTRISCORE = colored('Nutriscore: ', 'green')
SHOP = colored('Magasin: ', 'yellow')
BRAND = colored('Marque: ', 'blue')
LINK = colored('URL: ', 'white')
SUBSTITUT = colored('Votre substitut: ', 'red', attrs=['blink'])
PRODUCT = colored('Produit à remplacer: ', 'blue')
N_SEARCH = colored('N° recherche: ', 'magenta')

CHOOSE_CAT = colored(
    'Sinon, sélectionnez une catégorie de produits par son numéro.',
    attrs=['underline'])
CHOOSE_PROD = colored(
    'Sinon, sélectionnez un produit par son numéro pour le substituer.',
    attrs=['underline'])
ERROR_1 = colored(
    'Choisir entre +, - ou q SVP', 'white',
    'on_red', attrs=['blink'])
ERROR_2 = colored(
    'Choisir entre +, -, q ou un numéro SVP', 'white',
    'on_red', attrs=['blink'])
YOUR_CAT = colored(
    'Vous êtes dans la catégorie: %s',
    attrs=['underline'])

# Variables used for menus
MAIN_MENU_DECORATION_1 = colored(
    '##################################################',
    'blue', attrs=['blink'])

MAIN_MENU_TITLE = colored(
    'MENU PRINCIPAL', 'red', attrs=['underline'])

MAIN_MENU_TEXT = ('\n Que voulez-vous faire :\t\t\t \n\
    1) Quel aliment souhaitez vous remplacer ?\t\t \n\
    2) Retrouver mes aliments substitués\t\t \n\
    3) Quitter\t\t\t\t\t ')

MAIN_MENU = ('\n\n%s \n \t %s \t\t\t %s \n%s' % (
    MAIN_MENU_DECORATION_1, MAIN_MENU_TITLE, MAIN_MENU_TEXT, MAIN_MENU_DECORATION_1))

SS_MENU = ("\t +----------------------------------+\
    \n\t |Pour plus d'elements , taper '%s'  |\
    \n\t |Pour moins d'elements , taper '%s' |\
    \n\t |Pour quitter, taper '%s'           |\
    \n\t +----------------------------------+ \n" % (
    PLUS, LESS, QUIT))

SS_MENU_2 = ("\t +-------------------------------------------+\
    \n\t |Pour plus d'elements , tapez '%s'          |\
    \n\t |Pour moins d'elements , tapez '%s'         |\
    \n\t |Pour quitter, tapez '%s'                   |\
    \n\t |Pour plus d'informations, tapez son numéro |\
    \n\t +-------------------------------------------+\n" % (
    PLUS, LESS, QUIT))

MENU_CHOOSE_CAT = ('\t +------------------------------------------------------------------+\
    \n\t |Pour plus de categories, taper "%s"                                |\
    \n\t |Pour moins de categories, taper "%s"                               |\
    \n\t |Pour quitter, taper "%s"                                           |\
    \n\t |                                                                  |\
    \n\t |%s     |\
    \n\t +------------------------------------------------------------------+ \n' % (
    PLUS, LESS, QUIT, CHOOSE_CAT))

MENU_CHOOSE_PROD = ('\t +----------------------------------------------------------------------+\
    \n\t |Pour plus de produits, taper "%s"                                      |\
    \n\t |Pour moins de produits, taper "%s"                                     |\
    \n\t |Pour quitter, taper "%s"                                               |\
    \n\t |                                                                      |\
    \n\t |%s     |\
    \n\t +----------------------------------------------------------------------+ \n' % (
    PLUS, LESS, QUIT, CHOOSE_PROD))

MENU_SAVE = ('\t +---------------------------------+\
    \n\t |Sauvegarder ?                     |\
    \n\t |\t Si oui, taper "%s" ou "%s"       |\
    \n\t |\t Si non, taper "%s" ou "%s"       |\
    \n\t |\t Pour quitter, taper "%s"        |\
    \n\t +---------------------------------+ \n' % (
    LOWER_YES, UPPER_YES, LOWER_NO, UPPER_NO, QUIT))

MENU_INF = ('\t +--------------------+\
    \n\t |Quitter, taper sur %s|\
    \n\t +--------------------+ \n' % QUIT)

# Variables used for some SQL requests
LIMIT = 10
OFFSET = 0
