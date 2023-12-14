from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from config import SECRET_KEY, ALGORITHM
from database.database import db
from database.model import User
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")


def generate_token(user, expires_delta: Optional[timedelta] = timedelta(minutes=15)):
    db_user = db.query(User).filter(User.email == user.email).one()
    if not db_user:
        return False, "User Not Registered", [], status.HTTP_401_UNAUTHORIZED
    if not CryptContext(schemes=["bcrypt"]).verify(user.password, db_user.password):
        return False, "Invalid Credential", [], status.HTTP_401_UNAUTHORIZED
    now = datetime.utcnow()
    expires = now + expires_delta
    token_data = {
        "name": db_user.name,
        "email": db_user.email,
        "system": "library",
        "expires": expires.timestamp(),
    }
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return (
        True,
        "token genrated succesfully",
        {"access_token": token, "token_type": "bearer"},
        status.HTTP_200_OK,
    )


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        if email is None:
            raise credentials_exception

    except Exception as e:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).one()
    return user
