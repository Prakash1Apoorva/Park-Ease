from app.extensions import db

class ParkingSpot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spot_number = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(1), nullable=False, default='A')  # 'A' for Available, 'O' for Occupied
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable=False)

    lot = db.relationship('ParkingLot', back_populates='spots')
    reservations = db.relationship('Reservation', back_populates='spot', lazy='dynamic')

    def __repr__(self):
        return f'<ParkingSpot {self.id} in Lot {self.lot_id}>'
