from pymodm import connect
import models
import time
import datetime
from database_webserver_functions import add_heart_rate, create_user, \
        print_user, avg_total_hr, interval_hr, check_valid_user


def test_exceptions():
    import pytest
    import math
    with pytest.raises(ImportError, message="Expecting ImportError"):
        import blah
    with pytest.raises(TypeError, message="Expecting TypeError"):
        test = 5 + 'h'
    with pytest.raises(ValueError, message="Expecting ValueError"):
        test = math.sqrt(-1)


def test_add_heart_rate():
    connect("mongodb://vcm-3502.vm.duke.edu:27017/heart_rate_app")
    email = "ml273@duke.edu"
    test_user = models.User(email, 22, [], [])
    test_user.heart_rate.append(66)
    test_user.heart_rate_times.append(datetime.datetime.now())
    test_user.save()
    add_heart_rate(email, 56, datetime.datetime.now())
    updated_test = models.User.objects.raw({"_id": email}).first()
    assert updated_test.heart_rate[1] == 56 and updated_test.age == 22


def test_create_user():
    connect("mongodb://vcm-3502.vm.duke.edu:27017/heart_rate_app")
    email = "ml@duke.edu"
    create_user(email, 22, 66)
    test_user = models.User.objects.raw({"_id": email}).first()
    assert test_user.heart_rate[0] == 66 and test_user.age == 22


def test_avg_total_hr():
    connect("mongodb://vcm-3502.vm.duke.edu:27017/heart_rate_app")
    email = "ml273@duke.edu"
    rates = [45, 65, 34, 68]
    for rate in rates:
        add_heart_rate(email, rate, datetime.datetime.now())
    # Should be [66, 56, 45, 65, 34, 68] now if including previous test
    assert abs(avg_total_hr(email) - 55.67) < 0.1


def test_interval_hr():
    connect("mongodb://vcm-3502.vm.duke.edu:27017/heart_rate_app")
    email = "example@duke.edu"
    now = datetime.datetime.now()
    test_user = models.User(email, 22, [], [])
    test_user.heart_rate.append(66)
    test_user.heart_rate_times.append(now)
    test_user.save()
    time.sleep(0.500)
    then = datetime.datetime.now()
    add_heart_rate(email, 78, then)
    ###EDIT
    assert interval_hr(email, str(now)) == 72


def test_interval_hr_invalid():
    connect("mongodb://vcm-3502.vm.duke.edu:27017/heart_rate_app")
    email = "example2@duke.edu"
    now = datetime.datetime.now()
    test_user = models.User(email, 22, [], [])
    test_user.heart_rate.append(66)
    test_user.heart_rate_times.append(now)
    test_user.save()
    time.sleep(0.500)
    then = datetime.datetime.now()
    time.sleep(0.500)
    ###EDIT
    future = str(datetime.datetime.now())
    #future = datetime.datetime.now()
    add_heart_rate(email, 78, then)
    message = "Given date is in the future. Please give a reasonable input."
    assert interval_hr(email, future) == message
