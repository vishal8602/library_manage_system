from enum import *
from datetime import date
from abc import ABC, abstractmethod
from typing import List, Dict
from utils.book import BookItem, Book, Rack
from BO.enums import *
import threading


class Search(ABC):
    """Interface for search may be in fuature we swift to elastic search or ml search"""

    @abstractmethod
    def search_by_title(self, title: str) -> List[str]:
        pass

    @abstractmethod
    def search_by_author(self, author: str) -> List[str]:
        pass

    @abstractmethod
    def search_by_subject(self, subject: str) -> List[str]:
        pass

    @abstractmethod
    def search_by_publication_date(self, date: date) -> List[str]:
        pass

    @abstractmethod
    def add_book_in_catalog(cls, book_item: BookItem) -> None:
        pass

    @abstractmethod
    def remove_book_from_catalog(cls, book_item: BookItem) -> None:
        pass


class Catalog(Search):
    """Implemented as a singleton class by using lock so it would be thread safe"""

    __instanse = None
    __lock = threading.Lock()

    def __new__(cls) -> "Catalog":
        with cls.__lock:
            if cls.__instanse is None:
                cls.__instanse = super().__new__(cls)
                cls.__instanse.__total_books = 0
                cls.__instanse.__book_titles: Dict[str, List[str]] = {}
                cls.__instanse.__book_author: Dict[str, List[str]] = {}
                cls.__instanse.__book_subject: Dict[str, List[str]] = {}
                cls.__instanse.__book_publication_date: Dict[date, List[str]] = {}
            return cls.__instanse

    @classmethod
    def add_book_in_catalog(cls, book_item: BookItem) -> None:
        book = book_item.get_book()
        title = book.get_title()
        author = book.get_author()
        subject = book.get_subject()
        publication_date = book_item.get_publication_date()
        book_id = book.get_id()
        cls.__instanse.__book_titles.setdefault(title, []).append(book_id)
        cls.__instanse.__book_author.setdefault(author, []).append(book_id)
        cls.__instanse.__book_subject.setdefault(subject, []).append(book_id)
        cls.__instanse.__book_publication_date.setdefault(publication_date, []).append(
            book_id
        )
        cls.__instanse.__total_books += 1

    @classmethod
    def remove_book_from_catalog(cls, book_item: BookItem) -> None:
        book = book_item.get_book()
        title = book.get_title()
        author = book.get_author()
        subject = book.get_subject()
        publication_date = book_item.get_publication_date()
        book_id = book.get_id()

        cls.__instanse.__book_titles[title].remove(book_id)
        cls.__instanse.__book_author[author].remove(book_id)
        cls.__instanse.__book_subject[subject].remove(book_id)
        cls.__instanse.__book_publication_date[publication_date].remove(book_id)
        cls.__instanse.__total_books -= 1

    @classmethod
    def search_by_title(cls, title: str) -> List[str]:
        return cls.__instanse.__book_titles.get(title, [])

    @classmethod
    def search_by_author(cls, author: str) -> List[str]:
        return cls.__instanse.__book_author.get(author, [])

    @classmethod
    def search_by_subject(cls, subject: str) -> List[str]:
        return cls.__instanse.__book_subject.get(subject, [])

    @classmethod
    def search_by_publication_date(cls, date: date) -> List[str]:
        return cls.__instanse.__book_publication_date.get(date, [])


if __name__ == "__main__":
    book = Book(
        "123456789",
        "Introduction to Python",
        "Programming",
        "Publisher",
        "English",
        300,
        "Vishal Patel",
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
    Catalog().add_book_in_catalog(book_item)
    book = Book(
        "12345678910",
        "Introduction to C++",
        "Programming",
        "Publisher Vishal",
        "English",
        300,
        "Vishal Patel",
    )
    rack = Rack(1, "Bottom")
    # Create a book item
    book_item = BookItem(
        book,
        rack,
        barcode="B123454",
        is_reference_only=False,
        borrowed_date=date(2023, 1, 1),
        due_date=date(2023, 1, 1),
        price=29.99,
        book_format=BookFormat.HARDCOVER,
        book_status=BookStatus.AVAILIABLE,
        date_of_purchase=date(2023, 1, 1),
        publication_date=date(2022, 1, 1),
    )
    Catalog().add_book_in_catalog(book_item)
    print(Catalog().search_by_title("Introduction to C++"))
    Catalog().remove_book_from_catalog(book_item)
    print(Catalog().search_by_title("Introduction to C++"))
