from flask import Blueprint, request, jsonify

from ..models import Appointment, db, Service
from werkzeug.utils import secure_filename
import os
from datetime import datetime

appointment_bp = Blueprint('appointment', __name__)

# will replace this with S3
UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@appointment_bp.route('/', methods=['POST'])
def create_appointment():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        zipcode = request.form.get('zipcode')
        message = request.form.get('message')
        service_names = request.form.getlist('services')
        appointment_date = request.form.get('appointment_date')
        appointment_time = request.form.get('appointment_time')
        image_url = None

        # Validate required fields
        if not all([name, email, service_names]):
            return jsonify({"error": "Name, email, and at least one service are required"}), 400


        if 'image' in request.files:
            image = request.files['image']
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                if not os.path.exists(UPLOAD_FOLDER):
                    os.makedirs(UPLOAD_FOLDER)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                image.save(filepath)
                image_url = filepath

        # Find matching services from DB
        services = Service.query.filter(Service.name.in_(service_names)).all()

        if not services:
            return jsonify({"error": "No matching services found"}), 400

        appointment = Appointment(
            name=name,
            email=email,
            phone=phone,
            zipcode=zipcode,
            message=message,
            image_url=image_url,
            services=services,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            created_at=datetime.now()
        )

        db.session.add(appointment)
        db.session.commit()

        # call send_email() function here using SendGrid

        return jsonify({"message": "Appointment created successfully"}), 201

    except Exception as e:
        print("Error creating appointment:", e)
        return jsonify({"error": "Failed to create appointment."}), 500
