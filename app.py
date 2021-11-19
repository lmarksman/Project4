import os
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
from sqlalchemy.ext.automap import automap_base
from datetime import date
import sqlalchemy as sa

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

#------------------------------------------
#API Routes




    

if __name__ == "__main__":
    app.run()

    