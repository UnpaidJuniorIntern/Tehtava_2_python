
# repositories/factories.py

from repositories.users_sqlite_repository import UsersSQLiteRepository

# pythonin tapauksessa voidaan luoda jokaiselle repositoriolle oma
# funktio, jota kutsutaan controllerissa
def create_users_repository():
    # jos repositorio muuttuu tietokannan vaihtuessa,
    # muutos voidaan tehdä vain tänne yhteen paikkaan
    # ja kaikki controllerit, joissa usersRepositorya tarvitaan
    # käyttävät palautettavaa instanssia
    
    return UsersSQLiteRepository()