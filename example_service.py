from flask import Flask, jsonify, request
app = Flask(__name__)
from main import add_heart_rate, create_user, print_user
import datetime

#edit
@app.route("/api/heart_rate", methods=["POST"])
def store_heart_rate():
    user = request.get_json()
    # maybe add line that checks if user is created already, and if so, just add heart rate instead
    # of create
    # if user is new:
        create_user(user["user_email"], user["user_age"], user["heart_rate"])
    #else:
        add_heart_rate(user["user_email"], user["heart_rate"], datetime.datetime.now())

@app.route("/api/heart_rate/<user_email>", methods=["GET"])
#def all_measurements(user_email):
print_user(user_email)

@app.route("/api/heart_rate/average/<user_email>", methods=["GET"])
# get average over all heart rates
def get_complete_average(user_email):
    #left off here. need to figure out how to get every number after searching for the user

@app.route("/api/heart_rate/interval_average", methods=["POST"])
r = request.get_json()
#get data for all times specified
#get the interval specified. maybe if case to make sure everything stays within



#end edit


@app.route("/", methods=["GET"])
def hi():
    return "Hello, world"

@app.route("/name", methods=["GET"])
def getname():
    name = {
        "name": "Marianne Lee"
    }
    return jsonify(name)

@app.route("/hello/<name>", methods=["GET"])
def hello(name):
    data = {
        "message": "Hello there, {}".format(name)
    }
    return jsonify(data)

@app.route("/distance", methods=["POST"])
def distance():
    points = request.get_json()
    dx = points["a"][0]-points["b"][0]
    dy = points["a"][1]-points["b"][1]
    dist = (dx**2 + dy**2)**0.5
    res = {
        "distance": "{}".format(dist),
        "a": "{}".format(points["a"]),
        "b": "{}".format(points["b"]),
    }
    return jsonify(res)
