from app import db
from datetime import date
from uuid import uuid4
from flask_login import UserMixin


def parse_event(event):
    return {
        'name': event.name,
        'enddate': str(event.enddate),
        'startdate': str(event.startdate),
        'image': event.image,
        'address': event.address,
        'description': event.description,
        'transfer': event.transfer,
        'timetable': event.timetable
    }


class Users(UserMixin, db.Model):
    """Class representing user in database"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    email = db.Column(db.Text, unique=True)
    pw_hash = db.Column(db.Text)
    uuid = db.Column(db.Text, unique=True)

    def __init__(self, username, email, pw_hash):
        self.username = username
        self.email = email
        self.pw_hash = pw_hash
        self.uuid = str(uuid4())


class Events(db.Model):
    """Class representing events"""
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    startdate = db.Column(db.Date)
    enddate = db.Column(db.Date)
    image = db.Column(db.Text)
    description = db.Column(db.Text)
    address = db.Column(db.Text)
    transfer = db.Column(db.Text)
    timetable = db.Column(db.Text)

    def __init__(self, data):
        self.name = data['name']

        self.startdate = date(*map(int, data['startdate'].split('-')))
        self.enddate = date(*map(int, data['enddate'].split('-'))) \
            if 'enddate' in data else self.startdate

        self.image = data['image'] if 'image' in data else None
        self.description = data['description'] if 'description' in data else None
        self.address = data['address'] if 'address' in data else None
        self.transfer = data['transfer'] if 'transfer' in data else None
        self.timetable = data['timetable'] if 'timetable' in data else None