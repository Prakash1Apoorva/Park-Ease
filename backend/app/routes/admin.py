from flask import Blueprint, request, jsonify, render_template
from app.extensions import db
from sqlalchemy import func
from app.models import User, ParkingLot, ParkingSpot
from .auth import role_required # We import our custom decorator
from app.models import User, ParkingLot, ParkingSpot, Reservation # Add Reservation
import math # Add math
from weasyprint import HTML
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')


# ----------------- Parking Lot Management -----------------

@admin_bp.route('/lots', methods=['POST'])
@role_required('admin')
def create_parking_lot():
    """Admin: Creates a new parking lot and auto-generates its spots."""
    data = request.get_json()
    
    required_fields = ['prime_location_name', 'price', 'address', 'pin_code', 'number_of_spots']
    if not all(field in data for field in required_fields):
        return jsonify({"msg": "Missing required fields"}), 400
    
    # --- ADDED VALIDATION ---
    try:
        price = float(data['price'])
        number_of_spots = int(data['number_of_spots'])
        if price <= 0:
            return jsonify({"msg": "Price must be a positive number."}), 400
        if number_of_spots <= 0:
            return jsonify({"msg": "Number of spots must be a positive integer."}), 400
    except (ValueError, TypeError):
        return jsonify({"msg": "Price and number of spots must be valid numbers."}), 400
    # --- END OF VALIDATION ---

    # Create the lot
    new_lot = ParkingLot(
        prime_location_name=data['prime_location_name'],
        price=data['price'],
        address=data['address'],
        pin_code=data['pin_code'],
        number_of_spots=data['number_of_spots']
    )
    db.session.add(new_lot)
    db.session.flush() # Use flush to get the new_lot.id before committing

    # Auto-generate parking spots for this lot
    for i in range(1, data['number_of_spots'] + 1):
        spot = ParkingSpot(spot_number=i, lot_id=new_lot.id)
        db.session.add(spot)
        
    db.session.commit()
    
    return jsonify({"msg": f"Parking lot '{new_lot.prime_location_name}' and its {new_lot.number_of_spots} spots created."}), 201

@admin_bp.route('/lots', methods=['GET'])
@role_required('admin')
def get_all_lots():
    """Admin: Retrieves a list of all parking lots."""
    lots = ParkingLot.query.all()
    lots_data = []
    for lot in lots:
        lots_data.append({
            "id": lot.id,
            "prime_location_name": lot.prime_location_name,
            "price": lot.price,
            "address": lot.address,
            "pin_code": lot.pin_code,
            "number_of_spots": lot.number_of_spots,
            "occupied_spots": lot.spots.filter_by(status='O').count(),
            "available_spots": lot.spots.filter_by(status='A').count()
        })
    return jsonify(lots_data)

@admin_bp.route('/lots/<int:lot_id>', methods=['GET'])
@role_required('admin')
def get_lot_details(lot_id):
    """Admin: Retrieves details for a specific lot, including spot status."""
    lot = ParkingLot.query.get_or_404(lot_id)
    spots = ParkingSpot.query.filter_by(lot_id=lot.id).order_by(ParkingSpot.spot_number).all()
    
    lot_data = {
        "id": lot.id,
        "prime_location_name": lot.prime_location_name,
        "price": lot.price,
        "address": lot.address,
        "pin_code": lot.pin_code,
        "spots": [{"id": spot.id, "spot_number": spot.spot_number, "status": spot.status} for spot in spots]
    }
    return jsonify(lot_data)


@admin_bp.route('/lots/<int:lot_id>', methods=['PUT'])
@role_required('admin')
def update_parking_lot(lot_id):
    """Admin: Updates a parking lot's details."""
    lot = ParkingLot.query.get_or_404(lot_id)
    data = request.get_json()

    lot.prime_location_name = data.get('prime_location_name', lot.prime_location_name)
    lot.price = data.get('price', lot.price)
    lot.address = data.get('address', lot.address)
    lot.pin_code = data.get('pin_code', lot.pin_code)

    # Note: Handling number_of_spots change is complex and deferred as per standard project flows.
    # A simple update is provided here. The project statement implies this logic can be complex.
    # For this milestone, we will not handle adding/deleting spots on update.
    
    db.session.commit()
    return jsonify({"msg": "Parking lot updated successfully."})


@admin_bp.route('/lots/<int:lot_id>', methods=['DELETE'])
@role_required('admin')
def delete_parking_lot(lot_id):
    """Admin: Deletes a parking lot only if all its spots are available."""
    lot = ParkingLot.query.get_or_404(lot_id)

    # Check if any spot is occupied
    occupied_spots = lot.spots.filter_by(status='O').count()
    if occupied_spots > 0:
        return jsonify({"msg": "Cannot delete lot. Some parking spots are occupied."}), 400

    db.session.delete(lot)
    db.session.commit()
    return jsonify({"msg": "Parking lot deleted successfully."})


# ----------------- User Management -----------------

@admin_bp.route('/users', methods=['GET'])
@role_required('admin')
def get_all_users():
    """Admin: Retrieves a list of all registered users."""
    users = User.query.filter(User.role != 'admin').all() # Exclude admin
    users_data = [{"id": user.id, "username": user.username} for user in users]
    return jsonify(users_data)

# ----------------- Reservation Management -----------------

@admin_bp.route('/reservations', methods=['GET'])
@role_required('admin')
def get_all_reservations():
    """Admin: Retrieves a list of all reservations in the system."""
    reservations = Reservation.query.order_by(Reservation.parking_timestamp.desc()).all()
    
    history = []
    for res in reservations:
        duration_hours = None
        if res.leaving_timestamp:
            duration = res.leaving_timestamp - res.parking_timestamp
            duration_hours = math.ceil(duration.total_seconds() / 3600)

        history.append({
            "reservation_id": res.id,
            "user_id": res.user_id,
            "username": res.user.username,
            "lot_name": res.spot.lot.prime_location_name,
            "spot_number": res.spot.spot_number,
            "parking_time": res.parking_timestamp.isoformat(),
            "leaving_time": res.leaving_timestamp.isoformat() if res.leaving_timestamp else "Active",
            "duration_hours": duration_hours,
            "cost": res.parking_cost
        })
        
    return jsonify(history)

# ----------------- Analytics -----------------

@admin_bp.route('/analytics/summary', methods=['GET'])
@role_required('admin')
def get_analytics_summary():
    """Admin: Retrieves summary analytics for the dashboard."""
    
    # Key Performance Indicators (KPIs)
    total_revenue = db.session.query(func.sum(Reservation.parking_cost)).filter(Reservation.parking_cost.isnot(None)).scalar() or 0
    total_lots = ParkingLot.query.count()
    total_spots = ParkingSpot.query.count()
    occupied_spots = ParkingSpot.query.filter_by(status='O').count()
    
    # Data for "Revenue by Lot" chart
    revenue_by_lot_data = db.session.query(
        ParkingLot.prime_location_name,
        func.sum(Reservation.parking_cost)
    ).join(ParkingSpot, ParkingLot.id == ParkingSpot.lot_id)\
     .join(Reservation, ParkingSpot.id == Reservation.spot_id)\
     .filter(Reservation.parking_cost.isnot(None))\
     .group_by(ParkingLot.prime_location_name)\
     .order_by(func.sum(Reservation.parking_cost).desc())\
     .all()

    chart_labels = [row[0] for row in revenue_by_lot_data]
    chart_values = [row[1] for row in revenue_by_lot_data]
    
    summary = {
        "kpis": {
            "total_revenue": round(total_revenue, 2),
            "total_lots": total_lots,
            "total_spots": total_spots,
            "occupied_spots_now": occupied_spots
        },
        "revenue_by_lot": {
            "labels": chart_labels,
            "data": chart_values
        }
    }
    
    return jsonify(summary)

@admin_bp.route('/reports/preview/<int:user_id>', methods=['GET'])
@role_required('admin')
def preview_user_report(user_id):
    """Admin: Generates a PDF report preview for a specific user."""
    user = User.query.get_or_404(user_id)

    # For preview purposes, we'll fetch data from the last 30 days
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=30)
    
    reservations_query = Reservation.query.filter(
        Reservation.user_id == user.id,
        Reservation.parking_timestamp >= start_date,
        Reservation.leaving_timestamp.isnot(None)
    ).order_by(Reservation.parking_timestamp.desc()).all()

    reservations_data = []
    total_spent = 0
    for res in reservations_query:
        duration = res.leaving_timestamp - res.parking_timestamp
        duration_hours = math.ceil(duration.total_seconds() / 3600)
        total_spent += res.parking_cost
        reservations_data.append({
            "lot_name": res.spot.lot.prime_location_name,
            "parking_time": res.parking_timestamp,
            "leaving_time": res.leaving_timestamp,
            "duration_hours": duration_hours,
            "cost": res.parking_cost
        })

    # Render the HTML template with the data
    html_out = render_template(
        'report.html', 
        user=user, 
        reservations=reservations_data, 
        total_spent=total_spent,
        report_month=end_date.strftime("%B %Y")
    )

    # Generate PDF
    pdf = HTML(string=html_out).write_pdf()

    # Return the PDF as a response
    return pdf, 200, {
        'Content-Type': 'application/pdf',
        'Content-Disposition': 'inline; filename="report_preview.pdf"'
    }

