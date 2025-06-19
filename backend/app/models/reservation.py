from app.extensions import db
from datetime import datetime

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parking_timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    leaving_timestamp = db.Column(db.DateTime, nullable=True)
    parking_cost = db.Column(db.Float, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'), nullable=False)
    
    user = db.relationship('User', back_populates='reservations')
    spot = db.relationship('ParkingSpot', back_populates='reservations')

    def __repr__(self):
        return f'<Reservation {self.id}>'
