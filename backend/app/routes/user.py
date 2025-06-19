from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import User, ParkingLot, ParkingSpot, Reservation
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import math
from sqlalchemy import func


user_bp = Blueprint('user', __name__, url_prefix='/api/user')

@user_bp.route('/lots', methods=['GET'])
@jwt_required()
def get_available_lots():
    """User: Retrieves a list of all parking lots with availability."""
    lots = ParkingLot.query.all()
    lots_data = []
    for lot in lots:
        available_spots = lot.spots.filter_by(status='A').count()
        lots_data.append({
            "id": lot.id,
            "prime_location_name": lot.prime_location_name,
            "price_per_hour": lot.price,
            "address": lot.address,
            "pin_code": lot.pin_code,
            "available_spots": available_spots
        })
    return jsonify(lots_data)

@user_bp.route('/lots/<int:lot_id>/reserve', methods=['POST'])
@jwt_required()
def reserve_spot(lot_id):
    """User: Reserves the first available spot in a given lot."""
    user_id = get_jwt_identity()

    # Business Rule: Check if user already has an active reservation
    active_reservation = Reservation.query.filter_by(user_id=user_id, leaving_timestamp=None).first()
    if active_reservation:
        return jsonify({"msg": "You already have an active reservation."}), 400

    # Find the first available spot in the requested lot
    spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').order_by(ParkingSpot.spot_number).first()
    if not spot:
        return jsonify({"msg": "No available spots in this parking lot."}), 404

    # Update spot status to 'Occupied'
    spot.status = 'O'

    # Create new reservation record
    new_reservation = Reservation(
        user_id=user_id,
        spot_id=spot.id
    )
    db.session.add(new_reservation)
    db.session.commit()

    return jsonify({
        "msg": "Spot reserved successfully!",
        "reservation_id": new_reservation.id,
        "spot_number": spot.spot_number,
        "lot_name": spot.lot.prime_location_name
    }), 201

@user_bp.route('/reservations/<int:reservation_id>/release', methods=['POST'])
@jwt_required()
def release_spot(reservation_id):
    """User: Releases an occupied spot and calculates the cost."""
    user_id = get_jwt_identity()
    
    reservation = Reservation.query.get_or_404(reservation_id)

    # Security Check: Ensure the reservation belongs to the current user
    if str(reservation.user_id) != user_id:
        return jsonify({"msg": "Unauthorized to release this spot."}), 403

    # Business Rule: Ensure the spot hasn't already been released
    if reservation.leaving_timestamp is not None:
        return jsonify({"msg": "This spot has already been released."}), 400

    # Update reservation and spot
    reservation.leaving_timestamp = datetime.utcnow()
    spot = ParkingSpot.query.get(reservation.spot_id)
    spot.status = 'A'

    # Cost Calculation (bridges to Milestone 5)
    duration = reservation.leaving_timestamp - reservation.parking_timestamp
    duration_in_hours = math.ceil(duration.total_seconds() / 3600) # Round up to the next hour
    cost = duration_in_hours * spot.lot.price
    reservation.parking_cost = cost

    db.session.commit()

    return jsonify({
        "msg": "Spot released successfully.",
        "duration_hours": duration_in_hours,
        "total_cost": cost
    })

@user_bp.route('/reservations', methods=['GET'])
@jwt_required()
def get_my_reservations():
    """User: Retrieves their own parking history, including duration."""
    user_id = get_jwt_identity()
    reservations = Reservation.query.filter_by(user_id=user_id).order_by(Reservation.parking_timestamp.desc()).all()
    
    history = []
    for res in reservations:
        # Calculate duration for both completed and active reservations
        duration_hours = None
        if res.leaving_timestamp:
            # For completed reservations
            duration = res.leaving_timestamp - res.parking_timestamp
            duration_hours = math.ceil(duration.total_seconds() / 3600)
        else:
            # For active reservations, show duration so far
            duration = datetime.utcnow() - res.parking_timestamp
            duration_hours = math.ceil(duration.total_seconds() / 3600)

        history.append({
            "reservation_id": res.id,
            "lot_name": res.spot.lot.prime_location_name,
            "spot_number": res.spot.spot_number,
            "parking_time": res.parking_timestamp.isoformat(),
            "leaving_time": res.leaving_timestamp.isoformat() if res.leaving_timestamp else "Active",
            "duration_hours": duration_hours,
            "cost": res.parking_cost
        })
        
    return jsonify(history)

# ----------------- Analytics -----------------

@user_bp.route('/analytics/summary', methods=['GET'])
@jwt_required()
def get_user_analytics():
    """User: Retrieves their personal parking analytics."""
    user_id = get_jwt_identity()

    # KPIs for the user
    total_spent = db.session.query(func.sum(Reservation.parking_cost)).filter(Reservation.user_id == user_id).scalar() or 0
    total_reservations = Reservation.query.filter_by(user_id=user_id).count()

    # Find the user's favorite parking lot
    favorite_lot_query = db.session.query(
        ParkingLot.prime_location_name,
        func.count(Reservation.id).label('reservation_count')
    ).join(ParkingSpot, ParkingLot.id == ParkingSpot.lot_id)\
     .join(Reservation, ParkingSpot.id == Reservation.spot_id)\
     .filter(Reservation.user_id == user_id)\
     .group_by(ParkingLot.prime_location_name)\
     .order_by(func.count(Reservation.id).desc())\
     .first()

    favorite_lot = favorite_lot_query[0] if favorite_lot_query else "N/A"

    summary = {
        "total_spent": round(total_spent, 2),
        "total_reservations": total_reservations,
        "favorite_lot": favorite_lot
    }
    
    return jsonify(summary)
