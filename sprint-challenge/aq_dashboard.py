"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from decouple import config
from os import getenv
from openaq import *
import requests

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)


API = openaq.OpenAQ()
status, body = API.measurements(city='Los Angeles', parameter='pm25')
def LAquery(k):
    LAresults = k['results']
    values = []
    for k in LAresults:
        kvalue = k.get('value')
        kdate = k.get('date')
        kutc = kdate.get('utc')
        values.append((kvalue, kutc))
    return values

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return "<id={self.id}, datetime={self.datetime}, value={self.value}>"

@APP.route('/')
def root():
    """Base view."""
    records = Record.query.filter(Record.value>=10).all()
    res=''
    for rec in records:
        res += 'datetime = '+ rec.datetime
        res += ", "
        res += 'value = '+ str(rec.value)
        res += '</br>'
    return res


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    API_items = body['results']
    for i in API_items:
        ivalue = i.get('value')
        idate = i.get('date')
        iutc = idate.get('utc')
        db_item = (Record(datetime=iutc, value=ivalue))
        DB.session.add(db_item)
    DB.session.commit()
    return 'Data refreshed!'

if __name__ == "__main__":
    APP.run()
