from flask import Blueprint, jsonify, request
from ..models import Service, Category
from ..schemas import services_schema

services_bp = Blueprint('services', __name__)

@services_bp.route('/', methods=['GET'])
def get_services():

    categories = Category.query.all()
    result = []

    for category in categories:
        services = Service.query.filter_by(category_id=category.id).all()
        if not services:
            return jsonify({"error": "No matching services found"}), 400

        result.append({
            "category_name": category.name,
            "category_id": category.id,
            "services": services_schema.dump(services)
        })

    return jsonify(result), 200

@services_bp.route('/category', methods=['GET'])
def get_service_by_category():

    category_id = request.args.get('category')
    category = Category.query.filter_by(id=category_id).first()

    result = Service.query.filter_by(category_id=category_id).all()
    services = services_schema.dump(result)
    if not services:
        return jsonify({"error": "No matching service found"}), 400

    return jsonify({
        'category_name': category.name,
        'category_id': category.id,
        "services": services
    })