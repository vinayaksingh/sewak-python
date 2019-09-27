from sqlalchemy import Integer, Column, String, func, DateTime, SmallInteger, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def create_model(engine):
    Base.metadata.create_all(engine)


class User(Base):

    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    phone_number = Column(String(10), primary_key=True)
    handset_serial_number = Column(String(20), primary_key=True)
    auth_code = Column(String(160), unique=True)
    name = Column(String(128), nullable=True)
    email = Column(String(128), nullable=True)
    dirty_bit = Column(Boolean, nullable=False)

    def __init__(self, phone_number, handset_serial_number, auth_code, timestamp=None, name=None, email=None, dirty_bit=False):
        self.phone_number = phone_number
        self.handset_serial_number = handset_serial_number
        self.auth_code = auth_code
        self.timestamp = timestamp
        self.name = name
        self.email = email
        self.dirty_bit = dirty_bit


class Category(Base):

    __tablename__ = 'category'

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(128), primary_key=True, unique=True)

    def __init__(self, category_name):
        self.category_name = category_name


class Service(Base):

    __tablename__ = 'service'

    service_id = Column(Integer, primary_key=True, autoincrement=True)
    service_name = Column(String(128), primary_key=True, unique=True)

    def __init__(self, service_name):

        self.service_name = service_name


class Complain(Base):

    __tablename__ = 'complain'

    complain_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.user_id), nullable=False)
    category_id = Column(Integer, ForeignKey(Category.category_id), nullable=False)
    service_id = Column(Integer, ForeignKey(Service.service_id), nullable=False)
    address = Column(String(100))
    message = Column(String(256))
    timestamp = Column(DateTime(timezone=True), default=func.now())
    service_status = Column(SmallInteger)
    complain_phone_number = Column(String(10))

    def __init__(self, user_id, category_id, service_id, address, message,
                 service_status, complain_phone_number):

        self.user_id = user_id
        self.category_id = category_id
        self.service_id = service_id
        self.address = address
        self.message = message
        self.service_status = service_status
        self.complain_phone_number = complain_phone_number



