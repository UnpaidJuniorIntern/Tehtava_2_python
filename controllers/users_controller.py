
from flask import jsonify, request, Response

from repositories.users_sqlite_repository import UsersSQLiteRepository
from repositories.factories import create_users_repository

def get_all_users_handler():
    try:
        repo = create_users_repository()
        users = repo.all()
        users_list = []
        for user in users:
            users_list.append(
                {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'username': user.username})
        return jsonify(users_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def get_user_by_id_handler(user_id):
    try:
        repo = create_users_repository()
        user = repo.get_by_id(user_id)
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
        repo = create_users_repository()
        request_data = request.get_json()
        username = request_data.get('username', None)
        first_name = request_data.get('first_name', None)
        last_name = request_data.get('last_name', None)

        if username is None or first_name is None or last_name is None:
            return jsonify({'error': 'username and first_name and last_name are required'}), 400

        user = repo.save(first_name, last_name, username)
        return jsonify(
            {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'username': user.username})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def update_user_handler(user_id):
    try:
        repo = create_users_repository()

        request_data = request.get_json()
        username = request_data.get('username', None)
        first_name = request_data.get('first_name', None)
        last_name = request_data.get('last_name', None)

        if username is None or first_name is None or last_name is None:
            return jsonify({'error': 'username and first_name and last_name are required'}), 400

        user = repo.save(first_name, last_name, username, user_id=user_id)

        return jsonify(
            {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'username': user.username})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def remove_user_handler(user_id):
    try:
        repo = create_users_repository()
        removed = repo.remove_by_id(user_id)
        if not removed:
            return jsonify({'error': 'error removing user'}), 400
        return Response(status=204)
    except Exception as e:
        return jsonify({'error': str(e)}), 500