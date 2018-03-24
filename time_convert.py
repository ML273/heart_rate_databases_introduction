import datetime


def time2str(dt):
    """Function that converts datetime object to string

    :param dt: datetime object
    """
    return dt.isoformat()


def str2time(strtime):
    """Function that converts string to datetime object

    :param strtime: string
    """
    return datetime.datetime.strptime(strtime, "%Y-%m-%dT%H:%M:%S.%f")
