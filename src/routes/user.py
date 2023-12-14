from fastapi import APIRouter, status, HTTPException, Depends, requests
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
import logging
import json
import sys

# Project Library
from models.user import RegistrationForm, UserCredential
from cruds.user import register_data, update_data
from database.model import User
from database.database import db
from Auth.auth import generate_token, get_current_user

logger = logging.getLogger(__name__)
logger.setLevel = logging.INFO
router = APIRouter()


@router.post(
    "/register",
    summary="Register Yourself",
    description="Register here to explore the API",
    response_description="Registered Successfully",
    status_code=status.HTTP_201_CREATED,
)
def register(data: RegistrationForm):
    try:
        logger.info("Initaiting register user " + data.email)
        api_status, message, response, status_code = register_data(data)
        return JSONResponse(
            status_code=status_code,
            content={"status": api_status, "data": response, "message": message},
        )
    except Exception as e:
        exc_type, _, exc_tb = sys.exc_info()
        error = str(exc_type) + str(exc_tb.tb_lineno) + str(e)
        logger.error(error)
        return JSONResponse(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            content={"status": False, "data": [], "message": error},
        )


@router.post(
    "/login",
    summary="Login To get the Access Token",
    description="Provide the Registered Email and Password to login to get the Access Token.",
    response_description="Access Token Generated",
    status_code=status.HTTP_200_OK,
)
def login(user: OAuth2PasswordRequestForm = Depends()):
    try:
        user.email = user.username
        logger.info("Initaiting login " + user.email)
        api_status, message, response, status_code = generate_token(user)
        return JSONResponse(
            status_code=status_code,
            content={"status": api_status, "data": response, "message": message},
        )
    except Exception as e:
        exc_type, _, exc_tb = sys.exc_info()
        error = str(exc_type) + str(exc_tb.tb_lineno) + str(e)
        logger.error(error)
        return JSONResponse(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            content={"status": False, "data": [], "message": error},
        )


@router.get(
    "/get_user",
    summary="TO get user info",
    description="Access Token requires",
    response_description="User Info ",
    status_code=status.HTTP_200_OK,
)
def get_user(user=Depends(get_current_user)):
    try:
        logger.info("Initaiting get user " + user.email)
        api_status, message, response, status_code = (
            True,
            "User Data",
            user.as_dict(),
            status.HTTP_200_OK,
        )
        return ({"status": api_status, "data": response, "message": message},)

    except Exception as e:
        exc_type, _, exc_tb = sys.exc_info()
        error = str(exc_type) + str(exc_tb.tb_lineno) + str(e)
        logger.error(error)
        return JSONResponse(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            content={"status": False, "data": [], "message": error},
        )


@router.post(
    "/update_user",
    summary="TO get user info",
    description="Access Token requires",
    response_description="User Info ",
    status_code=status.HTTP_200_OK,
)
def update_user(new_data: dict, user=Depends(get_current_user)):
    try:
        logger.info("Initaiting get user " + user.email)
        api_status, message, response, status_code = update_data(new_data, user)
        return ({"status": api_status, "data": response, "message": message},)

    except Exception as e:
        exc_type, _, exc_tb = sys.exc_info()
        error = str(exc_type) + str(exc_tb.tb_lineno) + str(e)
        logger.error(error)
        return JSONResponse(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            content={"status": False, "data": [], "message": error},
        )
