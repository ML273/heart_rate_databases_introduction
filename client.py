import requests
import datetime

r = requests.get("http://vcm-3502.vm.duke.edu:5000/")
print(r.text)

create_user = requests.post("http://vcm-3502.vm.duke.edu:5000/api/heart_rate",\
                            json={"user_email": "ml273@duke.edu",
                                  "user_age": 22,
                                  "heart_rate": 66})
print(create_user.text)

info = requests.get("http://vcm-3502.vm.duke.edu:5000/api/heart_rate/ml273@duke.edu")
print(info.text)
avg = requests.get("http://vcm-3502.vm.duke.edu:5000/api/heart_rate/average/ml273@duke.edu")
print(avg.text)
now = datetime.datetime.now()
interval = requests.post("http://vcm-3502.vm.duke.edu:5000/api/heart_rate/interval_average",
                         json={"user_email": "ml273@duke.edu", "heart_rate_average_since": now})
print(interval.text)
