from iieg import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(10), nullable=True)
    
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=True)
    brand = db.relationship('Brand', foreign_keys=[brand_id])

    subbrand_id = db.Column(db.Integer, db.ForeignKey('subbrand.id'), nullable=True)
    subbrand = db.relationship('Subbrand', foreign_keys=[subbrand_id])

    car_type_id = db.Column(db.Integer, db.ForeignKey('car_type.id'), nullable=True)
    car_type = db.relationship('Car_type', foreign_keys=[car_type_id])

    accident = db.relationship('Accident', uselist=False)

    def __init__(self, model, brand_id, subbrand_id, car_type_id):
        self.model = model
        self.brand_id = brand_id
        self.subbrand_id = subbrand_id
        self.car_type_id = car_type_id

    def __repr__(self):
        return f'<id {self.id}>'
    
    def serialize(self):
        return {
            'id': self.id, 
            'model': self.model,
            'brand_id': self.brand_id,
            'subbrand_id': self.subbrand_id,
            'car_type_id': self.car_type_id
        }