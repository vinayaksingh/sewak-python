import requests

from api.json.json_request import Request
from models.db_model import User, Complain


def requestForUser(timestamp):
    #
    user_obj = User(auth_code = None,
                   phone_number = 9780044093,
                   handset_serial_number = 'JLIU897978K',
                   name = None,
                   email = None)
    RequestObj = Request(timestamp=timestamp, user=user_obj)
    requestJson = Request.get_request_json(RequestObj)
    print(requestJson)
    response = requests.get('http://localhost:8080/api/user', json=requestJson)
    return response

def get_otp(timestamp):

    # get an opt. This shall be called after the checking if user exists on the server side.
    user_obj = User(auth_code = None,
                   phone_number = 9780044017,
                   handset_serial_number = 'JLIU897978K',
                   name = None,
                   email = None)
    RequestObj = Request(timestamp=timestamp, user=user_obj)
    requestJson = Request.get_request_json(RequestObj)
    print(requestJson)
    response = requests.get('http://localhost:8080/api/getotp', json=requestJson)
    return response


def verifyUser(timestamp, otp):
    # the client sends the OTP for verification.
    user_obj = User(auth_code = None,
                   phone_number = 9780044017,
                   handset_serial_number = 'JLIU897978K',
                   name = None,
                   email = None)
    RequestObj = Request(timestamp=timestamp, user=user_obj)
    requestJson = Request.get_request_json(RequestObj)
    print(requestJson)
    return requests.put('http://localhost:8080/api/otp/'+otp, json=requestJson)

def add_service(timestamp):
    # add service
    # TODO This will be sent from Owner's Mobile App or WebPortal.
    user_obj = User(auth_code = None,
                   phone_number = 9780044091,
                   handset_serial_number = 'JLIU897978F',
                   name = None,
                   email = None)

    RequestObj = Request(timestamp=timestamp, user=user_obj, category=None, service=None, complain=None)
    requestJson = Request.get_request_json(RequestObj)
    print(requestJson)
    return requests.post('http://localhost:8080/api/services/new_service_3', json=requestJson)


def add_category(timestamp):
    # add category
    # TODO This will be sent from Owner's Mobile App or WebPortal.
    user_obj = User(auth_code = None,
                   phone_number = 9780044091,
                   handset_serial_number = 'JLIU897978F',
                   name = None,
                   email = None)

    RequestObj = Request(timestamp=timestamp, user=user_obj, category=None, service=None, complain=None)
    requestJson = Request.get_request_json(RequestObj)
    print(requestJson)
    return requests.post('http://localhost:8080/api/categories/new_category_2', json=requestJson)


def get_all_categories(timestamp):
    user_obj = User(auth_code = 'dc0100845c1e8d389ecfb82946c40ccbb7982462',
                   phone_number = 9780044091,
                   handset_serial_number = 'JLIU897978F',
                   name = None,
                   email = None)

    RequestObj = Request(timestamp=timestamp, user=user_obj, category=None, service=None, complain=None)
    requestJson = Request.get_request_json(RequestObj)
    print(requestJson)
    return requests.get('http://localhost:8080/api/categories', json=requestJson)


def get_all_services(timestamp):
    user_obj = User(auth_code = 'dc0100845c1e8d389ecfb82946c40ccbb7982462',
                   phone_number = 9780044091,
                   handset_serial_number = 'JLIU897978F',
                   name = None,
                   email = None)

    RequestObj = Request(timestamp=timestamp, user=user_obj, category=None, service=None, complain=None)
    requestJson = Request.get_request_json(RequestObj)
    print(requestJson)
    return requests.get('http://localhost:8080/api/services', json=requestJson)


def add_complain(timestamp):
    # add complain.
    user_obj = User(auth_code = 'dc0100845c1e8d389ecfb82946c40ccbb7982462',
                   phone_number = 9780044091,
                   handset_serial_number = 'JLIU897978F',
                   name = None,
                   email = None)

    complain_obj = Complain(user_id=1, category_id=1, service_id=4, address='Panchkula', message='FixShit',
                 service_status=0, complain_phone_number=9415549481)

    RequestObj = Request(timestamp=timestamp, user=user_obj, category=None, service=None, complain=complain_obj)
    requestJson = Request.get_request_json(RequestObj)
    print(requestJson)
    return requests.post('http://localhost:8080/api/complains', json=requestJson)

def update_complain(timestamp):
    # add complain.
    user_obj = User(auth_code = 'dc0100845c1e8d389ecfb82946c40ccbb7982462',
                   phone_number = 9780044091,
                   handset_serial_number = 'JLIU897978F',
                   name = None,
                   email = None)

    complain_obj = Complain(user_id=1, category_id=1, service_id=4, address='Panchkule', message='changeShit',
                 service_status=0, complain_phone_number=9415549481)

    RequestObj = Request(timestamp=timestamp, user=user_obj, category=None, service=None, complain=complain_obj)
    requestJson = Request.get_request_json(RequestObj)
    print(requestJson)
    return requests.put('http://localhost:8080/api/complain/3', json=requestJson)

if __name__ == '__main__':
    import datetime
    timestamp = datetime.datetime.now().strftime("%d-%m-%Y_%H_%M_%S_%f")
    resp = requestForUser(timestamp)

    # resp = get_otp(timestamp)
    # resp = verifyUser(timestamp, '5153')
    # resp = add_category(timestamp)
    # resp = add_service(timestamp)
    # resp = get_all_categories(timestamp)
    # resp = get_all_services(timestamp)
    # resp = add_complain(timestamp)
    # resp = update_complain(timestamp)
    print(resp.json())
    pass


