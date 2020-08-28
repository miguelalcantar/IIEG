from iieg import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Detail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    belt = db.Column(db.SmallInteger, nullable=True)
    alcohol = db.Column(db.Boolean, nullable=True)
    amount = db.Column(db.Integer, nullable=True)
    injured = db.Column(db.String(10), nullable=True)
    consec = db.Column(db.Integer, nullable=True)
    conse_g = db.Column(db.Integer, nullable=True)
    conse_m = db.Column(db.Integer, nullable=True)
    conse_sem = db.Column(db.Integer, nullable=False)
    _merge = db.Column(db.String(15), nullable=True)
    accident = db.relationship('Accident', uselist=False)

    def __init__(self, belt, alcohol, amount, injured, consec, conse_g, conse_m, conse_sem, _merge):
        self.belt = belt
        self.alcohol = alcohol
        self.amount = amount
        self.injured = injured
        self.consec = consec
        self.conse_g = conse_g
        self.conse_m = conse_m
        self.conse_sem = conse_sem
        self._merge = _merge

    def __repr__(self):
        return f'<id {self.id}>'
    
    def serialize(self):
        return {
            'id': self.id, 
            'belt': self.belt,
            'amount': self.amount,
            'injured': self.injured,
            'consec': self.consec,
            'conse_g': self.conse_g,
            'conse_m': self.conse_m,
            'conse_sem': self.conse_sem,
            '_merge': self._merge
        }