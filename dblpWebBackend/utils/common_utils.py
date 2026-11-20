import datetime


def check_category(category):
    return bool(category)


def check_year(yf, yt):
    return 0 < yf <= datetime.datetime.now().year and 0 < yt <= datetime.datetime.now().year


def check_key(keys):
    return keys is not None and len(keys) != 0
