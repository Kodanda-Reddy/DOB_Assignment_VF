import requests
from datetime import datetime


def is_leap_day(year, month, day):
    # To check if a day is a leap day
    if year % 4 == 0 and month == 2 and day == 29:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            else:
                return False
        else:
            return True
    return False


def get_response_dob(url, params={}):
    # Fetch the response after sending the request to given endpoint
    response = requests.get(url=url, params=params)
    response_json = response.json()
    return response_json['message'],response.status_code


def get_expected_response_dob(dob, unit):
    today = datetime.now()  # gives current datetime
    dob_datetime = datetime(*[int(x) for x in dob.split('-')])

    # check if dob is leap day
    is_dob_leap_day = is_leap_day(dob_datetime.year, dob_datetime.month, dob_datetime.day)

    if (today.month == dob_datetime.month and today.day >= dob_datetime.day) \
            or (today.month > dob_datetime.month):
        if is_dob_leap_day:
            if is_leap_day(today.year + 1, dob_datetime.month, dob_datetime.day):
                dob_next = datetime(today.year + 1, dob_datetime.month, dob_datetime.day)
            else:
                dob_next = datetime(today.year + 1, dob_datetime.month, dob_datetime.day - 1)
        else:
            dob_next = datetime(today.year + 1, dob_datetime.month, dob_datetime.day)
    else:
        if is_dob_leap_day:
            if is_leap_day(today.year, dob_datetime.month, dob_datetime.day):
                dob_next = datetime(today.year, dob_datetime.month, dob_datetime.day)
            else:
                dob_next = datetime(today.year, dob_datetime.month, dob_datetime.day - 1)
        else:
            dob_next = datetime(today.year, dob_datetime.month, dob_datetime.day)

    # Getting time delta between next dob and today
    delta = dob_next - today

    # Returning expected output message
    out_message = ' ' + unit + 's left'
    if unit == 'hour':
        out_message = str(delta.days * 24 + int(delta.seconds / 60 / 60)) + out_message
    elif unit == 'day':
        out_message = str(delta.days + 1) + out_message
    elif unit == 'week':
        out_message = str((delta.days+1) // 7) + out_message
    elif unit == 'month':
        out_message = str((delta.days+1) // 30) + out_message
    return out_message
