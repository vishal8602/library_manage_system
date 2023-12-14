from sqlalchemy import *
from sqlalchemy.orm import relationship
from database.database import Base, engine
import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(10), unique=True, nullable=False)
    street_address = Column(Text, nullable=False)
    city = Column(String(255), nullable=False)
    state = Column(String(255), nullable=False)
    zipcode = Column(String(6), nullable=False)
    country = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )
    is_deleted = Column(Boolean, default=False)
    role = Column(String(6), nullable=False)

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class Book(Base):
    __tablename__ = "book"

    ISBN = Column(String(255), primary_key=True)
    title = Column(String(255))
    subject = Column(String(255))
    publisher = Column(String(255))
    language = Column(String(255))
    number_of_pages = Column(Integer)
    author = Column(String(255))


class Rack(Base):
    __tablename__ = "rack"

    rack_number = Column(Integer, primary_key=True)
    location_identifier = Column(String(255))


class BookItem(Base):
    __tablename__ = "book_item"

    barcode = Column(String(255), primary_key=True)
    book_isbn = Column(String(255), ForeignKey("book.ISBN"))
    rack_number = Column(Integer, ForeignKey("rack.rack_number"))
    is_reference_only = Column(Boolean)
    borrowed_date = Column(Date)
    due_date = Column(Date)
    price = Column(Float)
    book_format = Column(String(255))
    book_status = Column(String(255))
    date_of_purchase = Column(Date)
    publication_date = Column(Date)


class BorrowedBook(Base):
    __tablename__ = "borrowed_book"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_item_barcode = Column(
        String(255), ForeignKey("book_item.barcode"), nullable=False
    )


Base.metadata.create_all(bind=engine)
