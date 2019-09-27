class Request(object):
    def __init__(self, timestamp, user=None, category=None, service=None, complain=None):
        self.timestamp = timestamp
        self.user = user
        self.category = category
        self.service = service
        self.complain = complain

    @staticmethod
    def get_request_json(obj):
        """
        Create a pickled json object
        :param obj: Request object to be pickled.
        :return: Encoded pickled string. 
        """
        if isinstance(obj, Request):
            import jsonpickle
            return jsonpickle.encode(obj, unpicklable=True)
        raise TypeError


if __name__ == '__main__':

    from api.json.json_model import Auth, Category, Service, Complain
    authObj = Auth(auth_code = 'ccf6cebd53549f1d74a82bb455d907648fa28d0c',
                   phone_number = 9780044091,
                   serial_number = 'JLIU897978F',
                   name = None,
                   email = None)
    categoryObj = Category(category_id = 5467)
    serviceObj = Service(service_id=1234)
    complainObj = Complain(address = 'A-98',
                           message = 'Repair my arse',
                           service_status = '0',
                           timestamp = '98276998983',
                           complain_phone_number = None)
    import datetime
    timestamp = datetime.datetime.now().strftime("%d-%m-%Y_%H_%M_%S_%f")
    RequestObj = Request(timestamp=timestamp, auth=authObj, category=categoryObj, service=serviceObj, complain=complainObj)
    print(Request.get_request_json(RequestObj))