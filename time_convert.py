import datetime


def time2str(dt):
    return dt.isoformat()


def str2time(strtime):
    return datetime.datetime.strptime(strtime, "%Y-%m-%dT%H:%M:%S.%f")
