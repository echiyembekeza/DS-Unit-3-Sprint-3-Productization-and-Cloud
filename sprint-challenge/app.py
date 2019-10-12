"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import getenv
import openaq

APP = Flask(__name__)

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
APP.config['ENV'] = getenv('FLASK_ENV')
DB = SQLAlchemy(APP)
DB.init_app(APP)

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return "date: {}, value: {}".format(self.datetime, self.value)


@APP.route('/')
def root():
    """Base view."""
