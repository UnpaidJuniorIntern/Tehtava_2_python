from flask import Response, jsonify, request
import models

def get_all_users_handler():
    # sen sijaan, että tekisimme tietokantakyselyn tässä
    # kutsumme staattista User-luokan get_all-metodia
    # joka palauttaa meille listan User-luokan instansseja
    try:
        users = models.User.get_all()
        users_list = []
        for user in users:
            users_list.append(
                {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'username': user.username})
        return jsonify(users_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

def get_user_by_id_handler(user_id):
    try:
        user = models.User.get_by_id(user_id)
        if user is None:
            return jsonify({'error': 'user not found'}), 404
        return jsonify(
            {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'username': user.username})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

def add_user_handler():

    """
        routehandler lisää uuden käyttäjän tietokantaan
        1. otetaan vastaan request body
        2. tarkistetaan, että pakolliset tiedot löytyvät request bodysta
        3. luodaan tiedoilla uusi instanssi User-luokasta
        4. tallennetaan käyttäjä tietokantaan
        5. palautetaan tallennetun käyttäjän tiedot takaisin clientille
    """

    try:
        request_data = request.get_json()
        username = request_data.get('username', None)
        first_name = request_data.get('first_name', None)
        last_name = request_data.get('last_name', None)

        if username is None or first_name is None or last_name is None:
            return jsonify({'error': 'username and first_name and last_name are required'}), 400

        user = models.User(first_name, last_name, username)
        user.save()
        return jsonify(
            {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'username': user.username})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
def update_user_handler(user_id):

    """

        routehandler muokkaa oo. käyttäjää
        1. otetaan vastaan request body
        2. haetaan käyttäjä idn perusteella tietokannasta
        3. tarkistetaan, että käyttäjä löytyy
        4. jos jotakin pakollista tietoa ei ole request bodyssa, käytetään jo tietokannasta läytyvää arvoa
        5. asetetaan arvot käyttäjälle attribuutteihin first_name, last_name ja username
            * huom idn arvoa ei päivitetä ikinä
        6. päivitetään uudet tiedot tietokantaan
        7. palautetaan vastaus takaisin clientille


    """

    try:
        user = models.User.get_by_id(user_id)
        if user is None:
            return jsonify({'error': 'user not found'}), 404
        request_data = request.get_json()
        username = request_data.get('username', user.username)
        first_name = request_data.get('first_name', user.first_name)
        last_name = request_data.get('last_name', user.last_name)
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return jsonify(
            {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'username': user.username})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
def remove_user_handler(user_id):

    """

    routehandler poistaa id:n mukaan valitun käyttäjän tietokannasta
    1. haetaan käyttäjä tietokannasta id:n perusteella
    2. tarkistetaan, että käyttäjä löytyy
    3. poistetaan käyttäjä
    4.
        * jos ei onnistu, palautetaan virhe 'error removing user' statuskoodilla 400 (BAD REQUEST)
        * jos poisto onnistuu palautetaan tyhjä response statuskoodilla 204 (NO CONTENT)

    """
    try:
        user = models.User.get_by_id(user_id)
        if user is None:
            return jsonify({'error': 'user not found'}), 404
        removed = user.remove()
        if not removed:
            return jsonify({'error': 'error removing user'}), 400
        return Response(status=204)
    except Exception as e:
        return jsonify({'error': str(e)}), 500