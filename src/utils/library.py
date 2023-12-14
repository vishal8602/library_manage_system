from utils.book import BookItem
from utils.account import Account


class library:
    def __init__(self) -> None:
        self.books = []
        self.members = []

    def add_book(self, book_item: BookItem):
        self.books.append(book_item)

    def remove_book(self, book_item: BookItem):
        self.books.remove(book_item)

    def add_member(self, member: Account):
        self.members.append(member)

    def rmove_member(self, member: Account):
        self.members.remove(member)


library_object = library()
