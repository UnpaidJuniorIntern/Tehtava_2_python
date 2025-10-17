
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

    # Pythonissa staattinen metodi annotoidaan näin
    # Staattinen metodi tarkoittaa sitä, että sitä kutsutaan käyttäen
    # luokan nimeä metodin vasemmalla puolella
    @staticmethod
    def get_all():
        with sqlite3.connect("tuntiharjoitus1.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM users")
            users = cur.fetchall()
            cur.close()
            users_list = []
            # Huomaa, että model classin metodi ei palauta hakutulosta suoraan json-formaatissa
            # Meidän pitää pystyä käyttämään samaa koodia riippumatta siitä,
            # haluaako käyttäjä vastauksen html, json- tai xml-formaatissa

            # Jos päättäisimme responsen formaatin modelissa, 
            # joutuisimme tekemään uuden model-luokan metodin eri
            # dataformaateille. 
            # Modelin tehtävä ei ole päättää tästä. 
            # MODEL TOIMII TIETOMALLINA ja DATA ACCESS LAYERINÄ
            # ELI TULKKINA CONTROLLERIN JA TIETOKANNAN VÄLISSÄ
            for user in users:
                users_list.append(User(user[1], user[2], user[3], user[0]))
            return users_list

    @staticmethod
    def get_by_id(_id):
        with sqlite3.connect("tuntiharjoitus1.db") as con:
            cursor = con.cursor()
            cursor.execute('SELECT * FROM users WHERE id = ?', (_id,))
            user = cursor.fetchone()
            cursor.close()
            if user is None:
                # Tässä voisi myös vaihtoehtoisesti heittää poikkeuksen
                return None
            return User(user[1], user[2], user[3], user[0])

    # Mikä self? self on Pythonissa jokaisen luokan instanssimetodin ensimmäinen parametri.
    # Sillä viitataan itse luokan instanssiin
    # se on metodia kutsuttaessa metodin ja pisteen vasemmalla puolella oleva muuttuja

    # Muista, jos metodi on static (eli annotoitu @staticmethod),
    # se ei ole instanssimetodi ja sen ensimmäinen parametri ei ole self


    # koska Pythonissa ei ole privaatteja eikä protected metodeja,
    # vaan kaikki ovat publiceja.
    # alaviivalla (_) alkavat metodit ja muuttujat on tarkoitettu privaateiksi

    # niiden kutusuminen lukan ulkopuolelta on siis teknisesti mahdollista, mutta ei suotavaa eikä niin ole tarkoitus

    def _add(self):
        with sqlite3.connect("tuntiharjoitus1.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO users(first_name, last_name, username) VALUES(?, ?, ?)",
                        (self.first_name, self.last_name, self.username))
            con.commit()
            self._id = cur.lastrowid
            cur.close()

    def _update(self):
        with sqlite3.connect("tuntiharjoitus1.db") as con:
            cur = con.cursor()
            cur.execute("UPDATE users SET first_name = ?, last_name = ?, username = ? WHERE id = ?",
                        (self.first_name, self.last_name, self.username, self._id))
            con.commit()

            cur.close()


    def save(self):
        # Jos id:tä ei ole instanssilla olemassa vielä, se tarkoittaa, että ollaan lisäämässä vasta uutta riviä tietokantaan

        if self._id is None:
            self._add()
        # jos User-classin instanssilla on jo _id-attribuutin arvo,
        # se tarkoittaa, että ollaan muokkaamassa oo käyttäjää
        else:
            self._update()


    def remove(self):

        with sqlite3.connect("tuntiharjoitus1.db") as con:
            cur = con.cursor()
            cur.execute("DELETE FROM users WHERE id = ?", (self.id,))
            con.commit()
            rows_affected = cur.rowcount
            cur.close()
            return rows_affected == 1


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