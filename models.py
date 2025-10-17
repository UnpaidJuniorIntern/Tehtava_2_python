
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

    @property
    def id(self):
        return self._id