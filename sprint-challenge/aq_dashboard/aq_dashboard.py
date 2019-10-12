"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from decouple import config
from os import getenv
import openaq
import requests
#import DB

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
APP.config['ENV'] = getenv('FLASK_ENV')
DB = SQLAlchemy(APP)
DB.init_app(APP)

@APP.route('/', methods=['GET'])
def root():
    """Base view."""
    records = Record.query.filter(Record.value >= 10).all()
    return str(records)

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return "date: {}, value: {}".format(self.datetime, self.value)

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    add_data()
    DB.session.commit()
    return 'Data refreshed!'
def get_data(val_list):
    mmnt = API.measurements(city='Los Angeles', parameter='pm25')
    body = mmnt[1]
    results = body['results'][:100]
    for i in results:
        val_list.append((i['date']['utc'], i['value']))
    return val_list
def add_data():
    utc_val = []
    get_data(utc_val)
    n = 0
    for i in utc_val:
        utc = i[0]
        val = i[1]
        val_utc = Record(id=n, datetime=str(utc), value=val)
        n += 1
        DB.session.add(val_utc)
    DB.session.commit()
