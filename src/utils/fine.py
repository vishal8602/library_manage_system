from BO.enums import *
from datetime import date
from abc import ABC
from typing import List, Dict


class Fine:
    def __init__(self, amount) -> None:
        self.__amount = amount

    def get_amount(self):
        return self.__amount


class FineTransaction:
    def __init__(self, creation_date, amount) -> None:
        self.__creation_date = creation_date
        self.__amount = amount

    def iniitiate_transaction(self):
        pass


class CreditCardTransaction(FineTransaction):
    def __init__(self, creation_date, amount, name_on_card) -> None:
        super().__init__(creation_date, amount)
        self.__name_on_card = name_on_card

    def iniitiate_transaction(self):
        print("transaction logic goes here")


class CheckTransaction(FineTransaction):
    def __init__(self, creation_date, amount, bank_name, check_number) -> None:
        super().__init__(creation_date, amount)
        self.__bank_name = bank_name
        self.__check_number = check_number

    def iniitiate_transaction(self):
        print("transaction logic goes here")


class CashTransaction(FineTransaction):
    def __init__(self, creation_date, amount, cash_tendered) -> None:
        super().__init__(creation_date, amount)
        self.__cash_tendered = cash_tendered

    def iniitiate_transaction(self):
        print("transaction logic goes here")
