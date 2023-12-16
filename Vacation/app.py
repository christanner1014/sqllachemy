# Import the dependencies
from flask import Flask, jsonify
import datetime as dt
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

# Create the engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect the database
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Create Flask app
app = Flask(__name__)

# Define routes
@app.route("/")
def home():
    """Homepage."""
    return (
        f"Welcome to the Hawaii Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start_date> (enter start_date in YYYY-MM-DD format)<br/>"
        f"/api/v1.0/<start_date>/<end_date> (enter start_date and end_date in YYYY-MM-DD format)"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Convert the query results to a dictionary using date as the key and prcp as the value."""
    # Perform the query to retrieve the precipitation data
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-23").all()

    # Create a list of dictionaries with date and prcp as keys
    precipitation_data = [{"date": date, "prcp": prcp} for date, prcp in results]

    # Return the JSON representation of the list of dictionaries
    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""
    # Perform the query to retrieve the list of stations
    results = session.query(Station.station).all()

    # Convert the query results to a list
    station_list = [station[0] for station in results]

    # Return the JSON representation of the list
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """Query the dates and temperature observations of the most-active station for the previous year of data."""
    # Perform the query to retrieve the temperature observations
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= "2016-08-23").all()

    # Create a list of dictionaries with date and tobs as keys
    tobs_data = [{"date": date, "tobs": tobs} for date, tobs in results]

    # Return the JSON representation of the list of dictionaries
    return jsonify(tobs_data)

@app.route("/api/v1.0/<start_date>")
def start_date(start_date):
    """Return a JSON list of the minimum temperature, average temperature, and maximum temperature for dates greater than or equal to the start date."""
    # Perform the query to calculate TMIN, TAVG, and TMAX
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

    # Create a dictionary with the temperature statistics
    temperature_stats = {
        "min_temperature": results[0][0],
        "avg_temperature": results[0][1],
        "max_temperature": results[0][2]
    }
    #EXAMPLE: http://127.0.0.1:5000/api/v1.0/2016-10-14
    # Return the JSON representation of the dictionary
    return jsonify(temperature_stats)

@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end_date(start_date, end_date):
    """Return a JSON list of the minimum temperature, average temperature, and maximum temperature for dates within the specified range."""
    # Perform the query to calculate TMIN, TAVG, and TMAX
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    # Create a dictionary with the temperature statistics
    temperature_stats = {
        "min_temperature": results[0][0],
        "avg_temperature": results[0][1],
        "max_temperature": results[0][2]
    }
    #EXAMPLE: http://127.0.0.1:5000/api/v1.0/2016-10-14/2017-10-15
    # Return the JSON representation of the dictionary
    return jsonify(temperature_stats)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)