from sqlalchemy import Boolean, Column, Integer, String, Numeric
from sqlalchemy.orm import relationship
import logging
from database.database import Base, db
from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
from models.user import RegistrationForm
from database.model import User
from passlib.context import CryptContext
import sys

logger = logging.getLogger(__name__)
logger.setLevel = logging.INFO


def getHashedPassword(password: str) -> str:
    pwd = CryptContext(schemes=["bcrypt"])
    return pwd.hash(password)


def register_data(data: RegistrationForm):
    try:
        logger.info("Initaiting register crud user " + data.email)
        data.password = getHashedPassword(data.password)
        result = db.query(User).filter(User.email == data.email).all()

        if (len(result)) != 0:
            return (
                False,
                "The email address is already registered use login",
                [],
                status.HTTP_412_PRECONDITION_FAILED,
            )
        data = User(**data.model_dump())
        db.add(data)
        db.commit()
        return (
            True,
            "Registered Successfully",
            [],
            status.HTTP_201_CREATED,
        )

    except Exception as e:
        exc_type, _, exc_tb = sys.exc_info()
        error = str(exc_type) + str(exc_tb.tb_lineno) + str(e)
        logger.error(error)
        return False, error, [], status.HTTP_417_EXPECTATION_FAILED


def update_data(data: dict, user: User):
    try:
        logger.info("Initaiting register crud user " + user.email)
        if data.get("password", ""):
            data["password"] = getHashedPassword(data.password)

        db.query(User).filter(User.email == user.email).update(data)
        db.commit()
        return (
            True,
            "Updated Successfully",
            [],
            status.HTTP_201_CREATED,
        )

    except Exception as e:
        exc_type, _, exc_tb = sys.exc_info()
        error = str(exc_type) + str(exc_tb.tb_lineno) + str(e)
        logger.error(error)
        return False, error, [], status.HTTP_417_EXPECTATION_FAILED
