import pytest
from pytest_check import check
from Utils import get_testdata
from src import get_response
from datetime import datetime
from configparser import ConfigParser
import logging

config = ConfigParser()
config.read('config.ini')
logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def is_not_valid_date(date_str):
    try:
        date_format = config.get('configDOB', 'date_format')
        # formatting the date using strptime() function
        date_object = datetime.strptime(date_str, date_format)
        return False

    # If the date validation goes wrong
    except ValueError:
        return True


def is_dob_future_date(date_str):
    # To check if dob is a future date
    today = datetime.now()  # gives current datetime
    dob_datetime = datetime(*[int(x) for x in date_str.split('-')])
    if today >= dob_datetime:
        return False
    return True


def is_unit_invalid(unit):
    # To check if unit is in list of units for the end point
    units = config.get('configDOB', 'unit_list')
    if unit not in units:
        return True
    return False


@pytest.mark.parametrize("testcase_name,dob,unit, status, url", get_testdata.get_testdata_dob())
def test_dob_validation(testcase_name, dob, unit, status, url):
    # To validate the endpoint against all the test data
    logger.info('Running testcase : ' + testcase_name)
    logger.info('URL : ' + url)
    logger.info('Date Of Birth : ' + dob)
    logger.info('Unit : ' + unit)
    params = {'dateofbirth': dob, 'unit': unit.strip()}
    actual_response, actual_status_code = get_response.get_response_dob(url, params)

    if dob == '' or unit == '':
        expected_response = 'Please specify both query parameter dateofbirth and unit'
    elif is_unit_invalid(unit):
        expected_response = 'Please specify valid unit'
    elif is_not_valid_date(dob):
        expected_response = 'Please specify dateofbirth in ISO format YYYY-MM-DD'
    elif is_dob_future_date(dob):
        expected_response = 'Please specify dateofbirth in past or current day'
    else:
        expected_response = get_response.get_expected_response_dob(dob, unit)

    with check:
        assert actual_response == expected_response
    with check:
        assert actual_status_code == int(status)
    logger.info('endpoint response status code : ' + str(actual_status_code))
    logger.info('expected response status code : ' + status)
    logger.info('endpoint response message : ' + str(actual_response))
    logger.info('expected response message : ' + expected_response)


def test_dob_no_param_validation():
    # To validate if no params are sent in the URL i.e., in the GET request
    url = config.get('configDOB', 'ENDPOINT_URL')
    logger.info('Running testcase : Invalid_URL_with_no_parameters')
    logger.info('URL : ' + url)
    actual_response, actual_status_code = get_response.get_response_dob(url=url)
    expected_response = 'Please specify both query parameter dateofbirth and unit'
    assert actual_response == expected_response
    assert actual_status_code == 400
    logger.info('endpoint response status code : ' + str(actual_status_code))
    logger.info('expected response status code : 400')
    logger.info('endpoint response message : ' + str(actual_response))
    logger.info('expected response message : ' + expected_response)


