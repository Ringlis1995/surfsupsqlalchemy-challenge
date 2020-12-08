##had assistance from TA on parts of this assignment
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt

#database setup
engine = create_engine("sqlite:///hawaii.sqlite")

#reflect db
Base = automap_base()
#reflect tables
Base.prepare(engine, reflect=True)

#save reference to table
Measurement = Base.classes.measurement
Station = Base.classes.station


app = Flask(__name__)

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()

    #convert to normal lists
    stations_list = list(np.ravel(results))
    return jsonify(stations_list)


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine) # Rose: Add this line here
	
    results = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= "08-23-2017").all()
    session.close() # Rose: Add this line here
    year_prcp = list(np.ravel(results))
	#results.___dict___
     
    return jsonify(year_prcp)

@app.route("/api/v1.0/tobs")
def temperature():
	
    session = Session(engine)
    most_active = 'USC00519281'
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == most_active).\
        filter(Measurement.date >= "08-23-2017").all()

    session.close()
    
    year_tobs = list(np.ravel(results))

    return jsonify(year_tobs)



if __name__ == '__main__':
    app.run(debug=True)

