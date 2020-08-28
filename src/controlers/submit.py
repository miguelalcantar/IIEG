import pandas as pd

# folder to upload file
UPLOAD_FOLDER = '../data'
# files supported
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def to_catalogs(new_data,db_name):
    """
    1. Reads the catalog, in case of having one already.
    2. Concants the old catalog with new data, becoming
    a new one. BUT RESPECTING OLD ID'S
    3. Saves new catalog csv file overwriting the old one
    4. Returns new catalog with id's"""

    # in case of existing file    
    try:
        # Reading old catalog
        old_catalog = pd.read_csv(f'../catalogs/{db_name}.csv')
        # making sure they are unique and validate them
        validated_data = unique_and_validate(list(old_catalog[db_name]),new_data)
        # converting to dataframe
        catalog = pd.DataFrame({db_name: validated_data})
        # overwriting older file
        catalog.to_csv(f'catalogs/{db_name}.csv',index=False)
        # returning only those new values
        return catalog.iloc[len(old_catalog):]

    # In case of not existing
    except FileNotFoundError:
        validated_data = unique_and_validate([],new_data)
        catalog = pd.DataFrame({
            db_name: validated_data,
            # 'id': range(len(validated_data))
            })

    # writing file
    catalog.to_csv(f'catalogs/{db_name}.csv',index=False)

    return catalog


def validate(a):
    """
    Validate a single value"""
    a = str(a)
    
    if a == '' or a == 'nan':
        return None
    if a == 'N.D' or a == 'N.D.' or a == 'SIN DATOS':
        return 'N.D.'
    if a == 'OTRA' or a == 'OTRO':
        return 'OTRO'

    if not a[0].isalnum():
        a = a[1:]

    a_cp = a
    for i in a_cp:
        if i.isalnum() or i == ' ':
            continue
        a = a.replace(i,'')
    
    return a
    # remove double spaces no valid character: 
    # no alpha numeric, coma, periods, spaces.

def unique_and_validate(a, b):
    """
    Method for concatenating two different lists,
    validating whether their concat has unique values
    and its content is valid"""
    print('old vs new',len(a),len(b))
    for i in b:
        # validate data
        i = validate(str(i))
        # print(i, end = ' ')
        # to list in case of being valid
        if i and i not in a:
            # print(i)
            a.append(i)
    return a


def get_max_length(nombre_csv):
    """
    Get max length of an item in certain catalg"""

    # Read data
    data = pd.read_csv(f'catalogs/{nombre_csv}.csv')
    # List the unique values of the data and convert to string
    m = [str(i) for i in list(data[nombre_csv].unique())]
    # Get the max length
    m_max = max(m,key=len)

    return len(m_max)