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
    """ shows all products """
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