from enum import *
from datetime import date
from abc import ABC
from typing import List, Dict, email
from BO.enums import *
from BO.datatypes import *


class Notification(ABC):
    def __init__(self, notification_id: int, created_on: date, content: str) -> None:
        super().__init__()
        self.__notification_id = notification_id
        self.__created_on = created_on
        self.__content = content

    def send_notification():
        pass


class PostalNotification(Notification):
    def __init__(
        self, notification_id: int, created_on: date, content: str, address: Address
    ) -> None:
        super().__init__(notification_id, created_on, content)
        self.__address = address

    def send_notification():
        pass


class EmailNotification(Notification):
    def __init__(
        self, notification_id: int, created_on: date, content: str, email: email
    ) -> None:
        super().__init__(notification_id, created_on, content)
        self.__email = email

    def send_notification():
        pass
