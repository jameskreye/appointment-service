from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from app.routes.availability import availability_bp
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Configurations
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)

    # Import and register blueprints inside the function to avoid circular imports
    from app.routes.appointment import appointment_bp
    app.register_blueprint(appointment_bp, url_prefix='/api/appointments')
    app.register_blueprint(availability_bp, url_prefix='/api/availability')

    return app