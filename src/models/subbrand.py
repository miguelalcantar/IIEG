from iieg import db
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Subbrand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<id {self.id}>'
    
    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name
        }