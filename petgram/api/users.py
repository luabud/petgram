from petgram.api import crud
from petgram.api import models
from fastapi import Depends
from fastapi import APIRouter, HTTPException
from .. import db
from . import crud
from datetime import timedelta
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.security import OAuth2PasswordRequestForm
import hashlib

router = APIRouter()

session = db.SessionLocal()


def validate_credential(user, password):
    if not user:
        raise InvalidCredentialsException
    elif (
        hashlib.sha256(bytearray(password, "utf8")).hexdigest().upper()
        != user.hashed_password.upper()
    ):
        raise InvalidCredentialsException


@router.post("/auth/token")
def login(data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password

    user = crud.load_user(session, username)

    validate_credential(user, password)
    access_token = crud.manager.create_access_token(
        data=dict(sub=username), expires=timedelta(hours=6)
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/signup", status_code=201)
async def create_user():
    pass