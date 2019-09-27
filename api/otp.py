from __future__ import absolute_import, division, print_function, unicode_literals

import base64
import hashlib
import hmac
from datetime import datetime
from bottle import unicode

str = unicode


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


@singleton
class OTP(object):
    """
    OTP Handler.
    https://github.com/pyotp/pyotp/blob/master/src/pyotp/otp.py
    This is decorated as a Singleton class.
    """

    OTP_TIMEOUT = 60
    DICT_KEY_TIMESTAMP = 'otp_timestamp'
    DICT_KEY_OTP = 'otp_code'
    DICT_KEY_HASH = 'hash_code'

    def __init__(self, digits=4, digest=hashlib.sha1):
        """
        :param digits: number of integers in the OTP. We are fixing it to 4.
        :type digits: int
        :param digest: digest function to use in the HMAC (expected to be sha1)
        :type digest: callable
        """
        self.__digits = digits
        self.__digest = digest
        self.__otp_holder = {}

    def get_hash_code(self, user_phone_number):
        if self.__otp_holder.get(user_phone_number, None) is not None:
            return self.__otp_holder.pop(user_phone_number)[self.DICT_KEY_HASH]
        else:
            return None

    #TODO only for testing purpose
    def get_otp_code(self, user_phone_number):
        try:
            print(self.__otp_holder)
            if self.__otp_holder.get(user_phone_number, None) is not None:
                return self.__otp_holderget.get(user_phone_number, None)[self.DICT_KEY_OTP]
        except Exception:
            print(Exception.__dict__)
            return None

    def validate_otp(self, str_otp, str_timestamp, user_phone_number):
        if self.__otp_holder.get(user_phone_number, None) is not None:
            current_timestamp = datetime.strptime(str_timestamp, '%d-%m-%Y_%H_%M_%S_%f')
            seconds_elapsed = (current_timestamp - self.__otp_holder[user_phone_number][self.DICT_KEY_TIMESTAMP]).seconds
            # print(seconds_elapsed)
            if str_otp == self.__otp_holder[user_phone_number][self.DICT_KEY_OTP] \
                    and seconds_elapsed <= self.OTP_TIMEOUT:
                return True
            # self.__clear_otp_holder()
        return False

    def __clear_otp_holder(self):
        #TODO clear useless OTPs
        for key in self.__otp_holder:
            current_timestamp = datetime.now()
            seconds_elapsed = (current_timestamp - self.__otp_holder[key][self.DICT_KEY_TIMESTAMP]).seconds
            print(seconds_elapsed)
            if seconds_elapsed > 2*self.OTP_TIMEOUT:
                self.__otp_holder.pop(key)
                # print("Clearing OTP " + str)

    def generate_otp(self, secret, phone_number, timestamp):
        """
        :param secret: secret as str from request
        :type secret: str
        :param phone_number: part of the HMAC counter value to use as the OTP input.
        :type phone_number: int
        :param timestamp part of the HMAC counter value to use as the OTP input.
        :type timestamp: str [datetime object encoded to string]
        # Usually either the counter, or the computed integer based on the Unix timestamp
        """

        # extract datetime object from the request
        datetime_object = datetime.strptime(timestamp, '%d-%m-%Y_%H_%M_%S_%f')
        import time
        int_timestamp = int(time.mktime(datetime_object.timetuple()))

        if phone_number < 0 or int_timestamp < 0:
            raise ValueError('input must be positive integer')

        hasher = hmac.new(self.__byte_secret(secret),
                          msg=self.__int_to_bytestring(phone_number) + self.__int_to_bytestring(int_timestamp),
                          digestmod=self.__digest)
        hmac_hash = bytearray(hasher.digest())
        offset = hmac_hash[-1] & 0xf
        code = ((hmac_hash[offset] & 0x7f) << 24 |
                (hmac_hash[offset + 1] & 0xff) << 16 |
                (hmac_hash[offset + 2] & 0xff) << 8 |
                (hmac_hash[offset + 3] & 0xff))
        otp_code = str(code % 10 ** self.__digits)
        while len(otp_code) < self.__digits:
            otp_code = '0' + otp_code

        hash_code = hasher.hexdigest()
        otp_timestamp = datetime.now()

        self.__otp_holder[phone_number] = {self.DICT_KEY_OTP: otp_code,
                                           self.DICT_KEY_HASH: hash_code,
                                           self.DICT_KEY_TIMESTAMP: otp_timestamp}
        # print("OTP Holder Object : " + self.__otp_holder.__str__())

        return otp_code, hash_code

    def __byte_secret(self, secret):
        """
        :param secret: secret in base32 format
        :type secret: str
        """
        # encode the string
        secret = base64.b32encode(secret.encode('utf-8'))
        missing_padding = len(secret) % 8
        if missing_padding != 0:
            secret += '=' * (8 - missing_padding)

        return base64.b32decode(secret, casefold=True)

    def __int_to_bytestring(self, i, padding=8):
        """
        Turns an integer to the OATH specified
        bytestring, which is fed to the HMAC
        along with the secret
        :param i: Integer value to be converted.
        :type i: int
        :param padding : byte padding
        :type padding : int
        """
        result = bytearray()
        while i != 0:
            result.append(i & 0xFF)
            i >>= 8
        # It's necessary to convert the final result from bytearray to bytes
        # because the hmac functions in python 2.6 and 3.3 don't work with
        # bytearray
        return bytes(bytearray(reversed(result)).rjust(padding, b'\0'))




if __name__ == '__main__':
    otp = OTP()
    import time

    t = int(time.time())
    p = 9999999999

    str_code, hash = otp.generate_otp('df55SDFFSDSf', p, t)
    print(str_code)
    print(hash)
