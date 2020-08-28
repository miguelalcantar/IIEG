import os
from flask import Flask, flash, request, redirect, url_for, render_template
from flask import send_from_directory
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from flask import request
from flask import jsonify
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# handle db transactions
db = SQLAlchemy(app)

from controlers.submit import allowed_file
from controlers.csvdb import csv_to_db

@app.route('/submit', methods=['GET', 'POST'])
def my_form():
    if request.method == "POST":
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # saving file (temporaly while its saved into the db)
            file.save(os.path.join('data/', filename))
            # inserting data into the db
            csv_to_db(data=pd.read_csv("data/data.csv"),db=db)
            # return redirect(url_for('uploaded_file',
                                    # filename=filename))
    return render_template('submit.html')

# ----------------------
from controlers.charts import gender, month, hour, age, car_type, cause, injured
from controlers.maps import get_xy

api = Api(app)

parser = reqparse.RequestParser()

class Maps(Resource):
    def get(self):
        return {
            'status':True,
            'data': {
                'points':get_xy()
            }
        }

api.add_resource(Maps, '/maps')


class Graphs(Resource):
    def get(self):
        return {
            'status': True,
            'data': {'gender':gender(),
                    'month':month(),
                    'hour':hour(),
                    'age':age(),
                    'car_type':car_type(),
                    'cause':cause(),
                    'injured':injured()}
        }

api.add_resource(Graphs, '/charts')