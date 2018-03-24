from pymodm import connect
import models
import datetime
connect("mongodb://vcm-3502.vm.duke.edu:27017/heart_rate_app")


def add_heart_rate(email, heart_rate, time):
    check_valid_user(email)
    user = models.User.objects.raw({"_id": email}).first()
    # Get the first user where _id=email
    user.heart_rate.append(heart_rate)
    # Append the heart_rate to the user's list of heart rates
    user.heart_rate_times.append(time)
    # append the current time to the user's list of heart rate times
    user.save()  # save the user to the database


def create_user(email, age, heart_rate):
    u = models.User(email, age, [], [])  # create a new User instance
    u.heart_rate.append(heart_rate)  # add initial heart rate
    u.heart_rate_times.append(datetime.datetime.now())
    # add initial heart rate time
    u.save()  # save the user to the database


def print_user(email):
    user = models.User.objects.raw({"_id": email}).first()
    # Get the first user where _id=email
    res = {"email": user.email, "heart_rate": user.heart_rate, "heart_rate_times":
           user.heart_rate_times}
    return res


def avg_total_hr(email):
    check_valid_user(email)
    user = models.User.objects.raw({"_id": email}).first()
    n = len(user.heart_rate)
    average = sum(user.heart_rate)/n
    return average


def interval_hr(email, date):
    check_valid_user(email)
    user = models.User.objects.raw({"_id": email}).first()
    dates = user.heart_rate_times
    rates = user.heart_rate
    n = len(dates)
    ind = dates.index(min(dates, key=lambda d: abs(d - date)))
    found_date = dates[ind]
    if ind == n - 1 and (date - found_date).total_seconds() > 0:
        return "Given date is in the future. Please give a reasonable input."
    elif ind == 0 and (date - found_date).total_seconds() < 0:
        return avg_total_hr(email)
    elif (date - found_date).total_seconds() > 0.01:
        ind += 1
        m = n - ind
        result = sum(rates[ind:])/m
        print((date-found_date).total_seconds())
        return result
    else:
        m = n - ind
        result = sum(rates[ind:])/m
        return result


def check_valid_user(email):
    try:
        user = models.User.objects.raw({"_id": email}).first()
    except:
        print("User email is not in database! \
              Check for typos or create new user!")
