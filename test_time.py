import datetime
from time_convert import str2time, time2str


def test_conversion():
    dt = datetime.datetime.now()
    string = time2str(dt)
    assert dt == str2time(string)
