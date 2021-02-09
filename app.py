import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import os
import sys

#####################################
# Database setup 
#####################################
engine = create_engine("sqlite:///hawaii.sqlite", echo=False)

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)
######################################
# Flask setup 
######################################
app = Flask(__name__)

#####################################
# Flask Routes 
#####################################
@app.route("/")
def welcome():
    print("List all available api routes:")
    return (
        f"Welcome to the Hawaii Climate API<br/>"
        f"<br/>"
        f"<br/>"
        f"If you want to know about Precipitation Data, click here:<br/>"
        f"<a href='/api/v1.0/precipitation' target='_blank'>/api/v1.0/precipitation</a><br/>"
        f"<br/>"
        f"If you want to know about Stations, click here:<br/>"
        f"<a href='/api/v1.0/stations' target='_blank'>/api/v1.0/stations</a><br />"
        f"<br/>"
        f"If you want to know about Temperature Observation, click here:<br/>"
        f"<a href='/api/v1.0/tobs' target='_blank'>/api/v1.0/tobs</a><br />"
        f"<br/>"
        f"If you want to know about Minimum, Maximum and Average Temperatures a given start date, click here:<br/>"
        f"<a href='/api/v1.0/&lt;start&gt;' target='_blank'>/api/v1.0/&lt;start&gt;</a><br />"
        f"<br/>"
        f"And if you want to know about Minimum, Maximum and Average Temperatures for a given start and end date, click here:<br/>"
        f"<a href='/api/v1.0/&lt;end&gt;' target='_blank'>/api/v1.0/&lt;start&gt;/&lt;end&gt;</a>"
        
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    #Dictionary
    precipitations = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp 
        precipitations.append(prcp_dict) 
       
    return jsonify(precipitations)














######################################
if __name__ == '__main__':
    app.run(debug=True)