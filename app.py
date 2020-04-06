from flask import Flask,jsonify
import datetime as dt 
import numpy as np
import pandas as pd 
import datetime
import sqlalchemy 
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

#databse set-up
engine=create_engine(f"sqlite:///Resources/hawaii.sqlite")
Base=automap_base()
Base.prepare(engine,reflect=True)

#DB called passenger
Measurement=Base.classes.measurement
Station=Base.classes.station

#set up flask root
app=Flask(__name__)
@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"//api/v1.0/<start>/<end>"
        )

#/api/v1.0/precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    session=Session(engine)
    results=session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    all_results=[]
    for Date, Prcp in results:
        precipitation_dict={}
        precipitation_dict['Date']=Date
        precipitation_dict['Prcp']=Prcp
        all_results.append(precipitation_dict)
    return jsonify(all_results)

#/api/v1.0/stations
@app.route("/api/v1.0/stations")
def stations():
    session=Session(engine)
    results=session.query(Station.station,Station.name).all()
    session.close()
    all_results=[]
    for a, b in results:
        ststindict={}
        ststindict['Station Name']=a
        ststindict['Name']=b
        all_results.append(ststindict)
    return jsonify(all_results)

#/api/v1.0/tobs
@app.route("/api/v1.0/tobs")
def tobs():
    session=Session(engine)
    results = session.query(Measurement.date,Measurement.tobs).filter(Measurement.station=='USC00519281').filter(Measurement.date>'2016-08-22').all()
    session.close()
    all_results=[]
    for Date, tobs in results:
        tobs_dict={}
        tobs_dict['Date']=Date
        tobs_dict['tobs']=tobs
        all_results.append(tobs_dict)
    return jsonify(all_results)

#/api/v1.0/<start>
@app.route("/api/v1.0/<start>")
def Date(start):
    start=datetime.datetime.strptime(start, "%Y-%m-%d").date()
    session=Session(engine)
    results=session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date>start).all()
    session.close()
    all_results=[]
    for TMIN, TMAX, TAVG in results:
        tem_dict={}
        tem_dict['TMIN']=TMIN
        tem_dict['TMAX']=TMAX
        tem_dict['TAVG']=TAVG
        all_results.append(tem_dict)
    return jsonify(all_results)

# /api/v1.0/<start>/<end>
@app.route("/api/v1.0/<start>/<end>")
def Double(start,end):
    start=datetime.datetime.strptime(start, "%Y-%m-%d").date()
    end=datetime.datetime.strptime(end, "%Y-%m-%d").date()
    session=Session(engine)
    results=session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date>start).filter(Measurement.date<end).all()
    session.close()
    all_results=[]
    for TMIN, TMAX, TAVG in results:
        tem_dict={}
        tem_dict['TMIN']=TMIN
        tem_dict['TMAX']=TMAX
        tem_dict['TAVG']=TAVG
        all_results.append(tem_dict)
    return jsonify(all_results)

##end##
if __name__=="__main__":
    app.run(debug=True)
