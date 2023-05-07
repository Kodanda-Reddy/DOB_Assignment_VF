import csv
from configparser import ConfigParser


def get_testdata_dob():
    # To get the testdata in a list of tuples
    config = ConfigParser()
    config.read('config.ini')
    testdata_location = config.get('configDOB','DOB_TEST_DATA_FILE')
    endpoint_url = config.get('configDOB', 'ENDPOINT_URL')
    with open(testdata_location, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        data = [tuple(row+[endpoint_url]) for row in reader]
    return data
