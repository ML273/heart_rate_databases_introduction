from pymodm import connect
import models
import datetime

def add_heart_rate(email, heart_rate, time):
    connect("mongodb://vcm-3502.vm.duke.edu:27017/heart_rate_app")
    check_valid_user(email)
    user = models.User.objects.raw({"_id": email}).first() # Get the first user where _id=email
    user.heart_rate.append(heart_rate) # Append the heart_rate to the user's list of heart rates
    user.heart_rate_times.append(time) # append the current time to the user's list of heart rate times
    user.save() # save the user to the database

def create_user(email, age, heart_rate):
    connect("mongodb://vcm-3502.vm.duke.edu:27017/heart_rate_app")
    u = models.User(email, age, [], []) # create a new User instance
    u.heart_rate.append(heart_rate) # add initial heart rate
    u.heart_rate_times.append(datetime.datetime.now()) # add initial heart rate time
    u.save() # save the user to the database

def print_user(email):
    connect("mongodb://vcm-3502.vm.duke.edu:27017/heart_rate_app")
    user = models.User.objects.raw({"_id": email}).first() # Get the first user where _id=email
    print(user.email)
    print(user.heart_rate)
    print(user.heart_rate_times)

def avg_total_hr(email):
    connect("mongodb://vcm-3502.vm.duke.edu:27017/heart_rate_app")
    check_valid_user(email)
    user = models.User.objects.raw({"_id": email}).first()
    n = len(user.heart_rate)
    average = sum(user.heart_rate)/n
    return average

def interval_hr(email, date):
    connect("mongodb://vcm-3502.vm.duke.edu:27017/heart_rate_app")
    check_valid_user(email)
    user = models.User.objects.raw({"_id": email}).first()
    dates = user.heart_rate_times
    rates = user.heart_rate
    n = len(dates)
    ind = dates.index(min(dates, key=lambda d: abs(d - date)))
    found_date = dates[ind]
    if ind == n-1 and (date - found_date).total_seconds() > 0:
        return "Given date is in the future. Please give a reasonable input."
    elif ind == 0 and (date - found_date).total_seconds() < 0:
        return avg_total_hr(email)
    elif (date - found_date).total_seconds() > 0:
        ind += 1
        result = sum(rates[ind:])/n
        return result
    else:
        result = sum(rates[ind:])/n
        return result

def check_valid_user(email):
    try:
        user = models.User.objects.raw({"_id": email}).first()
    except:
        print("User email is not in database! Check for typos or create new user!")

#if __name__ == "__main__":
#    connect("mongodb://vcm-3502.vm.duke.edu:27017/heart_rate_app") # open up connection to db
#    create_user(email="suyash@suyashkumar.com", age=24, heart_rate=60) # we should only do this once, otherwise will overwrite existing user
#    add_heart_rate("suyash@suyashkumar.com", 60, datetime.datetime.now())
#    print_user("suyash@suyashkumar.com")
#    print_user("someone@something.com")
