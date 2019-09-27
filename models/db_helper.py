import traceback
from os import sys

import sqlalchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from api.json.json_request import Request
from api.json.json_response import *
from api.otp import OTP
from api.utils import create_sqlalchemy_engine, send_otp_message
from models import db_model


# class Singleton(object):
#     _instances = {}
#
#     def __new__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             cls._instances[cls] = super(Singleton, cls).__new__(cls, *args, **kwargs)
#         return cls._instances[cls]

class DbHelper(object):
    def __init__(self):

        # establish connection with sql server
        self.engine = create_sqlalchemy_engine()
        # create a session
        self.Session = sessionmaker(bind=self.engine, expire_on_commit=True)
        self.otpObj = OTP()

    def init_db(self):
        # create table from ORM models
        db_model.create_model(self.engine)

    def __is_valid_request__(self, http_request: Request):
        """
        Validates Requests. 
        :param http_request: Incoming Request object.
        :return: Boolean validity
        """
        valid = False
        session = self.Session()
        try:
            q_count = session.query(db_model.User).filter(
                db_model.User.auth_code == http_request.user.auth_code,
                db_model.User.phone_number == http_request.user.phone_number,
                db_model.User.handset_serial_number == http_request.user.handset_serial_number
                                                    ).count()
            # should be 1 row only, primary constraint
            if q_count == 1:
                valid = True
            session.commit()
        except Exception as e:
            ret = "something shitty" + str(e.__dict__)
            print(ret)
            session.rollback()
        finally:
            session.close()

        return valid

    def __add_user__(self, http_request, auth_code):
        """
        Adds a new User
        :param http_request: Incoming Request
        :param auth_code: Unique auth code for a User
        :return: bottle.HTTPResponse 
          
        """
        new_user_obj = None
        success = False
        if auth_code is not None:
            session = self.Session()
            new_user_obj = db_model.User(phone_number=http_request.user.phone_number,
                                         handset_serial_number=http_request.user.handset_serial_number,
                                         auth_code=auth_code,
                                         timestamp=http_request.timestamp,
                                         name=http_request.user.name,
                                         email=http_request.user.email,
                                         dirty_bit=True)
            try:
                session.add(new_user_obj)
                session.refresh(new_user_obj)
                success = True
                session.commit()
            except IntegrityError as ie:
                ret = "ERROR: " + ie.detail
                print(ret)
                session.rollback()
            except Exception as e:
                ret = "ERROR: " + str(e.__dict__)
                print(ret)
                session.rollback()
            finally:
                session.close()
        # TODO: Should return User object instead of HTTP response. As this a private call, the wrapper functions should take care of the HTTP returns.
        return user_created_response(new_user_obj, success)


    def add_category(self, http_request, category_name):
        """
        Adds Category in database
        :param http_request: Incoming Request 
        :param category_name: Name of the Category to be added.
        :return: bottle.HTTPResponse 
        """

        session = self.Session()
        success = False
        try:
            # return number of rows, as primary, should be 1 or 0.
            q = session.query(db_model.Category).filter(db_model.Category.category_name == category_name).first()
            try:
                if q is None:
                    session.add(db_model.Category(category_name=category_name))
                    session.commit()
                    success = True
            except IntegrityError as e:
                ret = "something shitty" + e.detail
                print(ret)
                raise
        except Exception as e1:
            ret = "ERROR: " + str(e1.__dict__)
            print(ret)
            session.rollback()
        finally:
            session.close()

        return add_category_response(http_request, category_name, success)


    def add_service(self, http_request, service_name):
        """
        Adds Service in database
        :param http_request: Incoming Request 
        :param service_name: Name of the Service to be added.
        :return: bottle.HTTPResponse 
        """
        session = self.Session()
        success = False

        try:
            # return number of rows, as primary, should be 1 or 0.
            q = session.query(db_model.Service).filter(db_model.Service.service_name == service_name).first()
            try:
                if q is None:
                    session.add(db_model.Service(service_name=service_name))
                    session.commit()
                    success = True
            except IntegrityError as e:
                ret = "ERROR: " + e.detail
                print(ret)
                raise
        except Exception as e1:
            ret = "ERROR: " + str(e1.__dict__)
            print(ret)
            session.rollback()
        finally:
            session.close()

        return add_service_response(http_request, service_name, success)


    def add_complain(self, http_request):
        """
        Adds new Complain
        :param http_request: Incoming Request containing Complain object for a new Complain to added in database.
        :return: bottle.HTTPResponse 
        """
        session = self.Session()
        new_complain_obj = http_request.complain
        success = False
        if self.__is_valid_request__(http_request):
            if new_complain_obj is not None:
                try:
                    session.add(new_complain_obj)
                    # print("Is the new id generated? " + str(new_complain_obj.complain_id))

                    # TODO the timestamp which is auto-generated when new row is added in Complain table
                    # is not updated in the `new_complain_obj` object, thus in response this is Null
                    session.commit()
                    session.refresh(new_complain_obj)
                    success = True
                except IntegrityError as ie:
                    ret = str(ie.__dict__)
                    # print(ret)
                    session.rollback()
                finally:
                    session.close()
                return add_new_complain_response(http_request, new_complain_obj, success)
            else:
                return failure_response(http_request, Response.EMPTY_COMPLAIN)
        else:
            return invalid_request_received_response(http_request)

    def verify_otp_and_create_user(self, http_request, otp: str):
        """
        Verifies OTP string and returns new User object wrapped in Response on success. 
        :param http_request: Incoming Request
        :param otp: String OTP to be verified.
        :return: bottle.HTTPResponse 
        """
        # verify otp and otp timeout
        if self.otpObj.validate_otp(otp, http_request.timestamp, http_request.user.phone_number):
            return self.__add_user__(http_request, self.otpObj.get_hash_code(http_request.user.phone_number))
        else:
            return failure_response(http_request, Response.OTP_ERROR)

    def get_otp_for_new_user(self, http_request):
        """
        Generates OTP for new User and triggers a message routine to send SMS to the User's phone number. 
        :param http_request: Incoming Request 
        :return: bottle.HTTPResponse 
        """
        try:
            # generate otp and auth code
            str_code, auth_code = DbHelper().otpObj.generate_otp(
                http_request.user.handset_serial_number,
                http_request.user.phone_number,
                http_request.timestamp)
            # print(str_code, auth_code)
            # send otp message to the client
            send_otp_message(str_code, http_request.user.phone_number)
            return new_user_response(http_request)
        except Exception as e:
            ret = "ERROR: " + e.__traceback__.__str__()
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print(traceback.print_exception(exc_type, exc_value, exc_traceback,
                                                   limit=5, file=sys.stdout))
            print(ret)
            return failure_response(http_request, Response.OTP_ERROR)

    def is_user_exists(self, http_request: Request):
        """
        Checks if User exists in database. Returns HTTP response on success or failure.
        :param http_request: Incoming Request 
        :return: bottle.HTTPResponse 
        """
        success = False
        session = self.Session()
        user_obj = None
        try:
            # return number of rows, as primary, should be 1 or 0.
            user_obj = session.query(db_model.User).filter(
                db_model.User.phone_number == http_request.user.phone_number,
                db_model.User.handset_serial_number == http_request.user.handset_serial_number).first()
            session.commit()
            if user_obj is not None:
                success = True

        except Exception as e:
            session.rollback()
        # finally:
        #     session.close()

        return is_user_exists_response(http_request, user_obj, success)


    def get_all_categories(self, http_request):
        """
        Returns a list of Categories wrapped in HTTPResponse. 
        :param http_request: Incoming Request
        :return: bottle.HTTPResponse  
        """
        category_collection = []
        session = self.Session()
        try:
            if self.__is_valid_request__(http_request):
                categories = session.query(db_model.Category).all()

                for category in categories:
                    category_collection.append(category)
                session.commit()
            else:
                return invalid_request_received_response(http_request)

        except Exception as e:
            ret = "ERROR: " + e.__traceback__.__str__()
            print(ret)
            session.rollback()
        # finally:
        #     session.close()

        return all_categories_response(http_request, category_collection)

    def get_all_services(self, http_request):
        """
        Returns a list of Services wrapped in HTTPResponse.
        :param http_request: Incoming Request
        :return: bottle.HTTPResponse  
        """
        service_collection = []
        session = self.Session()
        try:
            if self.__is_valid_request__(http_request):
                services = session.query(db_model.Service).all()

                for service in services:
                    service_collection.append(service)
                session.commit()
            else:
                return invalid_request_received_response(http_request)
        except Exception as e:
            ret = "ERROR: " + str(e.__dict__)
            print(ret)
            session.rollback()
        # finally:
        #     session.close()

        return all_services_response(http_request, service_collection)

    def get_complains_for_user(self, http_request, user_id):
        """
        Returns a list of Complains present filtered by the user_id, wrapped in HTTPResponses.
        :param http_request: Incoming Request
        :param user_id: User identifier to filter complains in database.
        :return: bottle.HTTPResponse 
        """
        complain_collection = []
        session = self.Session()
        try:
            if self.__is_valid_request__(http_request) and user_id == str(http_request.user.user_id):
                complains = session.query(db_model.Complain).filter(db_model.Complain.user_id == user_id).all()

                for complain in complains:
                    complain_collection.append(complain)
                session.commit()
            else:
                return invalid_request_received_response(http_request)
        except Exception as e:
            ret = "ERROR: " + str(e.__dict__)
            print(ret)
            session.rollback()
        # finally:
        #     session.close()

        return all_complains_for_user_response(http_request, complain_collection)


    def update_complain(self, http_request, complain_id):
        """
        Updates a Complain using complain_id. 
        UseCase : Admin may want to update Status information 
        :param http_request: Incoming Request
        :param complain_id: Comaplain unique identifier
        :return: bottle.HTTPResponse 
        """
        session = self.Session()
        success = False
        complain_obj = None
        try:
            if self.__is_valid_request__(http_request):
                complain_obj = session.query(db_model.Complain).filter(db_model.Complain.complain_id == complain_id).one()
                # TODO do we want to update any other column ?
                complain_obj.address = http_request.complain.address
                complain_obj.message = http_request.complain.message
                complain_obj.service_status = http_request.complain.service_status
                complain_obj.complain_phone_number = http_request.complain.complain_phone_number
                # merge to update
                session.merge(complain_obj)
                session.commit()
                success = True
            else:
                return invalid_request_received_response(http_request)

        except sqlalchemy.orm.exc.NoResultFound:
            session.rollback()
        except Exception as e:
            ret = "ERROR: " + e.__str__()
            print(ret)
            session.rollback()
        # finally:
        #     session.close()

        return update_complain_response(http_request, complain_obj, success)


    def update_user(self, http_request, user_id):
        """
        Update User information.
        UseCase 1: Admin may want to update some user info for some business value, which may not be available with the User.
        UseCase 2: User may update some non-mandatory personal information via App.
        :param http_request: Incoming Request
        :param user_id: Unique User identifier
        :return: bottle.HTTPResponse 
        """
        session = self.Session()
        success = False
        user_obj = None
        try:
            if self.__is_valid_request__(http_request):
                user_obj = session.query(db_model.User).filter(db_model.User.user_id == user_id,
                                                               db_model.User.auth_code == http_request.user.auth_code).one()
                # TODO do we want to update any other column ?
                user_obj.name = http_request.user.name
                user_obj.email = http_request.user.email
                # merge to update
                session.merge(user_obj)
                session.commit()
                success = True
            else:
                return invalid_request_received_response(http_request)
        except Exception as e:
            ret = "ERROR: " + e.__str__()
            # print(ret)
            session.rollback()
        # finally:
        #     session.close()
        return update_user_response(http_request, user_obj, success)

if __name__ == '__main__':
    db =  DbHelper()