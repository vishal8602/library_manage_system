from enum import Enum


class BookFormat(Enum):
    HARDCOVER = 1
    PAPERBACK = 2
    AUDIOBOOK = 3
    EBOOK = 4
    NEWSPAPER = 5
    MAGAZINE = 6
    JOURNAL = 7


class BookStatus(Enum):
    AVAILIABLE = 1
    RESERVED = 2
    LOANED = 3
    LOST = 4


class ReservationStatus(Enum):
    WAITING = 1
    PENDING = 2
    COMPLETED = 3
    CANCELED = 4
    NONE = None


class AccountStatus(Enum):
    ACTIVE = 1
    CLOSED = 2
    CANCELED = 3
    BLACKLISTED = 4
    NONE = None
