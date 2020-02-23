#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

import sys

import mysql.connector
from mysql.connector import errorcode

import config


class Database:
    """
        Manage database
    """

    def __init__(self, cursor):
        self.mycursor = cursor

    def use_database(self, dbname):
        """
            This method uses the database - if
            the database doesn't exists, use the method create_database to
            create one.
        """
        # Try to use the database
        try:
            self.mycursor.execute("USE {};".format(dbname))
        # Print the error and use the method create_database
        except mysql.connector.Error as error:
            print("Database {} does not exists".format(dbname))
            if error.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_database(dbname)
                print("Database {} created successfully".format(dbname))
        else:
            print("\t Ok")

    def create_database(self, dbname):
        """
            creates the tables described in the "tables" files
            if they don't exist.
        """
        # Create the database with SQL request
        try:
            req = ("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8';".format(
                dbname))
            self.execute_request(req)
        except mysql.connector.Error as error:
            print("Failed creating database: {}".format(error))
            exit(1)
        else:
            print("\t Ok")
            self.use_database(dbname)

    def create_tables(self, tables, database):
        """ creates the tables through a loop """
        # Delete tables for a clean shot.
        for table_name in tables:
            table_description = tables[table_name]
            try:
                print("\t Table : {} ...".format(table_name), end='')
                self.execute_request(table_description)
            except mysql.connector.Error as error:
                if error.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(error.msg)
            else:
                print("\t Ok")
                database.commit()

    def execute_request(self, req):
        """ This method execute SQL request."""
        try:
            self.mycursor.execute(req)
        except Exception as error:
            # Display the SQL query and the error
            print("Incorrect SQL query: \n {} \n Detected error : ".format(
                req))
            print(error)
            return 0
        else:
            return 1
