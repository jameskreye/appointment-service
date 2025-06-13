from flask import Flask
from flask_cors import CORS

from app.routes.availability import availability_bp
from app.routes.services import services_bp
from config import Config

from .extensions import db, migrate


def create_app():
    app = Flask(__name__)
    CORS(app)

    # Configurations
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import and register blueprints inside the function to avoid circular imports
    from app.routes.appointment import appointment_bp
    app.register_blueprint(appointment_bp, url_prefix='/api/appointments')
    app.register_blueprint(availability_bp, url_prefix='/api/availability')
    app.register_blueprint(services_bp, url_prefix='/api/services')

    return app

# Import models AFTER db is initialized to avoid circular import
from app import models