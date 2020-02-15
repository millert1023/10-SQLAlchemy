
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

#weather app
app = Flask(__name__)

#List available routes:
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"/api/v1.0/precipitation<br>"
		f"/api/v1.0/stations<br>"
		f"/api/v1.0/tobs<br>"
		f"/api/v1.0/<start><br>"
		f"/api/v1.0<start>/<end><br>"
    )

#Precipitation Route -- Query for the dates and temperature observations from the last year.
@app.route("/api/v1.0/precipitation")
def precipitation():
	latest_date = (session.query(Measurement.date).order_by(Measurement.date.desc()).first())
    latest_date = list(np.ravel(latest_date))[0]
    latest_date = dt.datetime.strptime(latest_date, "%Y-%m-%d")
    late_yr = int(dt.datetime.strftime(latest_date, "%Y"))
    late_mo = int(dt.datetime.strftime(latest_date, "%m"))
    late_day = int(dt.datetime.strftime(latest_date, "%d"))
                                   
    prev_year = dt.date(late_yr,late_mo,late_day) - dt.timedelta(days=365)

    results = (session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>prev_year).order_by(Measurement.date).all())

    precp = list(np.ravel(results))
#Create a dictionary using 'date' as the key and 'prcp' as the value.
	precp = []
	for result in results:
		row = {}
		row[Measurements.date] = row[Measurements.prcp]
		precp.append(row)

	return jsonify(precp)

#Station Route -- return a json list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Stations.station).all()

	all_stations = list(np.ravel(results))

	return jsonify(all_stations)

#Temperature -- Return a json list of Temperature Observations (tobs) for the previous year
@app.route("/api/v1.0/tobs")
def temperature():
    year_tobs = []
    results = (session.query(Measurement.tobs,Measurement.date).filter(Measurement.date>prev_year).\
            filter(Measurement.station == station_id).order_by(Measurement.date).all())

    year_tobs = list(np.ravel(results))

	return jsonify(year_tobs)

#Start Date Only -- Calculate TMIN, TAVG, TMAX
@app.route("/api/v1.0/<start>")
def start_trip(start_date):
	start_trip = []

	results_min = session.query(func.min(Measurements.tobs)).filter(Measurements.date >= start_date).all()
	results_max = session.query(func.max(Measurements.tobs)).filter(Measurements.date >= start_date).all()
	results_avg = session.query(func.avg(Measurements.tobs)).filter(Measurements.date >= start_date).all()

	start_trip_date = list(np.ravel(results_min,results_max, results_avg))

	return jsonify(start_trip_date)
    
#Round Trip -- Calculate TMIN, TAVG, TMAX
@app.route("/api/v1.0/<start>/<end>")

def start_end_trip(start_date, end_date):

	round_trip_temps = []

	results_min = session.query(func.min(Measurements.tobs)).filter(Measurements.date >= start_date, Measurements.date >= end_date).all()
	results_max = session.query(func.max(Measurements.tobs)).filter(Measurements.date >= start_date, Measurements.date >= end_date).all()
	results_avg = session.query(func.avg(Measurements.tobs)).filter(Measurements.date >= start_date, Measurements.date >= end_date).all()

	round_trip_temps = list(np.ravel(results_min,results_max, results_avg))

	return jsonify(round_trip_temps)


if __name__ == '__main__':
    app.run(debug=True)