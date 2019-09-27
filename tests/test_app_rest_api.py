import unittest

import requests
import sqlalchemy
from api.json.json_response import Response, AlchemyEncoder
from sqlalchemy.orm import sessionmaker

from api.json.json_request import Request
from api.utils import create_sqlalchemy_engine, get_server_config
from models import db_model
from tests import _test_util


class ApiTest(unittest.TestCase):
    USER_1_PHONE_NUMBER = 9877452151
    USER_1_HANDSET_SERIAL_NUMBER = 'JLIU897978K'
    USER_1_AUTH_CODE = "KHJKH87856HJJHJB"
    USER_1_TIMESTAMP = _test_util.get_current_time()
    USER_1_NAME = "FirstUser"
    USER_1_EMAIL = "vin@vin.com"

    USER_2_PHONE_NUMBER = 9780044034
    USER_2_HANDSET_SERIAL_NUMBER = 'asdfgr43fffg45'
    USER_2_AUTH_CODE = "IUJNFGVTYEKNLMJD"
    USER_2_TIMESTAMP = _test_util.get_current_time()
    USER_2_NAME = "SecondUser"
    USER_2_EMAIL = "Jim@gmail.com"

    CATEGORY_1 = 'category_1'
    CATEGORY_2 = 'category_2'

    SERVICE_1 = 'service_1'
    SERVICE_2 = 'service_2'

    ADDRESS_1 = 'address_1'
    ADDRESS_2 = 'address_2'

    MESSAGE_1 = 'message_1'
    MESSAGE_2 = 'message_2'

    def setUp(self):
        # establish connection with sql server
        self.engine = create_sqlalchemy_engine()
        # create a session
        self.Session = sessionmaker(bind=self.engine)

    def test_get_user(self):
        """
        /api/user
        """
        # when no user is present in database.
        user_obj = db_model.User(auth_code=None,
                                 phone_number=self.USER_1_PHONE_NUMBER,
                                 handset_serial_number=self.USER_1_HANDSET_SERIAL_NUMBER,
                                 name=None,
                                 email=None)
        # print(request_json)
        response = requests.get('http://' + get_server_config()['server_ip'] + ':' + get_server_config()['server_port'] + '/api/user', json=Request.get_request_json(
            Request(timestamp=_test_util.get_current_time(), user=user_obj)))
        response_obj = _test_util.get_response(response)
        self.assertTrue(response_obj.return_code == Response.USER_NOT_EXIST, "The user does not exists")

        # add a user
        user_obj_for_db = db_model.User(
            phone_number=self.USER_1_PHONE_NUMBER,
            handset_serial_number=self.USER_1_HANDSET_SERIAL_NUMBER,
            auth_code=self.USER_1_AUTH_CODE,
            timestamp=self.USER_1_TIMESTAMP,
            name=self.USER_1_NAME,
            email=self.USER_1_EMAIL)

        _test_util.add_row_in_database(user_obj_for_db)
        # test the existing user
        request_json = Request.get_request_json(Request(timestamp=_test_util.get_current_time(), user=user_obj))
        # print(request_json)
        response_obj = _test_util.get_response(requests.get('http://' + get_server_config()['server_ip'] + ':' + get_server_config()['server_port'] + '/api/user', json=request_json))
        self.assertTrue(response_obj.return_code == Response.USER_EXISTS, "User exists.")
        # TODO get all info for this user from server to store on client side.

    def test_get_otp(self):
        """
        /api/getotp
        Note: The scope of this test is restricted to the HTTP response from server and does not validate SMS functionality.
        """
        # get a new otp.
        user_obj = db_model.User(auth_code=None,
                                 phone_number=self.USER_1_PHONE_NUMBER,
                                 handset_serial_number=self.USER_1_HANDSET_SERIAL_NUMBER,
                                 name=None,
                                 email=None)
        request_obj = Request(timestamp=_test_util.get_current_time(), user=user_obj)
        response_obj = _test_util.get_response(
            requests.get('http://' + get_server_config()['server_ip'] + ':' + get_server_config()['server_port'] + '/api/getotp', json=Request.get_request_json(request_obj)))
        self.assertTrue(response_obj.return_code == Response.NEW_USER, "Successful response from server for new user")

        # TODO can we test a fail condition here.

    def test_verify_otp_and_add_user(self):
        """
        /api/otp/<otp>
        """
        # TEST1: Positive #TODO cannot be tested as we do not know OTP generated and sent to client via SMS.
        # get a new otp for testing purpose.
        user_obj = db_model.User(auth_code=None,
                                 phone_number=self.USER_1_PHONE_NUMBER,
                                 handset_serial_number=self.USER_1_HANDSET_SERIAL_NUMBER,
                                 name=None,
                                 email=None)
        # request_obj = Request(timestamp=_test_util.get_current_time(), user=user_obj)
        # response_obj = _test_util.get_response(requests.get('http://' + get_server_config()['server_ip'] + ':' + get_server_config()['server_port'] + '/api/getotp', json=Request.get_request_json(request_obj)))
        # self.assertTrue(response_obj.return_code == Response.NEW_USER, "Successful response from server for new user")
        # # get db helper object. As otp class is singleton we can access the generated otp.
        # otp = DbHelper().otpObj.get_otp_code(self.USER_1_PHONE_NUMBER)
        # print("OTP from server context: " + otp)
        # # trigger /api/otp/<otp> with correct otp and within timeout
        # response_obj = _test_util.get_response(requests.put('http://' + get_server_config()['server_ip'] + ':' + get_server_config()['server_port'] + '/api/otp/' + otp, json=Request.get_request_json(request_obj)))
        # # expected response should convey that a new user is created on server side.
        # self.assertTrue(response_obj.return_code == Response.USER_CREATED, "Successful user created response")
        # #TODO more asserts ?

        # # TEST2: Negative : correct OTP but after timeout. #TODO cannot be tested as we do not know OTP generated and sent to client via SMS.
        # # empty database
        # _test_util.clear_up_db()
        #
        # # sent fresh request for otp
        # request_obj = Request(timestamp=_test_util.get_current_time(), user=user_obj)
        # response_obj = _test_util.get_response(
        #     requests.get('http://' + get_server_config()['server_ip'] + ':' + get_server_config()['server_port'] + '/api/getotp', json=Request.get_request_json(request_obj)))
        # self.assertTrue(response_obj.return_code == Response.NEW_USER, "Successful response from server for new user")
        # # wait for timeout.
        # #TODO wait for timeout
        # # get db helper object. As otp class is singleton we can access the generated otp.
        # otp = DbHelper().otpObj.get_otp_code(self.USER_1_PHONE_NUMBER)
        # print("OTP from server context: " + otp)
        # # trigger /api/otp/<otp> with correct otp and beyond timeout
        # response_obj = _test_util.get_response(
        #     requests.put('http://' + get_server_config()['server_ip'] + ':' + get_server_config()['server_port'] + '/api/otp/' + otp, json=Request.get_request_json(request_obj)))
        # # expected response should convey that a new user is created on server side.
        # self.assertTrue(response_obj.return_code == Response.OTP_ERROR, "Successful response from server for otp "
        #                                                                 "error due to timeout")
        #
        """
             TEST3: Negative : wrong OTP but within timeout.
        """

        # sent fresh request for otp
        request_obj = Request(timestamp=_test_util.get_current_time(), user=user_obj)
        response_obj = _test_util.get_response(
            requests.get('http://' + get_server_config()['server_ip'] + ':' + get_server_config()['server_port'] + '/api/getotp', json=Request.get_request_json(request_obj)))
        self.assertTrue(response_obj.return_code == Response.NEW_USER, "Successful response from server for new user")
        # trigger /api/otp/<otp> with wrong otp and within timeout
        wrong_otp = 12345
        response_obj = _test_util.get_response(
            requests.put('http://' + get_server_config()['server_ip'] + ':' + get_server_config()['server_port'] + '/api/otp/' + str(wrong_otp), json=Request.get_request_json(request_obj)))
        # expected response should convey that a new user is created on server side.
        self.assertTrue(response_obj.return_code == Response.OTP_ERROR, "Successful response form server for otp "
                                                                        "error due to wrong otp")

    def test_add_category(self):
        """
        /api/categories/<category_name>
        """
        """
            TEST1: POSITIVE : add category via api call
        """

        user_obj = db_model.User(auth_code=None,
                                 phone_number=self.USER_1_PHONE_NUMBER,
                                 handset_serial_number=self.USER_1_HANDSET_SERIAL_NUMBER,
                                 name=None,
                                 email=None)
        request_obj = Request(timestamp=_test_util.get_current_time(), user=user_obj)
        response_obj = _test_util.get_response(
            requests.post('http://' + get_server_config()['server_ip'] + ':' + get_server_config()['server_port'] + '/api/categories/' + self.CATEGORY_1,
                          json=Request.get_request_json(request_obj)))
        self.assertTrue(response_obj.return_code == Response.CATEGORY_ADDED, "Category added response")
        # check in db
        session = self.Session()
        try:
            session.query(db_model.Category).filter(db_model.Category.category_name == self.CATEGORY_1).one()
            session.commit()
            self.assertTrue(True, "Category inserted successfully.")
        except sqlalchemy.orm.exc.NoResultFound:
            session.rollback()
            self.fail("No Category row found")

        """
            TEST2: Negative : try to add same category again.
        """
        request_obj = Request(timestamp=_test_util.get_current_time(), user=user_obj)
        response_obj = _test_util.get_response(
            requests.post('http://' + get_server_config()['server_ip'] + ':' + get_server_config()['server_port'] + '/api/categories/' + self.CATEGORY_1,
                          json=Request.get_request_json(request_obj)))
        self.assertTrue(response_obj.return_code == Response.CATEGORY_ERROR, "Category error")

    def test_add_service(self):
        """
        /api/services/<service_name>
        """
        """
            TEST1: POSITIVE : add service via api call
        """
        user_obj = db_model.User(auth_code=None,
                                 phone_number=self.USER_1_PHONE_NUMBER,
                                 handset_serial_number=self.USER_1_HANDSET_SERIAL_NUMBER,
                                 name=None,
                                 email=None)
        request_obj = Request(timestamp=_test_util.get_current_time(), user=user_obj)
        response_obj = _test_util.get_response(
            requests.post('http://' + get_server_config()['server_ip'] + ':' + get_server_config()['server_port'] + '/api/services/' + self.SERVICE_1,
                          json=Request.get_request_json(request_obj)))
        self.assertTrue(response_obj.return_code == Response.SERVICE_ADDED, "Service added response")
        # check in database
        session = self.Session()
        try:
            session.query(db_model.Service).filter(db_model.Service.service_name == self.SERVICE_1).one()
            session.commit()
            self.assertTrue(True, "Service inserted successfully.")
        except sqlalchemy.orm.exc.NoResultFound:
            session.rollback()
            self.fail("No Service row found")

        """
            TEST2: Negative : try to add same category again.
        """
        request_obj = Request(timestamp=_test_util.get_current_time(), user=user_obj)
        response_obj = _test_util.get_response(
            requests.post('http://' + get_server_config()['server_ip'] + ':' + get_server_config()['server_port'] + '/api/services/' + self.SERVICE_1,
                          json=Request.get_request_json(request_obj)))
        self.assertTrue(response_obj.return_code == Response.SERVICE_ERROR, "Service error")

    def test_add_complain(self):
        """
        /api/complains
        """
        """
            TEST1 : NEGATIVE : Invalid request due to unknown user
        """
        user_obj = db_model.User(auth_code=None,
                                 phone_number=self.USER_1_PHONE_NUMBER,
                                 handset_serial_number=self.USER_1_HANDSET_SERIAL_NUMBER,
                                 name=None,
                                 email=None)
        request_obj = Request(timestamp=_test_util.get_current_time(), user=user_obj)
        response_obj = _test_util.get_response(
            requests.post('http://' + get_server_config()['server_ip'] + ':' + get_server_config()['server_port'] + '/api/complains', json=Request.get_request_json(request_obj)))
        self.assertTrue(response_obj.return_code == Response.INVALID_REQUEST, "Invalid request received.")

        """
            TEST2 : NEGATIVE : Empty complain object received.
        """
        # add a user in database.
        user_obj = db_model.User(auth_code=self.USER_1_AUTH_CODE,
                                 phone_number=self.USER_1_PHONE_NUMBER,
                                 handset_serial_number=self.USER_1_HANDSET_SERIAL_NUMBER,
                                 name=self.USER_1_NAME,
                                 email=self.USER_1_EMAIL)
        # add user in database. We must have a valid user in database to get any business info from database.
        _test_util.add_row_in_database(user_obj)
        request_obj = Request(timestamp=_test_util.get_current_time(), user=user_obj)
        response_obj = _test_util.get_response(
            requests.post('http://' + get_server_config()['server_ip'] + ':' + get_server_config()['server_port'] + '/api/complains', json=Request.get_request_json(request_obj)))
        self.assertTrue(response_obj.return_code == Response.EMPTY_COMPLAIN, "Empty complain received.")

        """
            TEST3 : NEGATIVE : Unable to add complain due to invalid category id or/and service id.
        """

        # get the user id from database.
        session = self.Session()
        try:
            user_from_database = session.query(db_model.User).filter(
                db_model.User.phone_number == self.USER_1_PHONE_NUMBER and \
                db_model.User.handset_serial_number == self.USER_1_HANDSET_SERIAL_NUMBER).one()
            session.commit()
            self.assertTrue(True, "User from database")
        except sqlalchemy.orm.exc.NoResultFound:
            session.rollback()
            self.fail("Intended user not found")
        except sqlalchemy.orm.exc.MultipleResultsFound:
            session.rollback()
            self.fail("More than 1 phone number and serial number combination found in database")

        complain_obj = db_model.Complain(user_id=user_from_database.user_id,
                                         category_id=1,
                                         service_id=4,
                                         address='Panchkula',
                                         message='FixShit',
                                         service_status=0,
                                         complain_phone_number=9415549481)
        request_obj = Request(timestamp=_test_util.get_current_time(), user=user_obj, complain=complain_obj)
        response_obj = _test_util.get_response(requests.post('http://' + get_server_config()['server_ip'] + ':' + get_server_config()['server_port'] + '/api/complains',
                                                             json=Request.get_request_json(request_obj)))
        # print(response_obj.return_code)
        self.assertTrue(response_obj.return_code == Response.COMPLAIN_ERROR)

        """
            TEST4 : POSITIVE : Successful addition of complain.
        """
        # add service in database.
        service_obj = db_model.Service(service_name=self.SERVICE_1)
        _test_util.add_row_in_database(service_obj)
        # add category in database.
        _test_util.add_row_in_database(db_model.Category(category_name=self.CATEGORY_1))

        # get the user id from database.
        session = self.Session()
        try:
            service_from_database = session.query(db_model.Service).filter(
                db_model.Service.service_name == self.SERVICE_1).one()
            self.assertTrue(True, "Service from database")
            category_from_database = session.query(db_model.Category).filter(
                db_model.Category.category_name == self.CATEGORY_1).one()
            self.assertTrue(True, "Category from database")
            session.commit()
        except sqlalchemy.orm.exc.NoResultFound:
            session.rollback()
            self.fail("Intended row not found")
        except sqlalchemy.orm.exc.MultipleResultsFound:
            session.rollback()
            self.fail("More than one row found in database")

        complain_obj = db_model.Complain(user_id=user_from_database.user_id,
                                         category_id=category_from_database.category_id,
                                         service_id=service_from_database.service_id, address='Panchkula',
                                         message='FixShit',
                                         service_status=0, complain_phone_number=9415549481)
        request_obj = Request(timestamp=_test_util.get_current_time(), user=user_obj, complain=complain_obj)
        response_obj = _test_util.get_response(requests.post('http://' + get_server_config()['server_ip'] + ':' + get_server_config()['server_port'] + '/api/complains',
                                                             json=Request.get_request_json(request_obj)))
        self.assertTrue(response_obj.return_code == Response.COMPLAIN_ADDED)

        # check if returned complain id is added in server database.
        session = self.Session()
        try:
            session.query(db_model.Complain).filter(
                db_model.Complain.complain_id == response_obj.complain[0]['complain_id']).one()
            self.assertTrue(True, "Query database.")
            session.commit()
        except sqlalchemy.orm.exc.NoResultFound:
            session.rollback()
            self.fail("No row found")

    def test_get_all_categories(self):
        """
        /api/categories
        """
        """
            TEST1 : NEGATIVE : Invalid request due to unknown user
        """
        user_obj = db_model.User(auth_code=None,
                                 phone_number=self.USER_1_PHONE_NUMBER,
                                 handset_serial_number=self.USER_1_HANDSET_SERIAL_NUMBER,
                                 name=None,
                                 email=None)
        request_obj = Request(timestamp=_test_util.get_current_time(), user=user_obj)
        response_obj = _test_util.get_response(
            requests.get('http://' + get_server_config()['server_ip'] + ':' + get_server_config()['server_port'] + '/api/categories', json=Request.get_request_json(request_obj)))
        self.assertTrue(response_obj.return_code == Response.INVALID_REQUEST, "Invalid request received.")
        """
            TEST2 : POSITIVE : no category in database.
        """
        # add a user in database.
        user_obj = db_model.User(auth_code=self.USER_1_AUTH_CODE,
                                 phone_number=self.USER_1_PHONE_NUMBER,
                                 handset_serial_number=self.USER_1_HANDSET_SERIAL_NUMBER,
                                 name=self.USER_1_NAME,
                                 email=self.USER_1_EMAIL)
        # add user in database. We must have a valid user in database to get any business info from database.
        _test_util.add_row_in_database(user_obj)
        # get category list (in this case empty), via api call
        request_obj = Request(timestamp=_test_util.get_current_time(), user=user_obj)
        response_obj = _test_util.get_response(requests.get('http://' + get_server_config()['server_ip'] + ':' + get_server_config()['server_port'] + '/api/categories',
                                                            json=Request.get_request_json(request_obj)))
        self.assertTrue(response_obj.return_code == Response.CATEGORY_LIST_EMPTY, "Category list empty")

        """
            TEST3 : POSITIVE : get all categories in database.
        """
        # add CATEGORY_1
        category_obj_for_db = db_model.Category(category_name=self.CATEGORY_1)
        _test_util.add_row_in_database(category_obj_for_db)
        # add CATEGORY_2
        category_obj_for_db = db_model.Category(category_name=self.CATEGORY_2)
        _test_util.add_row_in_database(category_obj_for_db)

        cat_list = [self.CATEGORY_1, self.CATEGORY_2]

        # get all categories via api call
        request_obj = Request(timestamp=_test_util.get_current_time(), user=user_obj)
        response_obj = _test_util.get_response(requests.get('http://' + get_server_config()['server_ip'] + ':' + get_server_config()['server_port'] + '/api/categories',
                                                            json=Request.get_request_json(request_obj)))
        self.assertTrue(response_obj.return_code == Response.ALL_CATEGORIES,
                        "Return code for category list in database")
        self.assertTrue(len([x for x in response_obj.category if x.get('category_name') in cat_list]) == 2,
                        "Validate returned list")

    def test_get_all_services(self):
        """
        /api/services
        """
        """
            TEST1 : NEGATIVE : Invalid request due to unknown user
        """
        user_obj = db_model.User(auth_code=None,
                                 phone_number=self.USER_1_PHONE_NUMBER,
                                 handset_serial_number=self.USER_1_HANDSET_SERIAL_NUMBER,
                                 name=None,
                                 email=None)
        request_obj = Request(timestamp=_test_util.get_current_time(), user=user_obj)
        response_obj = _test_util.get_response(
            requests.get('http://' + get_server_config()['server_ip'] + ':' + get_server_config()['server_port'] + '/api/services', json=Request.get_request_json(request_obj)))
        self.assertTrue(response_obj.return_code == Response.INVALID_REQUEST, "Invalid request received.")
        """
            TEST2 : POSITIVE : no service in database.
        """
        # get all services via api call
        user_obj = db_model.User(auth_code=self.USER_1_AUTH_CODE,
                                 phone_number=self.USER_1_PHONE_NUMBER,
                                 handset_serial_number=self.USER_1_HANDSET_SERIAL_NUMBER,
                                 name=self.USER_1_NAME,
                                 email=self.USER_1_EMAIL)
        # add user object in database. We must have a valid user in database to get any business info from database.
        _test_util.add_row_in_database(user_obj)
        # get service list (in this case empty), via api call
        request_obj = Request(timestamp=_test_util.get_current_time(), user=user_obj)
        response_obj = _test_util.get_response(requests.get('http://' + get_server_config()['server_ip'] + ':' + get_server_config()['server_port'] + '/api/services',
                                                            json=Request.get_request_json(request_obj)))
        self.assertTrue(response_obj.return_code == Response.SERVICE_LIST_EMPTY, "Category list empty")

        """
            TEST3 : POSITIVE : get all services in database.
        """
        # add SERVICE_1
        service_obj_for_db = db_model.Service(service_name=self.SERVICE_1)
        _test_util.add_row_in_database(service_obj_for_db)
        # add SERVICE_2
        service_obj_for_db = db_model.Service(service_name=self.SERVICE_2)
        _test_util.add_row_in_database(service_obj_for_db)

        ser_list = [self.SERVICE_1, self.SERVICE_2]

        # get all services via api call
        request_obj = Request(timestamp=_test_util.get_current_time(), user=user_obj)
        response_obj = _test_util.get_response(requests.get('http://' + get_server_config()['server_ip'] + ':' + get_server_config()['server_port'] + '/api/services',
                                                            json=Request.get_request_json(request_obj)))
        self.assertTrue(response_obj.return_code == Response.ALL_SERVICES,
                        "Return code for service list in database")
        self.assertTrue(len([x for x in response_obj.service if x.get('service_name') in ser_list]) == 2,
                        "Validate returned list")

    def test_get_complains_for_user(self):
        """
        /api/complain/<user_id>
        """

        """
        TEST1: NEGATIVE : Invalid request due to unknown user in request json.
        """
        user_obj = db_model.User(auth_code=None,
                                 phone_number=self.USER_1_PHONE_NUMBER,
                                 handset_serial_number=self.USER_1_HANDSET_SERIAL_NUMBER,
                                 name=None,
                                 email=None)
        request_obj = Request(timestamp=_test_util.get_current_time(), user=user_obj)
        response_obj = _test_util.get_response(
            requests.get('http://' + get_server_config()['server_ip'] + ':' + get_server_config()['server_port'] + '/api/complain/' + str(1), json=Request.get_request_json(request_obj)))
        self.assertTrue(response_obj.return_code == Response.INVALID_REQUEST, "Invalid request received.")

        """
        TEST2: NEGATIVE : Invalid request due to non-matching user in request json and api
        """
        user_obj_1 = db_model.User(auth_code=self.USER_1_AUTH_CODE,
                                   phone_number=self.USER_1_PHONE_NUMBER,
                                   handset_serial_number=self.USER_1_HANDSET_SERIAL_NUMBER,
                                   name=self.USER_1_NAME,
                                   email=self.USER_1_EMAIL)
        # add a user in database.
        _test_util.add_row_in_database(user_obj_1)

        # get the user id from database.
        session = self.Session()
        try:
            user_from_database = session.query(db_model.User).filter(
                db_model.User.phone_number == self.USER_1_PHONE_NUMBER and \
                db_model.User.handset_serial_number == self.USER_1_HANDSET_SERIAL_NUMBER).one()
            session.commit()
            self.assertTrue(True, "User from database")
        except sqlalchemy.orm.exc.NoResultFound:
            session.rollback()
            self.fail("Intended user not found")
        except sqlalchemy.orm.exc.MultipleResultsFound:
            session.rollback()
            self.fail("More than 1 phone number and serial number combination found in database")

        invalid_user_id = user_from_database.user_id + 1
        request_obj = Request(timestamp=_test_util.get_current_time(), user=user_obj_1)
        response_obj = _test_util.get_response(
            requests.get('http://' + get_server_config()['server_ip'] + ':' + get_server_config()['server_port'] + '/api/complain/' + str(invalid_user_id),
                         json=Request.get_request_json(request_obj)))
        self.assertTrue(response_obj.return_code == Response.INVALID_REQUEST, "Invalid request received.")

        """
        TEST3: POSITIVE : No complains registered for querying user.
        """
        valid_user_id = user_from_database.user_id
        request_obj = Request(timestamp=_test_util.get_current_time(), user=user_obj_1)
        response_obj = _test_util.get_response(
            requests.get('http://' + get_server_config()['server_ip'] + ':' + get_server_config()['server_port'] + '/api/complain/' + str(valid_user_id),
                         json=Request.get_request_json(request_obj)))
        self.assertTrue(response_obj.return_code == Response.COMPLAIN_LIST_EMPTY, "No complains for this user.")

        """
        TEST4: POSITIVE : List of complains registered for querying user.
        """

        # add CATEGORY_1
        category_obj_for_db = db_model.Category(category_name=self.CATEGORY_1)
        _test_util.add_row_in_database(category_obj_for_db)
        # add CATEGORY_2
        category_obj_for_db = db_model.Category(category_name=self.CATEGORY_2)
        _test_util.add_row_in_database(category_obj_for_db)

        # add SERVICE_1
        service_obj_for_db = db_model.Service(service_name=self.SERVICE_1)
        _test_util.add_row_in_database(service_obj_for_db)
        # add SERVICE_2
        service_obj_for_db = db_model.Service(service_name=self.SERVICE_2)
        _test_util.add_row_in_database(service_obj_for_db)

        # add user 2
        user_obj_2 = db_model.User(auth_code=self.USER_2_AUTH_CODE,
                                   phone_number=self.USER_2_PHONE_NUMBER,
                                   handset_serial_number=self.USER_2_HANDSET_SERIAL_NUMBER,
                                   name=self.USER_2_NAME,
                                   email=self.USER_2_EMAIL)
        # add a user in database.
        _test_util.add_row_in_database(user_obj_2)

        # get all ids from database , required for creating new complains.
        session = self.Session()
        try:
            category_1 = session.query(db_model.Category).filter(
                db_model.Category.category_name == self.CATEGORY_1).one()
            category_2 = session.query(db_model.Category).filter(
                db_model.Category.category_name == self.CATEGORY_2).one()
            service_1 = session.query(db_model.Service).filter(db_model.Service.service_name == self.SERVICE_1).one()
            service_2 = session.query(db_model.Service).filter(db_model.Service.service_name == self.SERVICE_2).one()
            user_1 = session.query(db_model.User).filter(
                db_model.User.phone_number == self.USER_1_PHONE_NUMBER and \
                db_model.User.handset_serial_number == self.USER_1_HANDSET_SERIAL_NUMBER).one()
            user_2 = session.query(db_model.User).filter(
                db_model.User.phone_number == self.USER_2_PHONE_NUMBER and \
                db_model.User.handset_serial_number == self.USER_2_HANDSET_SERIAL_NUMBER).one()
            self.assertTrue(True, "Query database.")
            session.rollback()
        except sqlalchemy.orm.exc.NoResultFound:
            session.rollback()
            self.fail("No row found")

        # add complains via Complain api.
        complain_1 = db_model.Complain(
            user_id=user_1.user_id,
            category_id=category_1.category_id,
            service_id=service_1.service_id,
            address=self.ADDRESS_1,
            message=self.MESSAGE_1,
            service_status=0,
            complain_phone_number=self.USER_2_PHONE_NUMBER)
        complain_2 = db_model.Complain(
            user_id=user_1.user_id,
            category_id=category_2.category_id,
            service_id=service_2.service_id,
            address=self.ADDRESS_2,
            message=self.MESSAGE_2,
            service_status=0,
            complain_phone_number=self.USER_2_PHONE_NUMBER)
        complain_3 = db_model.Complain(
            user_id=user_2.user_id,
            category_id=category_1.category_id,
            service_id=service_1.service_id,
            address=self.ADDRESS_1,
            message=self.MESSAGE_1,
            service_status=0,
            complain_phone_number=self.USER_2_PHONE_NUMBER)

        complain_4 = db_model.Complain(
            user_id=user_2.user_id,
            category_id=category_2.category_id,
            service_id=service_2.service_id,
            address=self.ADDRESS_2,
            message=self.MESSAGE_2,
            service_status=0,
            complain_phone_number=self.USER_2_PHONE_NUMBER)

        _test_util.add_row_in_database(complain_1)
        _test_util.add_row_in_database(complain_2)
        _test_util.add_row_in_database(complain_3)
        _test_util.add_row_in_database(complain_4)

        # request for user_1 complains
        request_obj = Request(timestamp=_test_util.get_current_time(), user=user_obj_1)
        response_obj = _test_util.get_response(
            requests.get('http://' + get_server_config()['server_ip'] + ':' + get_server_config()['server_port'] + '/api/complain/' + str(user_obj_1.user_id),
                         json=Request.get_request_json(request_obj)))
        self.assertTrue(response_obj.return_code == Response.ALL_COMPLAINS, "All complains for this user.")
        self.assertTrue(response_obj.complain == [AlchemyEncoder.get_pickle_dict(complain_1),
                                                  AlchemyEncoder.get_pickle_dict(complain_2)],
                        "All complains for this user.")

        # request for user_2 complains
        request_obj = Request(timestamp=_test_util.get_current_time(), user=user_obj_2)
        response_obj = _test_util.get_response(
            requests.get('http://' + get_server_config()['server_ip'] + ':' + get_server_config()['server_port'] + '/api/complain/' + str(user_obj_2.user_id),
                         json=Request.get_request_json(request_obj)))
        self.assertTrue(response_obj.return_code == Response.ALL_COMPLAINS, "All complains for this user.")
        self.assertTrue(response_obj.complain == [AlchemyEncoder.get_pickle_dict(complain_3),
                                                  AlchemyEncoder.get_pickle_dict(complain_4)],
                        "All complains for this user.")


    def test_update_complain(self):
        """
        /api/complain/<complain_id>
        """
        """
            TEST1 : NEGATIVE : invalid request.
        """
        user_obj = db_model.User(auth_code=None,
                                 phone_number=self.USER_1_PHONE_NUMBER,
                                 handset_serial_number=self.USER_1_HANDSET_SERIAL_NUMBER,
                                 name=None,
                                 email=None)
        request_obj = Request(timestamp=_test_util.get_current_time(), user=user_obj)
        response_obj = _test_util.get_response(
            requests.put('http://' + get_server_config()['server_ip'] + ':' + get_server_config()['server_port'] + '/api/complain/' + str(1), json=Request.get_request_json(request_obj)))
        self.assertTrue(response_obj.return_code == Response.INVALID_REQUEST, "Invalid request received.")

        """
            TEST2 : NEGATIVE : valid request but invalid <complain_id> triggered for update.
        """
        # add user.
        user_obj = db_model.User(auth_code=self.USER_1_AUTH_CODE,
                                   phone_number=self.USER_1_PHONE_NUMBER,
                                   handset_serial_number=self.USER_1_HANDSET_SERIAL_NUMBER,
                                   name=self.USER_1_NAME,
                                   email=self.USER_1_EMAIL)
        # add a user in database.
        _test_util.add_row_in_database(user_obj)
        # trigger update request.
        request_obj = Request(timestamp=_test_util.get_current_time(), user=user_obj)
        response_obj = _test_util.get_response(
            requests.put('http://' + get_server_config()['server_ip'] + ':' + get_server_config()['server_port'] + '/api/complain/' + str(100), json=Request.get_request_json(request_obj)))
        self.assertTrue(response_obj.return_code == Response.COMPLAIN_ERROR, "Invalid request received.")

        """
            TEST3 : POSITIVE : valid request.
        """
        # add CATEGORY_1 in database
        category_obj_for_db = db_model.Category(category_name=self.CATEGORY_1)
        _test_util.add_row_in_database(category_obj_for_db)
        # add SERVICE_1 in database
        service_obj_for_db = db_model.Service(service_name=self.SERVICE_1)
        _test_util.add_row_in_database(service_obj_for_db)
        # add complain in database
        complain_obj = db_model.Complain(
            user_id=user_obj.user_id,
            category_id=category_obj_for_db.category_id,
            service_id=service_obj_for_db.service_id,
            address=self.ADDRESS_2,
            message=self.MESSAGE_2,
            service_status=0,
            complain_phone_number=self.USER_2_PHONE_NUMBER)
        # add a complain in database.
        _test_util.add_row_in_database(complain_obj)

        updated_complain_obj = db_model.Complain(
            user_id=user_obj.user_id,
            category_id=category_obj_for_db.category_id,
            service_id=service_obj_for_db.service_id,
            address=self.ADDRESS_1,
            message=self.MESSAGE_1,
            service_status=2,
            complain_phone_number=self.USER_1_PHONE_NUMBER)

        # trigger update request.
        request_obj = Request(timestamp=_test_util.get_current_time(), user=user_obj, complain=updated_complain_obj)
        response_obj = _test_util.get_response(
            requests.put('http://' + get_server_config()['server_ip'] + ':' + get_server_config()['server_port'] + '/api/complain/' + str(complain_obj.complain_id), json=Request.get_request_json(request_obj)))
        self.assertTrue(response_obj.return_code == Response.COMPLAIN_UPDATED, "Valid request received.")
        session = self.Session()
        try:
            complain_from_database = session.query(db_model.Complain).filter(
                db_model.Complain.user_id == user_obj.user_id).one()
            self.assertTrue(True, "Query database.")
            session.commit()
        except sqlalchemy.orm.exc.NoResultFound:
            session.rollback()
            self.fail("No row found")
        self.assertTrue(response_obj.complain == [AlchemyEncoder.get_pickle_dict(complain_from_database)], "Valid request received.")



    def test_update_user(self):
        """
        /api/user/<user_id>
        """
        """
            TEST1 : NEGATIVE : invalid request.
        """
        user_obj = db_model.User(auth_code=None,
                                 phone_number=self.USER_1_PHONE_NUMBER,
                                 handset_serial_number=self.USER_1_HANDSET_SERIAL_NUMBER,
                                 name=None,
                                 email=None)
        request_obj = Request(timestamp=_test_util.get_current_time(), user=user_obj)
        response_obj = _test_util.get_response(
            requests.put('http://' + get_server_config()['server_ip'] + ':' + get_server_config()['server_port'] + '/api/user/' + str(1), json=Request.get_request_json(request_obj)))
        self.assertTrue(response_obj.return_code == Response.INVALID_REQUEST, "Invalid request received.")

        """
            TEST2 : NEGATIVE : valid request but invalid <user_id> in api request.
        """
        # add user.
        user_obj = db_model.User(auth_code=self.USER_1_AUTH_CODE,
                                   phone_number=self.USER_1_PHONE_NUMBER,
                                   handset_serial_number=self.USER_1_HANDSET_SERIAL_NUMBER,
                                   name=self.USER_1_NAME,
                                   email=self.USER_1_EMAIL)
        # add a user in database.
        _test_util.add_row_in_database(user_obj)
        # trigger update request.
        request_obj = Request(timestamp=_test_util.get_current_time(), user=user_obj)
        response_obj = _test_util.get_response(
            requests.put('http://' + get_server_config()['server_ip'] + ':' + get_server_config()['server_port'] + '/api/user/' + str(100), json=Request.get_request_json(request_obj)))
        self.assertTrue(response_obj.return_code == Response.USER_ERROR, "Invalid request received.")

        """
            TEST3 : NEGATIVE : Invalid request, cannot update Phone number and serial number.
        """
        session = self.Session()
        try:
            user_from_database = session.query(db_model.User).filter(
                db_model.User.auth_code == user_obj.auth_code).one()
            self.assertTrue(True, "Query database.")
            session.commit()
        except sqlalchemy.orm.exc.NoResultFound:
            session.rollback()
            self.fail("No row found")

        update_user_obj = db_model.User(
                                   auth_code=self.USER_1_AUTH_CODE,
                                   phone_number=self.USER_2_PHONE_NUMBER, # changed number
                                   handset_serial_number=self.USER_2_HANDSET_SERIAL_NUMBER, # changed serial number
                                   name=self.USER_2_NAME,
                                   email=self.USER_2_EMAIL)

        # trigger update request.
        request_obj = Request(timestamp=_test_util.get_current_time(), user=update_user_obj)
        response_obj = _test_util.get_response(
            requests.put('http://' + get_server_config()['server_ip'] + ':' + get_server_config()['server_port'] + '/api/user/' + str(user_from_database.user_id), json=Request.get_request_json(request_obj)))
        self.assertTrue(response_obj.return_code == Response.INVALID_REQUEST, "Valid request received.")

        """
            TEST4 : POSITIVE : Valid request.
        """
        update_user_obj = db_model.User(
                                   auth_code=self.USER_1_AUTH_CODE,
                                   phone_number=self.USER_1_PHONE_NUMBER,
                                   handset_serial_number=self.USER_1_HANDSET_SERIAL_NUMBER,
                                   name=self.USER_2_NAME, # changed name
                                   email=self.USER_2_EMAIL) # changed email

        # trigger update request.
        request_obj = Request(timestamp=_test_util.get_current_time(), user=update_user_obj)
        response_obj = _test_util.get_response(
            requests.put('http://' + get_server_config()['server_ip'] + ':' + get_server_config()['server_port'] + '/api/user/' + str(user_from_database.user_id),
                         json=Request.get_request_json(request_obj)))
        self.assertTrue(response_obj.return_code == Response.USER_UPDATED, "Valid update request received.")
        self.assertTrue(response_obj.user['name'] == self.USER_2_NAME, "Updated name.")
        self.assertTrue(response_obj.user['email'] == self.USER_2_EMAIL, "Updated email.")


    def tearDown(self):
        # pass
        _test_util.clear_up_db()
