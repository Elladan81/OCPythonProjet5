create TABLE  Categories (
    id SMALLINT(6) unsigned NOT NULL AUTO_INCREMENT,
    name VARCHAR(200) NOT NULL,
    PRIMARY KEY(id),
    UNIQUE KEY name (name)
    ) ENGINE=InnoDB;

create TABLE Products (
    id INT unsigned NOT NULL AUTO_INCREMENT COMMENT '',
    name VARCHAR(200) COMMENT '',
    id_category SMALLINT(6) unsigned NOT NULL,
    brands VARCHAR(100),
    nutriscore CHAR(1),
    link VARCHAR(200),
    shop VARCHAR(100),
    country TEXT,
    PRIMARY KEY(id),
    UNIQUE KEY name (name),
    CONSTRAINT fk_categories_id FOREIGN KEY (id_category)
    REFERENCES Categories(id) ON delete CASCADE
    ) ENGINE=InnoDB;

create TABLE Saved (
    id SMALLINT(6) unsigned NOT NULL AUTO_INCREMENT,
    name_orig VARCHAR(200),
    nutri_orig CHAR(1),
    name_sub VARCHAR(200),
    nutri_sub CHAR(1),
    shop_sub VARCHAR(100),
    link_sub VARCHAR(200),
    PRIMARY KEY(id),
    CONSTRAINT fk_products_name FOREIGN KEY (name_orig)
    REFERENCES Products(name) ON delete CASCADE,
    CONSTRAINT fk_products_name_sub FOREIGN KEY (name_sub)
    REFERENCES Products(name) ON delete CASCADE
    ) ENGINE=INNoDB;