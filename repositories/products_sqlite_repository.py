import sqlite3

import models
from models import Product

class ProductsSQLiteRepository:
    # avataan tietokantayhteys luokan konstruktorissa

    # HUOM: tietokantayhteyden avaaminen kannattaa tehdä toisin
    # mutta käymme sen läpi vasta Dependency Injection-osiossa

    def __init__(self):
        self.connection = sqlite3.connect('tuntiharjoitus1.db')

    # suljetaan tietokantayhteys destruktorissa
    # HUOM: tietokantayhteyden sulkeminen kannattaa tehdä toisin
    # mutta käymme sen läpi vasta Dependency Injection-osiossa

    def __del__(self):
        if self.connection is not None:
            self.connection.close()

    def all(self):
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
