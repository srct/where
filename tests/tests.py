import requests
import json
import os

from colorama import init, Fore, Style
from termcolor import colored

from codes import *

# initialize terminal colors
init()

def get_status(expected, actual):
    '''
    Returns whether or not the test passed
    :param expected (tuple) : tuple containing expected value(s)
    :param actual (tuple)   : tuple containing actual value(s) returned by the test

    :returns: success of the test
    '''
    success = True
    msg = ""

    for e, a in zip(expected, actual):
        if e != a:
            success = False
            msg += colored(f"Expected: {e}\nActual: {a}\n", "red")

    status = colored("failed", "red") if not success else \
        colored("success", "green")

    print(f"Status: {status}")
    if not success:
        # expected = [str(e) for e in expected]
        # actual = [str(a) for a in actual]
        # print(colored(f"Test: {expected}\nActual: {actual}\n", "red")) 
        print(msg)

    print("\n")
    return success

def print_test(test_num, endpoint):
    '''
    Prints the test number and endpoint
    :param: test_num (int): test number
    :param: endpoint (string): endpoint that is being tested
    '''

    print(f"----- Test {test_num} -----")
    print(f"Endpoint: " + colored(endpoint, "yellow"))

def setup(test_num):
    '''
    Tests the endpoint /test_data with valid input
    '''
    endpoint = "test_data"
    print_test(test_num, f"/{endpoint}")
    print("Method: " + colored("GET", "yellow"))

    data = requests.get(f"http://localhost:5000/{endpoint}")
    expected = [SUCCESS, REDIRECT]
    print(data.history[0].status_code)
    actual = [ codes[data.status_code], codes[data.history[0].status_code] ]

    return get_status(expected, actual)

def setup2(test_num):
    '''
    Tests the endpoint /test_data with an invalid method
    '''
    endpoint = "test_data"
    print_test(test_num, f"/{endpoint}")
    print("Method: " + colored("POST", "yellow"))

    data = requests.post(f"http://localhost:5000/{endpoint}")
    expected = [INVALID_METHOD]
    actual = [codes[data.status_code]]

    return get_status(expected, actual)

def valid_point(test_num):
    '''
    Test that getting the data for point 1 is proper
    '''

    endpoint = "point/1"
    print_test(test_num, f"/{endpoint}")
    print("Method: " + colored("GET", "yellow"))

    data = requests.get(f"http://localhost:5000/{endpoint}")
    try:
        js_path = os.path.join(os.path.dirname(__file__), "data", "point_1.json")

        actual = [codes[data.status_code], 
            list(data.json().keys())]
        expected = [SUCCESS, 
            list(json.loads(open(js_path).read()).keys())]

        return get_status(expected, actual)

    except Exception as e:
        print(e)
    
    return False

def invalid_point(test_num):
    '''
    Test that sending a string to the "point" endpoint returns a 404
    '''

    endpoint = "point/adba"
    print_test(test_num, f"/{endpoint}")
    print("Method: " + colored("GET", "yellow"))

    data = requests.get(f"http://localhost:5000/{endpoint}")
    try:
        actual = [codes[data.status_code]]
        expected = [NOT_FOUND]

        return get_status(expected, actual)

    except Exception as e:
        print(e)
    
    return False


num_errors = 0    
num_errors += 0 if setup(1) else 1
num_errors += 0 if setup2(2) else 1
num_errors += 0 if valid_point(2) else 1
num_errors += 0 if invalid_point(3) else 1

print(f"Errors: {num_errors}")