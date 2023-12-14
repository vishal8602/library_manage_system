from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Boolean, Column, Integer, String, Numeric, Text, DateTime
from enum import Enum
import datetime

SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:root@localhost/library_ms"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
db = SessionLocal()


# class Stock(Base):
#     __tablename__ = "stocks"

#     id = Column(Integer, primary_key=True, index=True)
#     symbol = Column(String, unique=True, index=True)
#     price = Column(Numeric(10, 2))
#     forward_pe = Column(Numeric(10, 2))
#     forward_eps = Column(Numeric(10, 2))
#     dividend_yield = Column(Numeric(10, 2))
#     ma50 = Column(Numeric(10, 2))
#     ma200 = Column(Numeric(10, 2))


# class RegistrationForm(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     email = Column(String, unique=True, index=True)


# Base.metadata.create_all(bind=engine)

# stock = Stock(
#     symbol="MSFT1",
#     price=150.0,
#     forward_pe=20.0,
#     forward_eps=7.5,
#     dividend_yield=2.0,
#     ma50=145.0,
#     ma200=140.0,
# )
# user = RegistrationForm(name="vishal patel", email="xyz_1@gmail.com")
# db.add(user)
# db.commit()

# with SessionLocal() as db:
#     users = db.query(RegistrationForm).all()
#     print(users)


from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.exc import SQLAlchemyError

# from utils.exceptions import SRCException
import logging

logger = logging.getLogger(__name__)


class SRCException(Exception):
    """Exception raised by every module in the SRC package."""

    def __init__(self, msg=None):
        """

        Args:
            msg (str): human friendly error message.
        """

        if msg is None:
            msg = "SRC Exception"
        logger.exception(msg)
        super().__init__(msg)


class SQLAlchemyVerbs(str, Enum):
    FIND = "find"
    FIND_ONE = "find_one"
    INSERT_ONE = "insert_one"
    INSERT_MANY = "insert_many"
    UPDATE_ONE = "update_one"
    UPDATE_MANY = "update_many"
    AGGREGATE = "aggregate"


def apply_sqlalchemy(session, model, verb, *args, **kwargs):
    """
    This method is used to perform database operations using SQLAlchemy.
    :param session: SQLAlchemy session
    :param model: SQLAlchemy model class
    :param verb: Verb for the operation (FIND, FIND_ONE, INSERT_ONE, INSERT_MANY, UPDATE_ONE, UPDATE_MANY)
    :param args: Positional arguments for the operation
    :param kwargs: Keyword arguments for the operation
    :return: Result of the operation
    """
    if verb not in list(map(lambda x: x.lower(), SQLAlchemyVerbs.__dict__.keys())):
        raise ValueError("SQLAlchemy Verb is not supported")

    try:
        if verb == SQLAlchemyVerbs.FIND:
            return session.query(model).filter(*args, **kwargs).all()

        elif verb == SQLAlchemyVerbs.FIND_ONE:
            try:
                result = session.query(model).filter(*args, **kwargs).one()
                return result
            except NoResultFound:
                raise SRCException(
                    f"Failed to find the record with {args} and {kwargs}"
                )
            except MultipleResultsFound:
                raise SRCException(f"Multiple records found with {args} and {kwargs}")

        elif verb == SQLAlchemyVerbs.INSERT_ONE:
            instance = model(*args, **kwargs)
            session.add(instance)
            session.commit()
            return instance.id

        elif verb == SQLAlchemyVerbs.INSERT_MANY:
            instances = [model(*arg, **kwarg) for arg, kwarg in zip(args, kwargs)]
            session.add_all(instances)
            session.commit()
            return [instance.id for instance in instances]

        elif verb == SQLAlchemyVerbs.UPDATE_ONE:
            # result = (
            #     session.query(model).filter_by(**filter_kwargs).update(update_kwargs)
            # )

            if result == 1:
                session.commit()
                return True
            raise SRCException(f"Failed to update the record with {args} and {kwargs}")

        elif verb == SQLAlchemyVerbs.UPDATE_MANY:
            result = (
                session.query(model)
                .filter(*args, **kwargs)
                .update(kwargs, synchronize_session=False)
            )
            if result > 0:
                session.commit()
                return True
            raise SRCException(f"Failed to update records with {args} and {kwargs}")

    except SQLAlchemyError as e:
        raise SRCException(str(e))


# x = apply_sqlalchemy(
#     db,
#     RegistrationForm,
#     SQLAlchemyVerbs.UPDATE_ONE,
#     RegistrationForm.name == "vishal1",
#     email="new_email@gmail.com",
# )


# x = apply_sqlalchemy(
#     db,
#     RegistrationForm,
#     SQLAlchemyVerbs.UPDATE_ONE,
#     RegistrationForm.name == "vishal1",
#     RegistrationForm.email="xyz2@gmail.com",
# )
# x = apply_sqlalchemy(
#     db,
#     RegistrationForm,
#     SQLAlchemyVerbs.INSERT_ONE,
#     name="deepesh_1",
#     email="deep_1@gmail.com",
# )
# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(255), nullable=False)
#     email = Column(String(255), unique=True, nullable=False)
#     phone = Column(String(10), unique=True, nullable=False)
#     street_address = Column(Text, nullable=False)
#     city = Column(String(255), nullable=False)
#     state = Column(String(255), nullable=False)
#     zipcode = Column(String(6), nullable=False)
#     country = Column(String(255), nullable=False)
#     password = Column(String(255), nullable=False)
#     created_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
#     updated_at = Column(
#         DateTime(timezone=True),
#         default=datetime.datetime.utcnow,
#         onupdate=datetime.datetime.utcnow,
#     )
#     is_deleted = Column(Boolean, default=False)


# Base.metadata.create_all(bind=engine)
# user = User(
#     name="11deepesh_1",
#     email="11deep_1@gmail.com",
#     phone="123",
#     street_address="",
#     city="",
#     state="",
#     zipcode="",
#     country="",
#     password="",
# )

# db.add(user)
# db.commit()
# # x = apply_sqlalchemy(db, User, SQLAlchemyVerbs.INSERT_ONE, user)
# x = apply_sqlalchemy(
#     db,
#     User,
#     SQLAlchemyVerbs.FIND,
# )
# print([(i.name, i.email) for i in x])


def insert_book():
    import requests
    import json
    import random
    import datetime

    url = "http://127.0.0.1:8000/api/v1/book/"
    for i in range(100):
        payload = json.dumps(
            {
                "ISBN": str(random.randint(1000000000, 9999999999)),
                "title": random.choice(["Love", "Life", "Death"]),
                "subject": random.choice(["Hindi", "Psychology", "History", "SciFi"]),
                "publisher": random.choice(
                    ["Penguin Books", "Oxford University Press", "HarperCollins"]
                ),
                "language": random.choice(["Hindi", "English", "Malwi"]),
                "number_of_pages": random.randint(100, 500),
                "author": random.choice(
                    ["Vishal Patel", "Deepesh Sharma", "Ajay Patel", "Ashustosh Dodiya"]
                ),
                "rack_number": random.randint(1, 100),
                "location_identifier": f"Shelf {random.randint(1, 10)}, Row {random.randint(1, 10)}",
                "barcode": str(random.randint(100000000000, 999999999999)),
                "is_reference_only": random.choice([True, False]),
                "borrowed_date": str(datetime.date.today()),
                "due_date": str(datetime.date.today() + datetime.timedelta(days=14)),
                "price": random.uniform(10.0, 50.0),
                "book_format": random.choice(["Paperback", "Hardcover", "Ebook"]),
                "book_status": random.choice(["Available", "Borrowed", "Lost"]),
                "date_of_purchase": str(datetime.date.today()),
                "publication_date": str(
                    datetime.date.today()
                    - datetime.timedelta(days=random.randint(365, 3650))
                ),
            }
        )
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoic3RyaW5nIiwiZW1haWwiOiJ1c2VyQGV4YW1wbGUuY29tIiwic3lzdGVtIjoibGlicmFyeSIsImV4cGlyZXMiOjE3MDE4NDkzNTkuMDU1MTE4fQ.Xjk9S8vB6ah8DWQ_4qsr2WkeIKez971_1j2ZDJQFgeY",
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
