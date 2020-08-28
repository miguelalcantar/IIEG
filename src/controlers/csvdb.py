from controlers.submit import to_catalogs, validate

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

def csv_to_db(data,db):
    """
    Inserting data columns into the relational database.

    We must validate data format before insert the data and trasnform
    if neccesary."""

    # 1. inserting catalogs

    # Maping between csv names and db names
    catalogs = {
        'causa': 'cause',
        'calle': 'street',
        'cruce': 'street',
        'mun': 'municipality',
        'Colonia': 'neighborhood',
        'marca_bien': 'brand',
        'submarca': 'subbrand',
        'ruta': 'route',
        'tipo_auto': 'car_type',
        'tipo_acc': 'accident_type',
    }
    # iterating over columns:
    for csv_name, table_name in catalogs.items():
        # Saving catalogs and validating them
        print(f'{csv_name}, {table_name}\n-------------------')
        category = to_catalogs(list(data[csv_name].unique()),table_name)
        # For each row:
        for index, row in category.iterrows():
            # Inserting into db
            if insert_values(db=db,table_name=table_name,name=row[table_name]):
                print(table_name,index,row[table_name])
            else:
                print('------------\nUnable to inset\n-------------')

    # 2. For the rest of the tables
    for index,row in data.iterrows():
        # counts
        place_cnt = 0
        # Car
        brand = (Brand.query.filter_by(name=validate(row['marca_bien'])).first() if validate(row['marca_bien']) else None)
        subbrand = (Subbrand.query.filter_by(name=validate(row['submarca'])).first() if validate(row['submarca']) else None)
        car_type = (Car_type.query.filter_by(name=validate(row['tipo_auto'])).first() if validate(row['tipo_auto']) else None)

        ok = insert_values(db=db,table_name='car',
                            model=(validate(row['modelo'])),
                            brand_id=(brand.id if brand else None),
                            subbrand_id=(subbrand.id if subbrand else None),
                            car_type_id=(car_type.id if car_type else None)
                            )
        if ok:
            print('car',row['modelo'],row['marca_bien'],row['submarca'],row['tipo_auto'])
        else:
            print('------------\nUnable to inset\n-------------')
    
        # Place
        municipality = (Municipality.query.filter_by(name=validate(row['mun'])).first() if validate(row['mun']) else None)
        street = (Street.query.filter_by(name=validate(row['calle'])).first() if validate(row['calle']) else None)
        intersection_a = (Street.query.filter_by(name=validate(row['cruce'])).first() if validate(row['cruce']) else None)
        neighborhood = (Neighborhood.query.filter_by(name=validate(row['Colonia'])).first() if validate(row['Colonia']) else None)
        # verify if place is already on db
        place_query = Place.query.filter_by(municipality_id=municipality.id,
                                            street_id=street.id,
                                            neighborhood_id=(neighborhood.id if neighborhood else None)
                                            ).first()
        # in case of being inside already
        if not place_query:
            # insert values
            ok = insert_values(db=db, table_name='place',
                        municipality=(municipality.id if municipality else None),
                        street=(street.id if street else None),
                        intersection_a=(intersection_a.id if intersection_a else None),
                        intersection_b=None,
                        neighborhood=(neighborhood.id if neighborhood else None)
                        )
            if ok:
                print('place',row['mun'],row['calle'],row['cruce'],row['Colonia'])
                place_cnt += 1
            else:
                print('------------\nUnable to inset\n-------------')
        
        # Affected
        # validate data
        if row['sexo'] == 'masculino':
            gender = True
        elif row['sexo'] == 'femenino':
            gender = False
        else:
            gender = None
        # age_range
        age = row['edad'].upper()
        if age == "10 A 19":
            age_range = Age_range.ten
        elif age == "20 A 29":
            age_range = Age_range.twenty
        elif age == "30 A 39":
            age_range = Age_range.thirty
        elif age == "40 A 49":
            age_range = Age_range.forty
        elif age == "50 A 59":
            age_range = Age_range.fifty
        elif age == "60 A 69":
            age_range = Age_range.sixty
        elif age == "70 Y MAS":
            age_range = Age_range.seventy
        elif "N" in age and "D" in age:
            age_range = Age_range.na
        else:
            age_range = "error"
        # inserting values
        ok = insert_values(db=db, table_name='affected',
                            gender=gender,
                            age_range=age_range
                            )
        if ok:
            print('affected',row['sexo'],row['edad'])
        else:
            print('------------\nUnable to inset\n-------------')
      
        # Detail
        belt = (int(validate(row['cinturon'])) if validate(row['cinturon']) and row['cinturon'] != 'N.D.' else None)
        # mejorar condicionales
        if row['alcohol'] == True or row['alcohol'] == 'si':
            alcohol = True
        elif row['alcohol'] == False or row['alcohol'] == 'no':
            alcohol = False
        else:
            alcohol = None
        # other variables
        amount = (int(validate(row['monto'])) if validate(row['monto']) and row['monto'] != 'N.D.' else None)
        injured = validate(row['herido'])
        consec = (int(validate(row['Consec'])) if validate(row['Consec']) and row['Consec'] != 'N.D.' else None)
        conse_g = (int(validate(row['conse_g'])) if validate(row['conse_g']) and row['conse_g'] != 'N.D.' else None)
        conse_m = (int(validate(row['conse_m'])) if validate(row['conse_m']) and row['conse_m'] != 'N.D.' else None)
        conse_sem = (int(validate(row['conse_sem'])) if validate(row['conse_sem']) and row['conse_sem'] != 'N.D.' else None)
        _merge = validate(row['_merge'])
        # inserting
        ok = insert_values(db=db, table_name='detail',
            belt=belt,
            alcohol=alcohol,
            amount=amount,
            injured=injured,
            consec=consec,
            conse_g=conse_g,
            conse_m=conse_m,
            conse_sem=conse_sem,
            _merge=_merge
            )
        if ok:
            print('detail',row['monto'],row['herido'],row['Consec'])
        else:
            print('------------\nUnable to inset\n-------------')
        
        # Accident
        # day
        if len(str(row['dia'])) < 2:
            day = '0'+str(row['dia'])
        else:
            day = str(row['dia'])
        # month
        if row['mes'] == 'enero':
            month = '01'
        elif row['mes'] == 'febrero':
            month = '02'
        elif row['mes'] == 'marzo':
            month = '03'
        elif row['mes'] == 'abril':
            month = '04'
        elif row['mes'] == 'mayo':
            month = '05'
        elif row['mes'] == 'junio':
            month = '06'
        elif row['mes'] == 'julio':
            month = '07'
        elif row['mes'] == 'agosto':
            month = '08'
        elif row['mes'] == 'septiembre':
            month = '09'
        elif row['mes'] == 'octubre':
            month = '10'
        elif row['mes'] == 'noviembre':
            month = '11'
        elif row['mes'] == 'diciembre':
            month = '12'
        else:
            month = 'na'
        # date
        date = f'2019-{month}-{day}'
        # hour
        hour_str = row['Horacerr'].upper()
        # switch case
        if hour_str == '00:01 A 02:00':
            hour = Hour.zero
        elif hour_str == '02:01 A 04:00':
            hour = Hour.two
        elif hour_str == '04:01 A 06:00':
            hour = Hour.four
        elif hour_str == '06:01 A 08:00':
            hour = Hour.six
        elif hour_str == '08:01 A 10:00':
            hour =Hour.eight
        elif hour_str == '10:01 A 12:00':
            hour = Hour.ten
        elif hour_str == '12:01 A 14:00':
            hour = Hour.twelve
        elif hour_str == '14:01 A 16:00':
            hour = Hour.fourteen
        elif hour_str == '16:01 A 18:00':
            hour = Hour.sixteen
        elif hour_str == '18:01 A 20:00':
            hour = Hour.eighteen
        elif hour_str == '20:01 A 22:00':
            hour = Hour.twenty
        elif hour_str == '22:01 A 24:00':
            hour = Hour.twentytwo
        else:
            hour = Hour.na
        # x
        x = row['x']
        # y
        y = row['y']
        # place_id
        if not place_query:
            place_query = Place.query.filter_by(id=place_cnt).first()
        # accident_type_id
        accident_type = (Accident_type.query.filter_by(name=validate(row['tipo_acc'])).first() if validate(row['tipo_acc']) else None)
        # cause_id
        cause = (Cause.query.filter_by(name=validate(row['causa'])).first() if validate(row['causa']) else None)
        # car_id
        print(index, Car.query.filter_by(id=index+1).first())
        car = Car.query.filter_by(id=index+1).first()
        # route_id
        route = (Route.query.filter_by(name=validate(row['ruta'])).first() if validate(row['ruta']) else None)
        # detail_id
        detail = Detail.query.filter_by(id=index+1).first()
        # affected_id
        affected = Affected.query.filter_by(id=index+1).first()
        # inserting values
        ok = insert_values(db=db,table_name='accident',
                            date=date,
                            hour=hour,
                            x=x,
                            y=y,
                            place_id=place_query.id,
                            accident_type_id=(accident_type.id if accident_type else None),
                            cause_id=(cause.id if cause else None),
                            car_id=car.id,
                            route_id=(route.id if route else None),
                            detail_id=detail.id,
                            affected_id=affected.id)
        if ok:
            print(index+1,date,hour,x,y)
        else:
            print('------------\nUnable to inset\n-------------')

def insert_values(db,table_name,**kwargs):

    #Catalogs
    if table_name == 'cause':
        value = Cause(name=kwargs['name'])
   
    elif table_name == 'street':
        value = Street(name=kwargs['name'])
    
    elif table_name == 'municipality':
        value = Municipality(name=kwargs['name'])
    
    elif table_name == 'neighborhood':
        value = Neighborhood(name=kwargs['name'])
    
    elif table_name == 'brand':
        value = Brand(name=kwargs['name'])
    
    elif table_name == 'subbrand':
        value = Subbrand(name=kwargs['name'])
    
    elif table_name == 'route':
        value = Route(name=kwargs['name'])

    elif table_name == 'car_type':
        value = Car_type(name=kwargs['name'])
    
    elif table_name == 'accident_type':
        value = Accident_type(name=kwargs['name'])
    
    # Second level
    elif table_name == 'affected':
        value = Affected(gender=kwargs['gender'],age_range=kwargs['age_range'])
    
    elif table_name == 'detail':
        value = Detail(belt=kwargs['belt'],
                    alcohol=kwargs['alcohol'],
                    amount=kwargs['amount'],
                    injured=kwargs['injured'],
                    consec=kwargs['consec'],
                    conse_g=kwargs['conse_g'],
                    conse_m=kwargs['conse_m'],
                    conse_sem=kwargs['conse_sem'],
                    _merge=kwargs['_merge'])

    elif table_name == 'car':
        value = Car(model=kwargs['model'],
                    brand_id=kwargs['brand_id'],
                    subbrand_id=kwargs['subbrand_id'],
                    car_type_id=kwargs['car_type_id'])
    
    elif table_name == 'place':
        value = Place(municipality_id=kwargs['municipality'],
                    street_id=kwargs['street'],
                    intersection_a_id=kwargs['intersection_a'],
                    intersection_b_id=kwargs['intersection_b'],
                    neighborhood_id=kwargs['neighborhood'])
    
    # main
    elif table_name == 'accident':
        value = Accident(date=kwargs['date'],
                        hour=kwargs['hour'],
                        x=kwargs['x'],
                        y=kwargs['y'],
                        place_id=kwargs['place_id'],
                        accident_type_id=kwargs['accident_type_id'],
                        cause_id=kwargs['cause_id'],
                        car_id=kwargs['car_id'],
                        route_id=kwargs['route_id'],
                        affected_id=kwargs['affected_id'],
                        detail_id=kwargs['detail_id'])
    
    else:
        return False
    
    db.session.add(value)
    db.session.commit()

    return True