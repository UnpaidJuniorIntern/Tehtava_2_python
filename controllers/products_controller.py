from flask import Response, jsonify, request
from repositories.products_sqlite_repository import ProductsSQLiteRepository
from repositories.factories import create_products_repository

def get_all_products_handler():
    
    try:
        repo = create_products_repository()
        products = repo.all()
        products_list = []
        for product in products:
            products_list.append(
                {'id': product.id, 'name': product.name})
        return jsonify(products_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
def get_product_by_id_handler(product_id):
    try:
        repo = create_products_repository()
        product = repo.get_by_id(product_id)
        if product is None:
            return jsonify({'error': 'product not found'}), 404
        return jsonify(
            {'id': product.id, 'name': product.name})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
def add_product_handler():

    try:
        repo = create_products_repository()
        request_data = request.get_json()
        name = request_data.get('name', None)

        if name is None:
            return jsonify({'error': 'name is required'}), 400

        product = repo.save(name)
        return jsonify(
            {'id': product.id, 'name': product.name})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
def update_product_handler(product_id):

    try:
        repo = create_products_repository()
        request_data = request.get_json()
        name = request_data.get('name', None)

        if name is None:
            return jsonify({'error': 'name is required'}), 400

        product = repo.save(name, product_id=product_id) 
        if product is None:
            return jsonify({'error': 'product not found'}), 404

        return jsonify(
            {'id': product.id, 'name': product.name})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
def remove_product_handler(product_id):

    try:
        repo = create_products_repository()
        removed = repo.remove_by_id(product_id)
        if not removed:
            return jsonify({'error': 'error removing product'}), 400
        return Response(status=204)
    except Exception as e:
        return jsonify({'error': str(e)}), 500