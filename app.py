# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import datetime as dt
import numpy as np

#################################################
# Database Setup
#################################################
# Create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Welcome to the Honolulu Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data for the last year."""
    # Calculate the date one year ago from the last date in database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query the date and precipitation for the last year
    precipitation_results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()

    # Convert the query results to a dictionary
    precipitation_dict = {date: prcp for date, prcp in precipitation_results}

    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations."""
    # Query all stations
    stations_results = session.query(Station.station).all()

    # Convert list of tuples into normal list
    stations_list = list(np.ravel(stations_results))

    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return the temperature observations for the previous year."""
    # Calculate the date one year ago from the last date in database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query the date and temperature observations for the last year of the most active station
    tobs_results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()

    # Convert list of tuples into normal list
    tobs_list = list(np.ravel(tobs_results))

    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start(start):
    """Return the min, avg, and max temperatures for a given start date."""
    # Query the min, avg, and max temperatures for dates greater than or equal to the start date
    temp_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    # Convert list of tuples into normal list
    temp_list = list(np.ravel(temp_results))

    return jsonify(temp_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    """Return the min, avg, and max temperatures for a given start-end range."""
    # Query the min, avg, and max temperatures for dates between the start and end dates
    temp_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    # Convert list of tuples into normal list
    temp_list = list(np.ravel(temp_results))

    return jsonify(temp_list)

if __name__ == '__main__':
    app.run(debug=True)

