from app.extensions import db

class ParkingLot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prime_location_name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False) # Price per hour
    address = db.Column(db.String(200), nullable=False)
    pin_code = db.Column(db.String(10), nullable=False)
    number_of_spots = db.Column(db.Integer, nullable=False)
    
    spots = db.relationship('ParkingSpot', back_populates='lot', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<ParkingLot {self.prime_location_name}>'
