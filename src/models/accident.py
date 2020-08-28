from iieg import db
import datetime
from enum import Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Hour(Enum):
    zero = '00:01 to 02:00'
    two = '02:01 to 04:00'
    four = '04:01 to 06:00'
    six = '06:01 to 08:00'
    eight = '08:01 to 10:00'
    ten = '10:01 to 12:00'
    twelve = '12:01 to 14:00'
    fourteen = '14:01 to 16:00'
    sixteen = '16:01 to 18:00'
    eighteen= '18:01 to 20:00'
    twenty = '20:01 to 22:00'
    twentytwo = '22:01 to 24:00'
    na = 'N.D.'

class Accident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=True)
    hour = db.Column(db.Enum(Hour), nullable=True)
    
    x = db.Column(db.Float(), nullable=True)
    y = db.Column(db.Float(), nullable=True)
    
    # one to many
    accident_type_id = db.Column(db.Integer, db.ForeignKey('accident_type.id'), nullable=True)
    cause_id = db.Column(db.Integer, db.ForeignKey('cause.id'), nullable=True)
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'), nullable=True)
    
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'), nullable=False)
    
    # one to one
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    car = relationship("Car",back_populates="accident")
    
    detail_id = db.Column(db.Integer, db.ForeignKey('detail.id'), nullable=False)
    detail = relationship("Detail",back_populates="accident")

    affected_id = db.Column(db.Integer, db.ForeignKey('affected.id'), nullable=False)
    affected = relationship("Affected",back_populates="accident")
    

    def __init__(self, date, hour, x, y, place_id, accident_type_id, cause_id, car_id, route_id, detail_id, affected_id):
        self.date = date
        self.hour = hour
        self.x = x
        self.y = y
        self.place_id = place_id
        self.accident_type_id = accident_type_id
        self.cause_id = cause_id
        self.car_id = car_id
        self.route_id = route_id
        self.detail_id = detail_id
        self.affected_id = affected_id

    def __repr__(self):
        return f'<id {self.id}>'
    
    def serialize(self):
        return {
            'id': self.id, 
            'date': self.date,
            'hour': self.hour,
            'x': self.x,
            'y':self.y,
            'place_id': self.place_id,
            'accident_type_id': self.accident_type_id,
            'cause_id': self.cause_id,
            'car_id': self.car_id,
            'route_id': self.route_id,
            'detail_id': self.detail_id,
            'affected_id': self.affected_id
        }