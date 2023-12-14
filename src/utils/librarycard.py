from datetime import date
from BO.enums import *
from BO.datatypes import *


class LibraryCard:
    def __init__(
        self,
        card_number: int,
        barcode: str,
        issue_date: date,
        active=AccountStatus.ACTIVE,
    ) -> None:
        self.__card_number = card_number
        self.__barcode = barcode
        self.__issue_date = issue_date
        self.__active = active

    def is_active(self, card_number) -> bool:
        return self.__active

    @staticmethod
    def genrate_card_number():
        return "fetch latest enrty from db increment the card number and return it "
