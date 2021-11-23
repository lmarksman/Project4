import os
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
from sqlalchemy.ext.automap import automap_base
from datetime import date
import sqlalchemy as sa
from datetime import datetime
import pickle

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
from sqlalchemy.sql.expression import extract
from sqlalchemy.sql.schema import Index

from config import password
# connection_string = f"postgres:{password}@localhost:5432/Tornado"
# engine = create_engine(f'postgresql://{connection_string}')
engine = create_engine("postgresql://postgres:postgres@localhost:5432/tornado")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

print(Base.classes.keys())

data = Base.classes.tornado_data

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#--------------------------------------------
# create route that renders HTML templates
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():

    return render_template("about.html")

@app.route("/charts")
def charts():

    return render_template("charts.html")

@app.route("/maps")
def maps():

    return render_template("maps.html")

@app.route("/frequency")
def frequency():

    return render_template("frequency.html")
#------------------------------------------
@app.route("/model" , methods=["POST"])
def model():

    Month = datetime.now().month
    Magnitude = request.form["magnitude"]
    Injuries = 2.4
    Fatalities = 0.15
    Crop_Loss = 0.003

    Length = request.form["length"]
    if Length == "":
        Length = 4.71
    Length = float(Length)

    Width = request.form["width"]
    if Width == "":
        Width = 124

    zipcode = request.form["zipcode"]
    if zipcode == "":
        zipcode = 67846.0
    zipcode = float(Width)

    Income = 56221.0
    Pop_Density = 462.39

    prediction = 0

    X = [[Month, Magnitude, Injuries, Fatalities, Crop_Loss, Length, Width, Income, Pop_Density, zipcode]]

    print(X)

    filename = './data/tornado_model.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    prediction = loaded_model.predict(X)[0][0]

    prediction = "${0:,.2f}".format(prediction)

    print(prediction)

    return render_template("index.html", prediction = prediction)





    

if __name__ == "__main__":
    app.run()

    