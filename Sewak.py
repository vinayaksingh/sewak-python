from bottle import route, run, post, put, get, request, Bottle

from api.utils import get_server_config
from models.db_helper import DbHelper
import jsonpickle

# initialize Sewak app.
app = Bottle(__name__)

#                                                 <-    ROUTE Requests     ->

@app.route('/')
def index():
    return "Nothing @app. root."


@app.route('/sewak')
def index():
    return "SEWAK'S FIRST api CALL !!"


#                                                 <-    POST Requests      ->  # New data to be added

@app.post('/api/categories/<category_name>')
def add_category(category_name):
    """
    POST request to add Category. This request should be triggered from Admin. 
    :param category_name: String name to be added in database
    :return: bottle.HTTPResponse 
    """
    return DbHelper().add_category(jsonpickle.decode(request.json), category_name)


@app.post('/api/services/<service_name>')
def add_service(service_name):
    """
    POST request to add Service. This request should be triggered from Admin.
    :param service_name: String service name 
    :return: bottle.HTTPResponse 
    """
    return DbHelper().add_service(jsonpickle.decode(request.json), service_name)


@app.post('/api/complains')
def add_complain():
    """
    POST request to add a new Complain.
    This should be triggered from end-user. The Complain information is part of the json in request.
    :return: bottle.HTTPResponse 
    """
    return DbHelper().add_complain(jsonpickle.decode(request.json))


#                                                 <-    GET Requests      ->  # Get existing data

@app.get('/api/categories')
def get_all_categories():
    """
    GET request returns all Categories in the database. 
    :return: bottle.HTTPResponse 
    """
    return DbHelper().get_all_categories(jsonpickle.decode(request.json))


@app.get('/api/services')
def get_all_services():
    """
    GET request returns all Services in the database.
    :return: bottle.HTTPResponse 
    """
    return DbHelper().get_all_services(jsonpickle.decode(request.json))


@app.get('/api/complain/<user_id>')
def get_complains_for_user(user_id):
    """
    GET request returns all Complains for that particular user.
    :param user_id: Integer 
    :return: bottle.HTTPResponse 
    """
    return DbHelper().get_complains_for_user(jsonpickle.decode(request.json), user_id)


@app.get('/api/user')
def get_user():
    """
    GET request returns if user already exists in database.
    :return: bottle.HTTPResponse 
    """
    return DbHelper().is_user_exists(jsonpickle.decode(request.json))


@app.get('/api/getotp')
def get_otp():
    """
    GET request for generating OTP from server.
    :return: bottle.HTTPResponse
    """
    return DbHelper().get_otp_for_new_user(jsonpickle.decode(request.json))


#                                                 <-    PUT Requests      ->  # Update existing data

@app.put('/api/complain/<complain_id>')
def update_complain(complain_id):
    """
    PUT request to update existing Complain.
    This can only be done via Admin.
    :param complain_id: Integer ID 
    :return: bottle.HTTPResponse
    """
    return DbHelper().update_complain(jsonpickle.decode(request.json), complain_id)


@app.put('/api/user/<user_id>')
def update_user(user_id):
    """
    PUT request to update User information. 
    This can also be done via App. 
    :param user_id: Integer 
    :return: bottle.HTTPResponse
    """
    return DbHelper().update_user(jsonpickle.decode(request.json), user_id)


@app.put('/api/otp/<otp>')
def verify_otp_and_add_user(otp):
    """
    PUT request with OTP sent from App for verification.
    :param otp: String 
    :return: bottle.HTTPResponse
    """
    return DbHelper().verify_otp_and_create_user(jsonpickle.decode(request.json), otp)


if __name__ == '__main__':
    """
    initialize database and start the Sewak App.
    """
    # initialize sql connection and setup DbHelper
    DbHelper().init_db()
    # Run server at localhost via bottle.
    run(app, host=get_server_config()['server_ip'], port=get_server_config()['server_port'])
