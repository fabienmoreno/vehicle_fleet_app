from app import db
from datetime import datetime

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_registration = db.Column(db.String(20), nullable=False, unique=True)
    first_registration = db.Column(db.Date, nullable=False)
    owner_name = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(50), nullable=True)
    number_of_seats = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)