from abc import ABC
from datetime import date
from BO.enums import *


class Author:
    def __init__(self, name: str, description: str) -> None:
        self.__name = name
        self.__description = description

    def get_name(self):
        return self.__name


class Book:
    def __init__(
        self,
        ISBN: str,
        title: str,
        subject: str,
        publisher: str,
        language: str,
        number_of_pages: int,
        author: str,
    ) -> None:
        self.__ISBN = ISBN
        self.__title = title
        self.__subject = subject
        self.__publisher = publisher
        self.__langauge = language
        self.__number_of_pages = number_of_pages
        self.__author = author

    def get_title(self):
        return self.__title

    def get_author(self):
        return self.__author

    def get_subject(self):
        return self.__subject

    def get_id(self):
        return self.__ISBN


class Rack:
    def __init__(self, rack_number: int, location_identifier: str) -> None:
        self.__rack_number = rack_number
        self.__location_identifier = location_identifier


class BookItem:
    def __init__(
        self,
        book: Book,
        rack: Rack,
        barcode: str,
        is_reference_only: bool,
        borrowed_date: date,
        due_date: date,
        price: float,
        book_format,
        book_status,
        date_of_purchase: date,
        publication_date: date,
    ) -> None:
        self.__book = book
        self.__rack = rack
        self.__barcode = barcode
        self.__is_reference_only = is_reference_only
        self.__borrowed_date = borrowed_date
        self.__due_date = due_date
        self.__price = price
        self.__format = book_format
        self.__status = book_status
        self.__date_of_purchase = date_of_purchase
        self.__publication_date = publication_date

    def get_book(self):
        return self.__book

    def get_publication_date(self):
        return self.__publication_date


class BookReservation:
    def __init__(self, creation_date: str, status=ReservationStatus.COMPLETED) -> None:
        self.__creation_date = creation_date
        self.__status = status

    def get_status(self):
        return self.__status

    def fetch_reservation_details(self):
        pass

    def reserve_book(self, barcode):
        book = 'get book from db reserve collection with given barcode if present can"t reserve '
        if book is not None:
            "update reserve db to reserver for given barcode"
            return ReservationStatus.COMPLETED
        return ReservationStatus.CANCELED

    def un_reserve_book(self, barcode):
        book = 'get book from db reserve collection with given barcode if present can"t reserve '
        if book is not None:
            "update reserve db to un reserver for given barcode"
        return ReservationStatus.CANCELED


class BookLending:
    def __init__(self, creation_date: str, due_date: date, return_date=date) -> None:
        self.__creation_date = creation_date
        self.__due_date = due_date
        self.__return_date = return_date

    def get_return_date(self):
        return self.__return_date

    def issue_book(self, barcode: str):
        book = "get book if prsent in library from book collection"
        if book is not None:
            "update status of book in collection"
            "remove reservation if reserved from reserve collection"
            return BookStatus.LOANED
        return BookStatus.LOST


if __name__ == "__main__":
    book = Book(
        "123456789",
        "Introduction to Python",
        "Programming",
        "Publisher",
        "English",
        300,
    )
    rack = Rack(1, "Bottom")
    # Create a book item
    book_item = BookItem(
        book,
        rack,
        barcode="B123456",
        is_reference_only=False,
        borrowed_date=date(2023, 1, 1),
        due_date=date(2023, 1, 1),
        price=29.99,
        book_format=BookFormat.HARDCOVER,
        book_status=BookStatus.AVAILIABLE,
        date_of_purchase=date(2023, 1, 1),
        publication_date=date(2022, 1, 1),
    )

    # Accessing information
    print(book.__dict__)
    print(book_item.__dict__)
