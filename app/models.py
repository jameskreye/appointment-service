import string

from sqlalchemy import String

from app import db
from datetime import datetime
import random

def generate_id(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

class Service(db.Model):
    __tablename__ = 'service'

    id = db.Column(String(8), primary_key=True, default=generate_id)
    name = db.Column(db.String(120), unique=True,nullable=False)

    def __repr__(self):
        return f"<Service {self.name}>"

class Appointment(db.Model):
    id = db.Column(String(8), primary_key=True, default=generate_id)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    zipcode = db.Column(db.String(10), nullable=False)
    message = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    appointment_date = db.Column(db.String, nullable=False)
    appointment_time = db.Column(db.String, nullable=False)


    # Many-to-many relationship
    services = db.relationship('Service', secondary='appointment_services', backref='appointments')

    def __repr__(self):
        return f"<Appointment {self.name} - {self.zipcode}>"

# Association table
appointment_services = db.Table('appointment_services',
    db.Column('appointment_id', String(8), db.ForeignKey('appointment.id'), primary_key=True),
    db.Column('service_id', String(8), db.ForeignKey('service.id'), primary_key=True)
)

