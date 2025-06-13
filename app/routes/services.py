from flask import Blueprint, jsonify

from ..models import Service, Category

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
            "services": [
                {"id": s.id, "name": s.name, "description": s.description} for s in services
            ]
        })

    return jsonify(result), 200