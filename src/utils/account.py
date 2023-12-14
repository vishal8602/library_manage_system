from abc import ABC, abstractmethod
from BO.datatypes import *
from BO.enums import *
from datetime import date
from utils.book import BookItem, Book, BookReservation
from utils.search import Catalog
from utils.librarycard import LibraryCard
from utils.barcodeReader import BarcodeReader
import uuid
from utils.registration import AccountRegistrationManager
from utils.library import library_object


class Account(ABC):
    def __init__(
        self,
        id: int,
        password: str,
        person: Person,
        library_card: LibraryCard,
        status=AccountStatus.ACTIVE,
    ) -> None:
        super().__init__()
        self.__id = id
        self.__password = password
        self.__status = status
        self.__person = person
        self.__library_card = library_card

    @abstractmethod
    def reset_password(self, password):
        pass

    @abstractmethod
    def update_person(self, person):
        pass

    @abstractmethod
    def set_account_status(self, status):
        pass

    @abstractmethod
    def un_reserve_book(self, book_barcode: str):
        pass

    @abstractmethod
    def renew_book(self):
        pass

    @abstractmethod
    def reserve_book(self, book_barcode: str):
        pass

    @abstractmethod
    def view_account(self):
        pass

    @abstractmethod
    def return_book(self):
        pass


class Member(Account):
    def __init__(
        self,
        id: int,
        password: str,
        person: Person,
        date_of_joining: date,
        library_card: LibraryCard,
        total_number_of_books: int = 0,
        status=AccountStatus.ACTIVE,
    ) -> None:
        super().__init__(id, password, person, library_card, status)
        self.__date_of_joining = date_of_joining
        self.__total_number_of_books = total_number_of_books

    def reset_password(self, password):
        self.__password = password

    def update_person(self, person):
        self.__person = person

    def set_account_status(self, status):
        self.__status = status

    def date_of_membership(self) -> date:
        return self.__date_of_joining

    def get_total_books_checkOut(self) -> int:
        return self.__total_number_of_books

    def reserve_book(self, book_barcode: str):
        print("reserve book")

    def un_reserve_book(self, book_barcode: str):
        print("un reserve book")

    def checkout(self, book_barcode: str):
        print("Book Checkout")
        pass

    def renew_book(self, book_barcode: str):
        print("Book Renew")
        pass

    def return_book(self):
        print("Book returend")
        pass


class Librarian(Account):
    def __init__(
        self,
        id,
        password,
        person,
        library_card: LibraryCard,
        status=AccountStatus.ACTIVE,
    ) -> None:
        super().__init__(id, password, person, library_card, status)

    def reset_password(self, password):
        self.__password = password

    def update_person(self, person):
        self.__person = person

    def set_account_status(self, status):
        self.__status = status

    def block_member(self, member: Member) -> bool:
        member.set_account_status(AccountStatus.BLACKLISTED)

    def unblock_member(self, member: Member) -> bool:
        member.set_account_status(AccountStatus.ACTIVE)

    def remove_book(self, bookItem: BookItem):
        Catalog().remove_book_from_catalog(bookItem)

    def add_book_item(self, bookItem: BookItem) -> bool:
        Catalog().add_book_in_catalog(bookItem)

    def register_new_member(self, registration_info: RegistrationInfo):
        member = Member(
            AccountRegistrationManager.register_new_member(registration_info)
        )
        library_object.add_member(member)

    def reserve_book(self, book_barcode: str):
        print("reserve book")

    def un_reserve_book(self, book_barcode: str):
        print("un reserve book")

    def checkout(self, book_barcode: str):
        print("Book Checkout")
        pass

    def renew_book(self, book_barcode: str):
        print("Book Renew")
        pass

    def return_book(self):
        print("Book returend")
        pass


# Example Usage
if __name__ == "__main__":
    # user
    address = Address("Vijay Nagar", "Dewas", "MP", "455116", "India")
    member_person = Person("Vishal Patel", address, "xyz@example.com", "1234567890")
    member_card = LibraryCard("M123", "M_BARCODE", date.today())
    member = Member(1, "password123", member_person, date.today(), member_card)

    #  librarian
    librarian_person = Person(
        "Librarian", address, "librarian@example.com", "9876543210"
    )
    librarian_card = LibraryCard("L456", "L_BARCODE", date.today())
    librarian = Librarian(2, "librarianpass", librarian_person, librarian_card)

    # Interaction
    librarian.block_member(member)
    librarian.unblock_member(member)

    # register new member by libraninan
    registration_info = RegistrationInfo(
        "Deepesh",
        "deepass@gmail.com",
        "0000123456",
        "Near MG Road",
        "Jaipur",
        "RJ",
        "567009",
        "India",
    )
    librarian.register_new_member(registration_info)
