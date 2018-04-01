from database_webserver_functions import add_heart_rate, create_user, \
        print_user, avg_total_hr, interval_hr
import datetime
from pymodm import connect
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
connect("mongodb://vcm-3502.vm.duke.edu:27017/heart_rate_app")


@app.route("/", methods=["GET"])
def hello():
    """ Function that greets the user on the main page!
    """
    return "Hello, there!"


@app.route("/api/heart_rate", methods=["POST"])
def store_heart_rate():
    """Function that takes in a json and creates or adds data to a user.

    :raises ValueError: Error raised for incorrect json format
    :raises TypeError: Error raised if values provided are incorrect type
    """
    user = request.get_json()
    try:
        email = user["user_email"]
        age = user["user_age"]
        rate = user["heart_rate"]
    except ValueError:
        print("Please provide the correct json format!")
    try:
        isinstance(email, str)
    except TypeError:
        print("Please provide a valid email!")
    try:
        isinstance(age, float)
        isinstance(rate, float)
    except TypeError:
        print("Please provide valid age and heart rate!")

    try:
        # attempt to add info. If user does not exist, except will create user
        add_heart_rate(email, rate, datetime.datetime.now())
        return "Added heart rate to existing user!"
    except:
        create_user(email, age, rate)
        return "Created new user!"


@app.route("/api/heart_rate/<user_email>", methods=["GET"])
def all_measurements(user_email):
    """Function that prints the entire record of a user, given email.
    """
    try:
        info = print_user(user_email)
        return jsonify(info)
    except:
        return "Must give a valid user email!"


@app.route("/api/heart_rate/average/<user_email>", methods=["GET"])
# get average over all heart rates
def get_complete_average(user_email):
    """Function that calculates the average of all heart rates
    """
    average = avg_total_hr(user_email)
    text = "The average is {}.".format(average)
    return text


@app.route("/api/heart_rate/interval_average", methods=["POST"])
def interval_avg():
    """Function that calculates the average heart rate from an interval.

    :raises ValueError: Error raised if incorrect json format
    :raises TypeError: Error raised if inputs are of incorrect type
    """
    r = request.get_json()
    try:
        email = r["user_email"]
        inter = r["heart_rate_average_since"]
    except ValueError:
        print("Please provide the correct json format!")
    try:
        isinstance(email, str)
        isinstance(inter, str)
    except TypeError:
        print("Please provide a valid email or proper time string!")
    return interval_hr(email, inter)
