from abc import ABC
from dataclasses import dataclass


class Address:
    def __init__(
        self, streetAddress: str, city: str, state: str, zipcode: str, country: str
    ):
        self.__streetAddress = streetAddress
        self.__city = city
        self.__state = state
        self.__zipcode = zipcode
        self.__country = country


class Person(ABC):
    def __init__(self, name: str, address: Address, email: str, phone: str):
        self.__name = name
        self.__address = address
        self.__email = email
        self.__phone = phone


class constants:
    def __init__(self):
        self.MAX_BOOKS_ISSUED_TO_A_USER = 5
        self.MAX_LENDING_DAYS = 10


@dataclass
class RegistrationInfo:
    name: str
    email: str
    phone: str
    street_address: str
    city: str
    state: str
    zipcode: str
    country: str
