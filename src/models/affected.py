from iieg import db
from enum import Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Age_range(Enum):
    ten = '10 A 19',
    twenty = '20 A 29',
    thirty = '30 A 39',
    forty = '40 A 49',
    fifty = '50 A 59',
    sixty = '60 A 69',
    seventy = '70 Y MAS',
    na = 'N.D.'

class Affected(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.Boolean(), nullable=True)
    age_range = db.Column(db.Enum(Age_range), nullable=True)
    accident = db.relationship('Accident', uselist=False)

    def __init__(self, gender, age_range):
        self.gender = gender
        self.age_range = age_range

    def __repr__(self):
        return f'<id {self.id}>'
    
    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'age_range': self.age_range
        }