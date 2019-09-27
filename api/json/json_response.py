import json

import bottle
import jsonpickle
from sqlalchemy.ext.declarative import DeclarativeMeta

from api.json.json_request import Request
from models.db_model import User, Category, Service, Complain

"""
Here we should have all responses for the REST APIs.
"""


class Response(object):

    SUCCESS =               101
    FAILURE =               102
    INVALID_REQUEST =       103
    USER_EXISTS =           104
    USER_NOT_EXIST =        105
    NEW_USER =              106
    USER_CREATED =          107
    USER_CREATION_ERROR =   108
    USER_ERROR =            109
    CATEGORY_ADDED =        110
    CATEGORY_ERROR =        111
    CATEGORY_LIST_EMPTY =   112
    SERVICE_ADDED =         113
    SERVICE_ERROR =         114
    SERVICE_LIST_EMPTY =    115
    ALL_CATEGORIES =        116
    ALL_SERVICES =          117
    EMPTY_COMPLAIN =        118
    COMPLAIN_ADDED =        119
    COMPLAIN_ERROR =        120
    OTP_ERROR =             121
    COMPLAIN_UPDATED =      122
    USER_UPDATED =          123
    ALL_COMPLAINS =         124
    COMPLAIN_LIST_EMPTY =   125

    def __init__(self, return_code, user=None, category=None, service=None, complain=None):
        self.return_code = return_code

        self.user = AlchemyEncoder.get_pickle_dict(user)
        self.category = AlchemyEncoder.get_pickle_dict(category)
        self.service = AlchemyEncoder.get_pickle_dict(service)
        self.complain = AlchemyEncoder.get_pickle_dict(complain)

    @staticmethod
    def get_response_json(obj):
        """
        Create a pickled json object
        :param obj: Response object to be pickled.
        :return: Encoded pickled string. 
        """
        # could have just used json.dump
        # jsonpickle.set_encoder_options()
        jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4)
        try:
            if isinstance(obj, Response):
                return jsonpickle.encode(obj, unpicklable=True, max_depth=4)
            else:
                raise TypeError
        except TypeError:
            return jsonpickle.encode(Response(Response.FAILURE), unpicklable=True)



class AlchemyEncoder():
    """
            dump json your way, strip out Alchemy Metadata from Table object's json representations.
            
    """
    @staticmethod
    def get_pickle_dict(obj):
        # in case of list of objects we would get trimmed list
        if isinstance(obj, list):
            ret_list = []
            for list_obj in obj:
                ret_list.append(AlchemyEncoder.__remove_declarative_meta__(list_obj))
            return ret_list
        else:
            return AlchemyEncoder.__remove_declarative_meta__(obj)


    @staticmethod
    def __remove_declarative_meta__(obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            # dir(obj) : Provide all the attributes for a passed `obj`
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields
        return None


def new_user_response(http_request: Request):
    return bottle.HTTPResponse(status=200, body=Response.get_response_json(Response(
        return_code=Response.NEW_USER,
        user=http_request.user
    )))


def is_user_exists_response(http_request: Request, user_db_obj: User, success: bool):
    if success:
        return bottle.HTTPResponse(status=200, body=Response.get_response_json(Response(
            return_code=Response.USER_EXISTS,
            user=user_db_obj
        )))
    else:
        return bottle.HTTPResponse(status=200, body=Response.get_response_json(Response(
            return_code=Response.USER_NOT_EXIST,
            user=User(
                auth_code=None,
                phone_number=http_request.user.phone_number,
                handset_serial_number=http_request.user.handset_serial_number
            )
        )))


def user_created_response(user_obj: User, success: bool):
    if success:
        return bottle.HTTPResponse(status=200, body=Response.get_response_json(Response(
            return_code=Response.USER_CREATED,
            user=user_obj
        )))
    else:
        return bottle.HTTPResponse(status=500, body=Response.get_response_json(Response(
            return_code=Response.USER_CREATION_ERROR,
            user=user_obj
        )))

def failure_response(http_request: Request, failure_code=Response.FAILURE):
    return bottle.HTTPResponse(status=500, body=Response.get_response_json(Response(
        return_code=failure_code,
        user=User(
            auth_code=http_request.user.auth_code,
            phone_number=http_request.user.phone_number,
            handset_serial_number=http_request.user.handset_serial_number
        )
    )))


def invalid_request_received_response(http_request: Request):
    return bottle.HTTPResponse(status=500, body=Response.get_response_json(Response(
        return_code=Response.INVALID_REQUEST,
        user=User(
            auth_code=http_request.user.auth_code,
            phone_number=http_request.user.phone_number,
            handset_serial_number=http_request.user.handset_serial_number
        )
    )))


def add_category_response(http_request: Request, category_name: str, success: bool):
    if success:
        return bottle.HTTPResponse(status=200, body=Response.get_response_json(Response(
            return_code=Response.CATEGORY_ADDED,
            user=User(
                auth_code=http_request.user.auth_code,
                phone_number=http_request.user.phone_number,
                handset_serial_number=http_request.user.handset_serial_number
            ),
            category=[Category(category_name=category_name)]
        )))
    else:
        return bottle.HTTPResponse(status=500, body=Response.get_response_json(Response(
            return_code=Response.CATEGORY_ERROR,
            user=User(
                auth_code=http_request.user.auth_code,
                phone_number=http_request.user.phone_number,
                handset_serial_number=http_request.user.handset_serial_number
            ),
            category=[Category(category_name=category_name)]
        )))


def add_service_response(http_request: Request, service_name: str, success: bool):
    if success:
        return bottle.HTTPResponse(status=200, body=Response.get_response_json(Response(
            return_code=Response.SERVICE_ADDED,
            user=User(
                auth_code=http_request.user.auth_code,
                phone_number=http_request.user.phone_number,
                handset_serial_number=http_request.user.handset_serial_number
            ),
            service=[Service(service_name=service_name)]
        )))
    else:
        return bottle.HTTPResponse(status=500, body=Response.get_response_json(Response(
            return_code=Response.SERVICE_ERROR,
            user=User(
                auth_code=http_request.user.auth_code,
                phone_number=http_request.user.phone_number,
                handset_serial_number=http_request.user.handset_serial_number
            ),
            service=[Service(service_name=service_name)]
        )))


def all_categories_response(http_request: Request, db_category_collection):

    if db_category_collection :

        return bottle.HTTPResponse(status=200, body=Response.get_response_json(Response(
            return_code=Response.ALL_CATEGORIES,
            user=User(
                auth_code=http_request.user.auth_code,
                phone_number=http_request.user.phone_number,
                handset_serial_number=http_request.user.handset_serial_number
            ),
            category=db_category_collection
        )))

    else:
        return bottle.HTTPResponse(status=200, body=Response.get_response_json(Response(
            return_code=Response.CATEGORY_LIST_EMPTY,
            user=User(
                auth_code=http_request.user.auth_code,
                phone_number=http_request.user.phone_number,
                handset_serial_number=http_request.user.handset_serial_number
            ),
            category=db_category_collection
        )))


def all_services_response(http_request: Request, db_service_collection):

    if db_service_collection :
        return bottle.HTTPResponse(status=200, body=Response.get_response_json(Response(
            return_code=Response.ALL_SERVICES,
            user=User(
                auth_code=http_request.user.auth_code,
                phone_number=http_request.user.phone_number,
                handset_serial_number=http_request.user.handset_serial_number
            ),
            service=db_service_collection
        )))
    else:
        return bottle.HTTPResponse(status=200, body=Response.get_response_json(Response(
            return_code=Response.SERVICE_LIST_EMPTY,
            user=User(
                auth_code=http_request.user.auth_code,
                phone_number=http_request.user.phone_number,
                handset_serial_number=http_request.user.handset_serial_number
            ),
            category=db_service_collection
        )))


def all_complains_for_user_response(http_request: Request, db_complain_collection):
    if db_complain_collection :
        return bottle.HTTPResponse(status=200, body=Response.get_response_json(Response(
            return_code=Response.ALL_COMPLAINS,
            user=User(
                auth_code=http_request.user.auth_code,
                phone_number=http_request.user.phone_number,
                handset_serial_number=http_request.user.handset_serial_number
            ),
            complain=db_complain_collection
        )))
    else:
        return bottle.HTTPResponse(status=200, body=Response.get_response_json(Response(
            return_code=Response.COMPLAIN_LIST_EMPTY,
            user=User(
                auth_code=http_request.user.auth_code,
                phone_number=http_request.user.phone_number,
                handset_serial_number=http_request.user.handset_serial_number
            ),
            complain=db_complain_collection
        )))


def add_new_complain_response(http_request: Request, new_complain_obj, success: bool):
    if success:
        return bottle.HTTPResponse(status=200, body=Response.get_response_json(Response(
            return_code=Response.COMPLAIN_ADDED,
            user=User(
                auth_code=http_request.user.auth_code,
                phone_number=http_request.user.phone_number,
                handset_serial_number=http_request.user.handset_serial_number
            ),
            complain=[new_complain_obj]
        )))
    else:
        return bottle.HTTPResponse(status=500, body=Response.get_response_json(Response(
            return_code=Response.COMPLAIN_ERROR,
            user=User(
                auth_code=http_request.user.auth_code,
                phone_number=http_request.user.phone_number,
                handset_serial_number=http_request.user.handset_serial_number
            ),
            complain=[new_complain_obj]
        )))


def update_complain_response(http_request: Request, complain_obj: Complain, success: bool):
    if success:
        return bottle.HTTPResponse(status=200, body=Response.get_response_json(Response(
            return_code=Response.COMPLAIN_UPDATED,
            user=User(
                auth_code=http_request.user.auth_code,
                phone_number=http_request.user.phone_number,
                handset_serial_number=http_request.user.handset_serial_number
            ),
            complain=[complain_obj]
        )))
    else:
        return bottle.HTTPResponse(status=500, body=Response.get_response_json(Response(
            return_code=Response.COMPLAIN_ERROR,
            user=User(
                auth_code=http_request.user.auth_code,
                phone_number=http_request.user.phone_number,
                handset_serial_number=http_request.user.handset_serial_number
            )
        )))


def update_user_response(http_request: Request, user_obj: User, success: bool):
    if success:
        return bottle.HTTPResponse(status=200, body=Response.get_response_json(Response(
            return_code=Response.USER_UPDATED,
            user=user_obj
        )))
    else:
        return bottle.HTTPResponse(status=500, body=Response.get_response_json(Response(
            return_code=Response.USER_ERROR,
            user=User(
                auth_code=http_request.user.auth_code,
                phone_number=http_request.user.phone_number,
                handset_serial_number=http_request.user.handset_serial_number
            )
        )))

if __name__ == '__main__':

    user = User(auth_code = 'ccf6cebd53549f1d74a82bb455d907648fa28d0c',
                   phone_number = 9780044091,
                   handset_serial_number = 'JLIU897978F',
                   name = None,
                   email = None)
    categoryObj = Category(category_name = 5467)
    serviceObj = Service(service_name=1234)
    complainObj = Complain(address = 'A-98',
                           message = 'Repair my arse',
                           service_status = '0',
                           complain_phone_number = None)

    responseObj = Response(return_code=Response.SUCCESS,
                           user=user,
                           category=[categoryObj],
                           service=[serviceObj],
                           complain=[complainObj])
    print(Response.get_response_json(responseObj))