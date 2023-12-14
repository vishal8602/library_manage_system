from sqlalchemy import Boolean, Column, Integer, String, Numeric, text
from sqlalchemy.orm import relationship
import logging
from database.database import Base, db
from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
from models.user import RegistrationForm
from database.model import User, BorrowedBook
from passlib.context import CryptContext
import logging
import sys
from fastapi import APIRouter, status

# third party library
from models.book import BookDetails
from database.model import Book, Rack, BookItem
import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel = logging.INFO
router = APIRouter()


def add_book_details(data: BookDetails, user: User):
    try:
        logger.info("Initinating add book curd")

        book_data = db.query(Book).filter(Book.ISBN == data.ISBN).all()
        if not len(book_data):
            book = Book(
                ISBN=data.ISBN,
                title=data.title,
                subject=data.subject,
                publisher=data.publisher,
                language=data.language,
                number_of_pages=data.number_of_pages,
                author=data.author,
            )
            db.add(book)
            db.commit()

        rack_data = db.query(Rack).filter(Rack.rack_number == data.rack_number).all()
        if not len(rack_data):
            rack = Rack(
                rack_number=data.rack_number,
                location_identifier=data.location_identifier,
            )
            db.add(rack)
            db.commit()

        book_item_data = (
            db.query(BookItem).filter(BookItem.barcode == data.barcode).all()
        )
        if not len(book_item_data):
            book_item = BookItem(
                barcode=data.barcode,
                book_isbn=data.ISBN,
                rack_number=data.rack_number,
                is_reference_only=data.is_reference_only,
                borrowed_date=data.borrowed_date,
                due_date=data.due_date,
                price=data.price,
                book_format=data.book_format,
                book_status=data.book_status,
                date_of_purchase=data.date_of_purchase,
                publication_date=data.publication_date,
            )
            db.add(book_item)
            db.commit()
            return (
                True,
                "New Book Added Succesfully",
                [],
                status.HTTP_201_CREATED,
            )

        return (
            True,
            "Book Already Present",
            [],
            status.HTTP_200_OK,
        )

    except Exception as e:
        exc_type, _, exc_tb = sys.exc_info()
        error = str(exc_type) + str(exc_tb.tb_lineno) + str(e)
        logger.error(error)
        return False, error, [], status.HTTP_417_EXPECTATION_FAILED


def get_book_details(request, page_no: int, page_size: int, user: User):
    try:
        logger.info("Initinating get book curd")
        offset = (page_no - 1) * page_size
        query = text(
            f"select * from book inner join book_item on book.ISBN=book_item.book_isbn limit {page_size} offset {offset} "
        )

        result = db.execute(query)
        result = pd.DataFrame(result).astype(str)
        result = result.to_dict(orient="records")

        query = text(
            f"select count(*) as total_size from book inner join book_item on book.ISBN=book_item.book_isbn  "
        )
        total_pages = pd.DataFrame(db.execute(query))["total_size"][0] // page_size
        return (
            True,
            "Books fetch succesfully",
            {
                "data": result,
                "total_pages": str(total_pages),
                "links": {
                    "next": f"{str(request.url).split('?')[0]}?page_no={page_no+1}&page_size={page_size}"
                    if page_no < total_pages
                    else None,
                    "previous": f"{str(request.url).split('?')[0]}?page_no={page_no-1}&page_size={page_size}"
                    if page_no > 1
                    else None,
                },
            },
            status.HTTP_200_OK,
        )

    except Exception as e:
        exc_type, _, exc_tb = sys.exc_info()
        error = str(exc_type) + str(exc_tb.tb_lineno) + str(e)
        logger.error(error)
        return False, error, [], status.HTTP_417_EXPECTATION_FAILED


def delete_book_details(book_barcode: str, user: User):
    try:
        logger.info("Initinating delete book curd")
        query = f"delete from book_item where barcode={book_barcode}"
        db.execute(query)
        db.commit()
        return (
            True,
            "Book deleted succesfully",
            [],
            status.HTTP_200_OK,
        )

    except Exception as e:
        exc_type, _, exc_tb = sys.exc_info()
        error = str(exc_type) + str(exc_tb.tb_lineno) + str(e)
        logger.error(error)
        return False, error, [], status.HTTP_417_EXPECTATION_FAILED


def issue_book_details(book_barcode: str, user_id: int, user_name: str, user: User):
    try:
        logger.info("Initiating issue book curd")
        query = f"select * from book_item where barcode={book_barcode}"
        result = db.execute(query)
        if result and result.is_reference_only:
            return True, " Reference book can't issue ", [], status.HTTP_200_OK
        if result and result.book_status != "Available":
            return (
                True,
                " Book Not available ",
                {"book status": result.status},
                status.HTTP_200_OK,
            )
        if result:
            data = BorrowedBook(user_id=user_id, book_item_barcode=book_barcode)
            db.add(data)
            db.query(BookItem).filter(BookItem.barcode == book_barcode).update(
                {BookItem.book_status: "Borrowed"}
            )
            db.commit()


        return (
            True,
            "Book deleted succesfully",
            [],
            status.HTTP_200_OK,
        )

    except Exception as e:
        exc_type, _, exc_tb = sys.exc_info()
        error = str(exc_type) + str(exc_tb.tb_lineno) + str(e)
        logger.error(error)
        return False, error, [], status.HTTP_417_EXPECTATION_FAILED
