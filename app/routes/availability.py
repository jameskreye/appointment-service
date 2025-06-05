import os
from flask import request, Blueprint, jsonify
from app.services.distance_service import get_coordinates, calculate_distance

availability_bp = Blueprint('availability', __name__)

@availability_bp.route('/', methods=['GET'])
def check_availability():

    user_zip = request.args.get('zipcode')

    if not user_zip:
        return jsonify({'error': 'zipcode is required'}), 400

    default_zip = os.getenv('DEFAULT_ZIPCODE')

    user_coordinate = get_coordinates(user_zip)
    default_coordinate = get_coordinates(default_zip)

    if not user_coordinate or not default_coordinate:
        return jsonify({'error': 'invalid zipcode'}), 400

    distance = calculate_distance(user_coordinate, default_coordinate)
    default_distance_limit = os.getenv('DISTANCE_LIMIT_KM')

    availability = distance < float(default_distance_limit)

    return jsonify({
        'available': availability,
        'distance_km': round(distance, 2),
        'from': default_zip,
        'to': user_zip
    })

