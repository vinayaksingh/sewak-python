import threading


def read_config(config_file):
    """
    This function returns a dictionary that has the
    constants contained in the config_file.json
    :param config_file: The file that contains the config
    :return: json dictionary
    """

    import json
    import os

    config_file_path = os.path.join(os.path.dirname(__file__)[0:-len("api")], 'config/' + config_file + '.json')

    with open(config_file_path, 'r') as file:
        data = json.load(file)
    file.close()

    return data


def create_sqlalchemy_engine():
    """
    Creates SQL engine and return 
    
    :return: engine
    """

    from sqlalchemy import create_engine

    config_data = read_config('db_config')
    server_ip = config_data["db_server_ip"]
    server_port = config_data["db_server_port"]
    database_name = config_data["db_name"]
    username = config_data["username"]
    password = config_data["password"]

    connection_string = "mysql+pymysql://" + username + ":" + password + "@" + \
                        server_ip + ":" + server_port + "/" + database_name

    engine = create_engine(connection_string, echo_pool=False)

    return engine


def send_otp_message(otp, phone_number):
    """
    Handles sending of OTP SMS to the phone number provided. 
    :param otp: String value provided by OTP Class
    :param phone_number: int phone number for SMS to be sent
    :return: Boolean True for success otherwise False
    """

    thread = threading.Thread(target=__spawn_twilio__, args=(otp, phone_number))
    thread.daemon = True
    thread.start()


def __spawn_twilio__(otp, phone_number):
    # https://www.twilio.com/docs/libraries/python
    from twilio.rest import Client

    # TODO manage secret information.
    # Your Account SID from twilio.com/console
    account_sid = ""
    # Your Auth Token from twilio.com/console
    auth_token = ""

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to="+91" + str(phone_number),
        from_="+14159697091",
        body="\nHello from Sewak!\n" + "Your OTP: " + otp)

    #print(message.sid)


def get_server_config():
    return read_config('server_config')


#TODO add email validations