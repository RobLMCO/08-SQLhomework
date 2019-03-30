import numpy as np
import pandas as pd

import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite?check_same_thread=False")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/year-month-day<br/>"
        f"/api/v1.0/start_end/year-month-day/year-month-day<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # 1 year ago data point
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > last_year).\
    order_by(Measurement.date).all()
    precipitation_df=pd.DataFrame(precipitation_data)
    precipitation_dict = precipitation_df.to_dict()

    return jsonify(precipitation_dict)


@app.route("/api/v1.0/stations")
def stations():
    stations_data = session.query(Measurement.station).all()
    
    return jsonify(stations_data)

@app.route("/api/v1.0/tobs")
def tobs():
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temperature_data = session.query(Measurement.station,Measurement.date, Measurement.tobs).\
    filter(Measurement.date > last_year).\
    order_by(Measurement.date).all()
    temperatures_df=pd.DataFrame(temperature_data)
    temperatures_dict = temperatures_df.to_dict()
    return jsonify(temperatures_dict)

@app.route("/api/v1.0/start/<start>")
def start(start):
    start_date = start
    startdate_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    return jsonify(startdate_data)

@app.route("/api/v1.0/start_end/<start>/<end>")
def startend(start,end):
    start_date = start
    end_date = end
    startenddates_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    return jsonify(startenddates_data)

if __name__ == '__main__':
    app.run(debug=True)
