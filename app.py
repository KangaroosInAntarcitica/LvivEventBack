from flask import Flask, render_template, request, url_for, redirect, \
    json, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, \
    check_password_hash
import os
from string import ascii_letters, digits
import re
from models import Users, Events, parse_event


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


@app.route('/', methods=['GET'])
def default():
    return 'This is the default webpage. Here is your request: ' + str(request)


@app.route("/register", methods=["POST"])
def register():
    print("A post request to register was made")
    print("The details are: ", request.json)

    username = request.json["username"]
    # validate username
    if (not 0 < len(username) < 11) or \
            (not set(ascii_letters + digits + '_').issuperset(set(username.lower()))):
        return jsonify(status="wrong username format")
    if Users.query.filter_by(username=username).first():
        return jsonify(status="username unavailable")

    email = request.json["email"]
    # validate email
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify(status="wrong e-mail format")
    if Users.query.filter_by(email=email).first():
        return jsonify(status="e-mail unavailable")

    password = request.json["password"]
    # validate password
    if (not 8 <= len(password)):
        return jsonify(status="too short password")
    pw_hash = generate_password_hash(password)

    new_user = Users(username, email, pw_hash)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(status="success")


@app.route("/login", methods=["POST"])
def login():
    print("A post request to login was made")
    print("The details are: ", request.json)

    username = request.json["username"]
    password = request.json["password"]

    user = Users.query.filter_by(username=username).first()
    if (user and check_password_hash(user.pw_hash, password)):
        return jsonify(status="success")
    else:
        return jsonify(status="wrong e-mail or password")

# EVENTS PART
# TODO make a separate file for different functions


@app.route("/events", methods=["GET"])
def get_events():
    print("A get request to events was made")

    events = list(map(parse_event, Events.query.all()))
    return jsonify(events)


@app.route("/newEvent", methods=["POST"])
def post_event():
    print("A post request to newEvent was made")

    data = request.json
    new_event = Events(data)
    db.session.add(new_event)
    db.session.commit()
    return jsonify(status="success")


@app.route("/getEvent/<event_name>")
def get_event(event_name):
    event = Events.query.filter_by(name=event_name).first()
    if event:
        return jsonify(parse_event(event))
    else:
        return jsonify(status="wrong event name")


if __name__ == '__main__':
    app.run(debug=True)
