
#################################################
# Import Modules and Dependencies 
#################################################

from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import numpy as np
import datetime as dt

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Database Setup
#################################################

engine = create_engine('sqlite:///Resources/hawaii.sqlite')

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Welcome Page : Flask Available Routes
#################################################

@app.route("/")
def welcome():
    ## List all available routes
    return (
        f'Welcome to the Hawaii Climate App, a Flask API<br/>'
        f'<br/>'
        f'Available routes:<br/>'
        f'<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/2016-06-28<br/>'
        f'/api/v1.0/2016-06-28/2016-07-10'
    ) 
#################################################
# Precipitation Route 
#################################################

# Define what to do when a user hits /precipitation route 

@app.route("/api/v1.0/precipitation")
def precipitation(): 

    # Calculate the date 1 year ago from the last data point in the database
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    # Perform a query to retrieve the data and precipitation scores
    prcp_data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > one_year_ago).\
    order_by(Measurement.date).all()

    # Create a dictionary from query and append to a list of dates and preciptation route
    all_prcp= []
    for date, prcp in prcp_data:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)
    # Return JSON List 
    return jsonify(all_prcp)

#################################################
# Stations Route 
#################################################

# Define what to do when a user hits /stations route 
@app.route("/api/v1.0/stations")
def stations(): 

    # Query for Stations
    stations = session.query(Station.station, Station.name).all()

    # Create a dictionary from the query and append to a list of all the Stations
    all_stations= []
    for station, name in stations:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        all_stations.append(station_dict)
    # Return JSON List 
    return jsonify(all_stations)

#################################################
# Tobs Route 
#################################################

# Define what to do when a user hits /tobs route 
@app.route("/api/v1.0/tobs")
def tobs(): 

    # Calculate the date 1 year ago from the last data point in the database
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    # Query for Tobs
    tobs_query = session.query(Measurement.date,Measurement.tobs).\
    filter(Measurement.date >= one_year_ago).\
    order_by(Measurement.date).all()

    # Create a dictionary from the query and append to a list of dates and tobs
    all_tobs= []
    for date, tobs in tobs_query:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)
    # Return JSON List 
    return jsonify(all_tobs)

#################################################
#  <start> Route
#################################################

# Define what to do when a user hits /<start>
@app.route("/api/v1.0/<start>")
def start_day(start):
        # Query for the dates and min/avg/max tobs that are equal or greater to the start date given 
        start_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                group_by(Measurement.date).all()

        # Convert query into a List
        start_day_list = list(start_day)
        # Return JSON List 
        return jsonify(start_day_list)

#################################################
#  <start>/<end> Route
#################################################

# Define what to do when a user hits /<start>
@app.route("/api/v1.0/<start>/<end>")
def start_end_day(start, end):
        # Query for min/avg/max tobs  for dates between the start and end date given
        start_end_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).\
                group_by(Measurement.date).all()
        # Convert query into a List
        start_end_day_list = list(start_end_day)
        # Return JSON List 
        return jsonify(start_end_day_list)

if __name__ == "__main__": 
    app.run(debug=True)