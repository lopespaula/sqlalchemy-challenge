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
        f"If you want to know about Temperature Observation of the most active station, click here:<br/>"
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

@app.route("/api/v1.0/stations")
def stations():

    results = session.query(Station.station,Station.name).all()
    session.close()

    #Dictionary
    stations_list = []
    for station, name in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        stations_list.append(station_dict)

    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():

    results = session.query(Measurement.date,Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= '2016-08-23').all()
    session.close()

    #Dictionary
    temperature = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        temperature.append(tobs_dict)

    return jsonify(temperature)

@app.route("/api/v1.0/<start>/")
def get_start(start):

    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()

    #Dictionary
    temperature = []
    for min_tobs, max_tobs, avg_tobs in results:
        tobs_dict = {}
        tobs_dict["Min Temp"] = min_tobs    
        tobs_dict["Max Temp"] = max_tobs
        tobs_dict["Avg Temp"] = avg_tobs
        temperature.append(tobs_dict)

    return jsonify(temperature)

@app.route("/api/v1.0/<start>/<end>")
def get_measurments_startend(start, end):

    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()

     #Dictionary
    temperature = []
    for min_tobs, max_tobs, avg_tobs in results:
        tobs_dict = {}
        tobs_dict["Min Temp"] = min_tobs    
        tobs_dict["Max Temp"] = max_tobs
        tobs_dict["Avg Temp"] = avg_tobs
        temperature.append(tobs_dict)

    return jsonify(temperature) 

######################################
if __name__ == '__main__':
    app.run(debug=True)