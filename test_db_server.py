from pymodm import connect
import models
import datetime
from database_webserver_function import add_heart_rate, create_user, print_user, avg_total_hr, interval_hr, check_valid_user

def test_exceptions():
    pass

def test_add_heart_rate():
    connect("mongodb://vcm-3502.vm.duke.edu:27017/heart_rate_app")
    email = "ml273@duke.edu"
    test_user = models.User(email, 22, 66, datetime.datetime.now())
    test_user.save()
    add_heart_rate(email, 56, datetime.datetime.now())
    updated_test = models.User.objects.raw({"_id": email}).first()
    assert updated_test.heart_rate == [66, 56] and updated_test.age == 22

def test_create_user():
    pass

def test_print_user():
    pass

def test_avg_total_hr():
    pass

def test_interval_hr():
    pass

def check_valid_user():
    pass
