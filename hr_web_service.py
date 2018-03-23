from pymodm import connect
connect("mongodb://vcm-3502.vm.duke.edu:27017/heart_rate_app")

from flask import Flask, jsonify, request
app = Flask(__name__)
from database_webserver_interface import add_heart_rate, create_user, print_user, avg_total_hr
import datetime

@app.route("/api/heart_rate", methods=["POST"])
def store_heart_rate():
    user = request.get_json()
    ########EDIT######## check json format is okay
    try:  # attempt to add info. If user does not exist, except will create user
        add_heart_rate(user["user_email"], user["heart_rate"], datetime.datetime.now())
    except:
        create_user(user["user_email"], user["user_age"], user["heart_rate"])

@app.route("/api/heart_rate/<user_email>", methods=["GET"])
def all_measurements(user_email):
    #can check user_email input type (string?)
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
    #####EDIT###### check this json format is okay (appropriate fields)
    return print(interval_hr(r["user_email"], r["heart_rate_average_since"]))
