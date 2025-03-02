from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__)

# Build the database URI from environment variables
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')
DB_HOST = os.environ.get('DB_HOST', 'postgres')  # This should match the service name or IP of your PostgreSQL container
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_NAME = os.environ.get('DB_NAME', 'fleetdb')

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_registration = db.Column(db.String(20), unique=True, nullable=False)
    date_first_registration = db.Column(db.Date, nullable=False)
    owner_name = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(50))
    number_of_seats = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def as_dict(self):
        return {
            "id": self.id,
            "car_registration": self.car_registration,
            "date_first_registration": self.date_first_registration.isoformat(),
            "owner_name": self.owner_name,
            "color": self.color,
            "number_of_seats": self.number_of_seats,
            "created_at": self.created_at.isoformat()
        }

# Endpoint to add a new vehicle
@app.route('/vehicles', methods=['POST'])
def add_vehicle():
    data = request.get_json()
    # Check mandatory fields
    for field in ['car_registration', 'date_first_registration', 'owner_name']:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    # Validate and parse the date
    try:
        date_first_registration = datetime.strptime(data['date_first_registration'], "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid date format for date_first_registration. Use YYYY-MM-DD."}), 400

    # Validate number_of_seats if provided
    number_of_seats = None
    if 'number_of_seats' in data:
        try:
            number_of_seats = int(data['number_of_seats'])
            if number_of_seats <= 0:
                raise ValueError
        except ValueError:
            return jsonify({"error": "number_of_seats must be a positive integer"}), 400

    vehicle = Vehicle(
        car_registration=data['car_registration'],
        date_first_registration=date_first_registration,
        owner_name=data['owner_name'],
        color=data.get('color'),
        number_of_seats=number_of_seats
    )

    try:
        db.session.add(vehicle)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Vehicle could not be added", "details": str(e)}), 500

    return jsonify(vehicle.as_dict()), 201

# Endpoint to get vehicle by id
@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle_by_id(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404
    return jsonify(vehicle.as_dict()), 200

# Endpoint to get vehicle by car registration
@app.route('/vehicles/registration/<car_reg>', methods=['GET'])
def get_vehicle_by_registration(car_reg):
    vehicle = Vehicle.query.filter_by(car_registration=car_reg).first()
    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404
    return jsonify(vehicle.as_dict()), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates tables if they do not exist
    app.run(host='0.0.0.0', port=5000)
