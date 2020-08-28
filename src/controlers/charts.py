import pandas as pd
from iieg import db
from sqlalchemy import extract  

from models.accident import Accident, Hour
from models.accident_type import Accident_type
from models.affected import Affected, Age_range
from models.brand import Brand
from models.car import Car
from models.car_type import Car_type
from models.cause import Cause
from models.detail import Detail
from models.municipality import Municipality
from models.neighborhood import Neighborhood
from models.place import Place
from models.route import Route
from models.street import Street
from models.subbrand import Subbrand

def injured():
    inj = {
        'label':[],
        'value':[]
    }
    types = Detail.query.with_entities(Detail.injured).distinct()

    for i in types:
        if i[0]:
            inj['value'].append(Detail.query.filter_by(injured=i[0]).count())
            inj['label'].append(i[0])
    return inj

def car_type():
    car = {
        'label':[],
        'value':[]
    }
    types = db.session.query(Car_type.name.distinct().label("name"))

    for i in types:
        car_query = Car_type.query.filter_by(name=i[0]).first()
        car['label'].append(car_query.name)
        car['value'].append(db.session.query(Car).filter_by(car_type_id=car_query.id).count())
    return car

def cause():
    cause_dict = {
        'label':[],
        'count':[]
    }
    
    causes = Cause.query.with_entities(Cause.name).distinct()

    for i in causes:
        if i[0] != 'SIN ELEMENTOS':
            cause = Cause.query.filter_by(name=i[0]).first()
            cause_dict['count'].append(db.session.query(Accident).filter_by(cause_id=cause.id).count())
            cause_dict['label'].append(cause.name)
    return cause_dict

def gender():
    man = db.session.query(Affected).filter_by(gender=True).count()
    woman = db.session.query(Affected).filter_by(gender=False).count()
    return man, woman

def hour():
    hours = []
    for hour in Hour:
        hours.append(db.session.query(Accident).filter_by(hour=hour).count())
    return hours

def age():
    ages = []
    for age in Age_range:
        ages.append(db.session.query(Affected).filter_by(age_range=age).count())
    return ages

def month():
    month = []
    for i in range(1,13):
        month.append(len(db.session.query(Accident).filter(extract('month', Accident.date)==i).all()))
    return month