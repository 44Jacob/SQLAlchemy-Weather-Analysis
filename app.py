# Import the dependencies.
from flask import Flask
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################
# reflect an existing database into a new model
# reflect the tables
# Save references to each table
# Create our session (link) from Python to the DB

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine)
M = Base.classes.measurement
S = Base.classes.station
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route('/')
def home():
    return '''
        <h2>Available routes:</h2>
        <ul>
            <li>/api/v1.0/precipitation</li>
            <li>/api/v1.0/stations</li>
            <li>/api/v1.0/tobs</li>
            <li>/api/v1.0/[start]</li>
            <li>/api/v1.0/[start]/[end]</li>
        </ul>
'''
@app.route('/api/v1.0/precipitation')
def precip():
    results = session.query(M.date,M.prcp).filter(M.date >= '2016-08-23').all()
    return { d:v for d,v in results }

@app.route('/api/v1.0/stations')
def stations():
    results = session.query(S.station, S.name).all()
    return { id:loc for id,loc in results }

@app.route('/api/v1.0/tobs')
def Temperature():
    results = session.query(M.date, M.tobs).all()
    return { date:tobs for date,tobs in results }

@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')
def date_range(start,end='2017-08-23'):

    sel = [ func.min(M.tobs), func.avg(M.tobs), func.max(M.tobs) ]
    [min,avg,max] = session.query(*sel).filter((M.date>=start)&(M.date<=end)).first()

    return { 'Date_range':f'{start} to {end}','Min_Temp':min,'Avg_Temp':round(avg,0),'Max_Temp':max }

if '__main__' == __name__:
    app.run()