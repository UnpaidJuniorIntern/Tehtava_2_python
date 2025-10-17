
import sqlite3

# models.py

class User:
    # otetaan konstruktorissa vastaan tarvittavat parametrit,
    # jotta voimme tehdä luokan instansseja tietokannan riveistä

    # huomaa, että _id on tietokannassa nimellä id.
    # Nimeäminen poikkeaa tässä, koska id on varattu nimi Pythonissa,
    # emmekä halua ylikirjoittaa sitä

    # _id on ainoa parametri, joka ei ole pakollinen konstruktorissa.
    # id on kyllä pakollinen sarake tietokantataulussa, mutta
    # mutta lisättäessä uutta riviä tietokantaan emme anna itse id:n arvoa,
    # vaan tietokanta päättää sen

    def __init__(self, first_name, last_name, username, _id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self._id = _id

    @property
    def id(self):
        return self._id
    
    # Product luokka

class Product:
    def __init__(self, name, _id=None):
        self.name = name
        self._id = _id

    @staticmethod
    def get_all():
        with sqlite3.connect("tuntiharjoitus1.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM products")
            products = cur.fetchall()
            cur.close()
            products_list = []
            for product in products:
                products_list.append(Product(product[1], product[0]))
            return products_list

    @staticmethod
    def get_by_id(_id):
        with sqlite3.connect("tuntiharjoitus1.db") as con:
            cursor = con.cursor()
            cursor.execute('SELECT * FROM products WHERE id = ?', (_id,))
            product = cursor.fetchone()
            cursor.close()
            if product is None:
                return None
            return Product(product[1], product[0])

    def _add(self):
        with sqlite3.connect("tuntiharjoitus1.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO products(name) VALUES(?)", (self.name,))
            con.commit()
            self._id = cur.lastrowid
            cur.close()

    def _update(self):
        with sqlite3.connect("tuntiharjoitus1.db") as con:
            cur = con.cursor()
            cur.execute("UPDATE products SET name = ? WHERE id = ?", (self.name, self._id))
            con.commit()
            cur.close()

    def save(self):
        if self._id is None:
            self._add()
        else:
            self._update()

    def remove(self):
        with sqlite3.connect("tuntiharjoitus1.db") as con:
            cur = con.cursor()
            cur.execute("DELETE FROM products WHERE id = ?", (self.id,))
            con.commit()
            rows_affected = cur.rowcount
            cur.close()
            return rows_affected == 1

    @property
    def id(self):
        return self._id