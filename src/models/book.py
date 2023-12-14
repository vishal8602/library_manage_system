# Standard Library
from uuid import UUID, uuid4
import re

# Third Party Library
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import date


class BookDetails(BaseModel):
    ISBN: str = Field(...)
    title: str = Field(...)
    subject: str = Field(...)
    publisher: str = Field(...)
    language: str = Field(...)
    number_of_pages: int = Field(...)
    author: str = Field(...)
    rack_number: int = Field(...)
    location_identifier: str = Field(...)
    barcode: str = Field(...)
    is_reference_only: bool = Field(...)
    borrowed_date: date
    due_date: date
    price: float = Field(...)
    book_format: str = Field(...)
    book_status: str = Field(...)
    date_of_purchase: date
    publication_date: date
