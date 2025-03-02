from flask import request, jsonify
from app import app, db
from app.models import Vehicle
from datetime import datetime

# Helper function to serialize Vehicle objects
def serialize_vehicle(vehicle):
    return {
        "id": vehicle.id,
        "car_registration": vehicle.car_registration,
        "first_registration": vehicle.first_registration.strftime('%Y-%m-%d'),
        "owner_name": vehicle.owner_name,
        "color": vehicle.color,
        "number_of_seats": vehicle.number_of_seats
    }

@app.route('/add_vehicle', methods=['POST'])
def add_vehicle():
    data = request.get_json()
    required_fields = ['car_registration', 'first_registration', 'owner_name']

    # Check for missing required fields
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

    # Validate date format
    try:
        first_registration = datetime.strptime(data['first_registration'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"error": "Invalid date format, expected YYYY-MM-DD"}), 400

    # Validate number_of_seats if provided
    number_of_seats = data.get('number_of_seats')
    if number_of_seats is not None:
        if not isinstance(number_of_seats, int) or number_of_seats <= 0:
            return jsonify({"error": "number_of_seats must be a positive integer"}), 400

    # Check for duplicate car registration
    if Vehicle.query.filter_by(car_registration=data['car_registration']).first():
        return jsonify({"error": "Vehicle with this car registration already exists"}), 409

    # Create and add new vehicle
    new_vehicle = Vehicle(
        car_registration=data['car_registration'],
        first_registration=first_registration,
        owner_name=data['owner_name'],
        color=data.get('color'),
        number_of_seats=number_of_seats
    )
    db.session.add(new_vehicle)
    db.session.commit()

    return jsonify({"id": new_vehicle.id, "message": "Vehicle added successfully"}), 201

@app.route('/get_vehicle/<int:vehicle_id>', methods=['GET'])
def get_vehicle_by_id(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404
    return jsonify(serialize_vehicle(vehicle))

@app.route('/get_vehicle_by_registration/<string:car_registration>', methods=['GET'])
def get_vehicle_by_registration(car_registration):
    vehicle = Vehicle.query.filter_by(car_registration=car_registration).first()
    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404
    return jsonify(serialize_vehicle(vehicle))
