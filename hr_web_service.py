from database_webserver_functions import add_heart_rate, create_user, \
        print_user, avg_total_hr, interval_hr
import datetime
from pymodm import connect
from flask import Flask, jsonify, request
connect("mongodb://vcm-3502.vm.duke.edu:27017/heart_rate_app")
app = Flask(__name__)


@app.route("/api/heart_rate", methods=["POST"])
def store_heart_rate():
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
    except:
        create_user(email, age, rate)


@app.route("/api/heart_rate/<user_email>", methods=["GET"])
def all_measurements(user_email):
    try:
        return print_user(user_email)
    except:
        print("Must give a valid user email!")


@app.route("/api/heart_rate/average/<user_email>", methods=["GET"])
# get average over all heart rates
def get_complete_average(user_email):
    average = avg_total_hr(user_email)
    return print(average)


@app.route("/api/heart_rate/interval_average", methods=["POST"])
def interval_avg():
    r = request.get_json()
    try:
        email = r["user_email"]
        inter = r["heart_rate_average_since"]
    except ValueError:
        print("Please provide the correct json format!")
    try:
        isinstance(email, str)
    except TypeError:
        print("Please provide a valid email!")
    try:
        isinstance(inter, type(datetime.datetime.now()))
    except TypeError:
        print("Please provide proper format for time!")
    return print(interval_hr(email, inter))
