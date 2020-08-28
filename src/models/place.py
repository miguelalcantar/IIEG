from iieg import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    municipality_id = db.Column(db.Integer, db.ForeignKey('municipality.id'), nullable=False)
    municipality = db.relationship("Municipality", foreign_keys=[municipality_id])
    
    intersection_a_id = db.Column(db.Integer, db.ForeignKey('street.id'), nullable=True)
    intersection_a = db.relationship("Street", foreign_keys=[intersection_a_id])
    
    intersection_b_id = db.Column(db.Integer, db.ForeignKey('street.id'), nullable=True)
    intersection_b = db.relationship("Street", foreign_keys=[intersection_b_id])
    
    street_id = db.Column(db.Integer, db.ForeignKey('street.id'), nullable=False)
    street = db.relationship("Street", foreign_keys=[street_id])
    
    neighborhood_id = db.Column(db.Integer, db.ForeignKey('neighborhood.id'), nullable=True)
    neighborhood = db.relationship("Neighborhood", foreign_keys=[neighborhood_id])

    def __init__(self, municipality_id, intersection_a_id, intersection_b_id, street_id, neighborhood_id):
        self.municipality_id = municipality_id
        self.intersection_a_id = intersection_a_id
        self.intersection_b_id = intersection_b_id
        self.street_id = street_id
        self.neighborhood_id = neighborhood_id

    def __repr__(self):
        return f'<id {self.id}>'
    
    def serialize(self):
        return {
            'id': self.id, 
            'municipality_id': self.municipality_id,
            'intersection_a': self.intersection_a,
            'intersection_b': self.intersection_b,
            'street_id': self.street_id,
            'neigborhood_id': self.neigborhood_id
        }