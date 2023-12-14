from datetime import date
from BO.enums import *
from BO.datatypes import *


class BarcodeReader:
    def __init__(self, id: int, register_at: date, active: bool) -> None:
        self.__id = id
        self.__register_at = register_at
        self.__active = active

    def is_active(self):
        return self.__active

    @staticmethod
    def barcode_genrator():
        print("define something that will genrate unique barcode everytime")
        return "barcode"
