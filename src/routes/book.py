from fastapi import APIRouter, status, HTTPException, Depends, Form, Request, Query
from fastapi.responses import JSONResponse
import logging
from Auth.auth import get_current_user
import sys

# third party library
from models.book import BookDetails
from cruds.book import (
    add_book_details,
    get_book_details,
    delete_book_details,
    issue_book_details,
)

logger = logging.getLogger(__name__)
logger.setLevel = logging.INFO
router = APIRouter()


@router.post(
    "/",
    summary="TO add book in library",
    description="Access Token requires",
    response_description="List[Books] ",
    status_code=status.HTTP_200_OK,
)
def add_book(details: BookDetails, user=Depends(get_current_user)):
    try:
        logger.info("Initaiting get user " + user.email)
        api_status, message, response, status_code = add_book_details(details, user)
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
    "/",
    summary="TO get book in library",
    description="Access Token requires",
    response_description="List[Books] ",
    status_code=status.HTTP_200_OK,
)
def get_book(
    request: Request,
    page_no: int = Query(1),
    page_size: int = Query(10),
    user=Depends(get_current_user),
):
    try:
        logger.info("Initaiting get user " + user.email)
        api_status, message, response, status_code = get_book_details(
            request, page_no, page_size, user
        )

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


@router.delete(
    "/{book_barcode}",
    summary="TO delete book in library",
    description="Access Token requires",
    status_code=status.HTTP_202_ACCEPTED,
)
def delete_book(
    book_barcode: str,
    user=Depends(get_current_user),
):
    try:
        logger.info("Initaiting get user " + user.email)
        api_status, message, response, status_code = delete_book_details(
            book_barcode, user
        )

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
    "/issue",
    summary="TO issue book from library",
    description="Access Token requires",
    status_code=status.HTTP_202_ACCEPTED,
)
def issue_book(
    book_barcode: str,
    user_id: int,
    user_name: str,
    user=Depends(get_current_user),
):
    try:
        logger.info("Initaiting get user " + user.email)
        api_status, message, response, status_code = issue_book_details(
            book_barcode, user_id, user_name, user
        )
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
