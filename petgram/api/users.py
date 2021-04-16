from os import access
from starlette.responses import RedirectResponse, Response
from petgram.api import crud
from petgram.api.models import User
from fastapi import Depends, status, Request
from fastapi import APIRouter, HTTPException

from . import crud
from datetime import timedelta
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.security import OAuth2PasswordRequestForm
import hashlib
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="frontend/templates")

router = APIRouter()


access_token = "not set"


def validate_credential(user, password):
    if not user:
        raise InvalidCredentialsException
    elif (
        hashlib.sha256(bytearray(password, "utf8")).hexdigest().upper()
        != user.hashed_password.upper()
    ):
        raise InvalidCredentialsException


@router.post("/auth/token")
def login(response: Response, data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password

    potential_user = crud.load_user(username)

    validate_credential(potential_user, password)
    access_token = crud.manager.create_access_token(
        data=dict(sub=username), expires=timedelta(hours=6)
    )
    user = crud.manager.get_current_user(access_token)

    resp = RedirectResponse(
        url="/feed",
        status_code=status.HTTP_302_FOUND,
        #     headers={"username": username},
    )
    crud.manager.set_cookie(resp, access_token)
    return resp
    # return {"access_token": access_token, "token_type": "bearer"}


@router.post("/signup", status_code=201)
async def create_user():
    pass


@router.post("/logout", status_code=201)
def logout(request: Request, user=Depends(crud.manager)):
    response = RedirectResponse("/", status_code=302)
    response.delete_cookie(key=crud.manager.cookie_name)
    return response


@router.get("/feed")
def display_feed(request: Request, user=Depends(crud.manager)):
    return templates.TemplateResponse(
        "feed.html", {"request": request, "username": user.username}
    )
