import datetime

import jsonpickle
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from api.json import json_response
from api.utils import create_sqlalchemy_engine
from models import db_model


def clear_up_db():
    # establish connection with sql server
    engine = create_sqlalchemy_engine()
    # create table from ORM models
    db_model.create_model(engine)
    # create a session
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        session.query(db_model.Complain).delete()
        session.query(db_model.User).delete()
        session.query(db_model.Service).delete()
        session.query(db_model.Category).delete()

        session.commit()
    except Exception as e:
        ret = "ERROR: " + str(e.__dict__)
        print(ret)
        session.rollback()


def add_row_in_database(row_object):
    # establish connection with sql server
    engine = create_sqlalchemy_engine()
    # create a session
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        session.add(row_object)
        session.commit()
        session.refresh(row_object)

    except IntegrityError as ie:
        ret = "ERROR: " + ie.detail
        print(ret)
        session.rollback()
    except Exception as e:
        ret = "ERROR: " + e.__traceback__.__str__()
        print(ret)
        session.rollback()
    finally:
        engine.dispose()


def get_user_by_phone_and_serial_number(phone_number, handset_serial_number):
    # establish connection with sql server
    engine = create_sqlalchemy_engine()
    # create a session
    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(db_model.User).filter(
        db_model.User.phone_number == phone_number,
        db_model.User.handset_serial_number == handset_serial_number
    ).one()

    return user


def get_response(response_obj):
    jsonpickle.set_decoder_options('simplejson', sort_keys=True, indent=4)
    res = jsonpickle.decode(response_obj.__dict__['_content'])
    if isinstance(res, json_response.Response):
        return res
    raise TypeError("Unexpected Response object type")


def get_current_time():
    timestamp = datetime.datetime.now().strftime("%d-%m-%Y_%H_%M_%S_%f")
    return timestamp
