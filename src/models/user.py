# Standard Library
from uuid import UUID, uuid4
import re

# Third Party Library
from pydantic import BaseModel, EmailStr, Field, validator


class UserCredential(BaseModel):
    password: str = Field(
        ...,
        example="Minimum 8 letters, 1 number, 1 capital letter and a special character.",
        min_length=8,
    )
    email: EmailStr = Field(..., example="user@example.com")


class RegistrationForm(UserCredential):
    name: str
    phone: str = Field(
        pattern=r"^\d{10}$", min_length=10, max_length=10, examples=[1234567890]
    )
    street_address: str
    city: str
    state: str
    zipcode: str = Field(min_length=6, max_length=6, examples=[455116])
    country: str
    password: str = Field(
        ...,
        example="Minimum 8 letters, 1 number, 1 capital letter and a special character.",
        min_length=8,
    )
    role: str = Field(...)

    @validator("password")
    def validate_password(cls, v):
        if not re.search("[a-zA-Z]", v):
            raise ValueError("Password must contain at least one letter")

        if not re.search("[0-9]", v):
            raise ValueError("Password must contain at least one digit")

        if not re.search("[!@#$%^&*()_+=-]", v):
            raise ValueError("Password must contain at least one special character")

        return v
