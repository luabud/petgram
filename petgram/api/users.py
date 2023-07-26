from starlette.responses import RedirectResponse, Response
from petgram.api import crud, models
from fastapi import Depends, status, Request, Form
from fastapi import APIRouter
from enum import StrEnum

from petgram.api.exceptions import (
    InvalidCredentialsException,
    PasswordMismatchError,
    SignupFailedError,
    UsernameTakenError,
    DatabaseAccessException,
)
from . import security
from . import crud
from datetime import timedelta
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.security import OAuth2PasswordRequestForm

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="frontend/templates")

router = APIRouter()


class SignupError(StrEnum):
    UserAlreadyExists = "UserAlreadyExists"
    PasswordsDoNotMatch = "PasswordsDoNotMatch"
    UserCreationFailed = "UserCreationFailed"


def validate_credential(user, password):
    if not user or not security.is_same_password(password, user.hashed_password):
        raise InvalidCredentialsException


def return_template(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/signup")
def signup(request: Request, error: SignupError | None = None):
    return templates.TemplateResponse("signup.html", {"request": request, "error": error})


@router.post("/create", status_code=201)
async def create_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    retyped_password: str = Form(...),
    bio: str = Form(...),
):
    db_user = crud.load_user(username=username)

    error = None
    if db_user:
        error = SignupError.UserAlreadyExists
    elif not security.is_same_password(
        password, security.hash_password(retyped_password)
    ):
        error = SignupError.PasswordsDoNotMatch
    else:
        try:
            user = crud.create_user(username, password, bio)
        except:
            error = SignupError.UserCreationFailed

    if error:
        # Display error and allow user to try again
        return signup(request, error)
    else:
        # User created successfully, prompt them to login
        return return_template(request)


@router.get("/login")
def login(request: Request):
    return return_template(request)


@router.post("/auth/token")
def login_auth(response: Response, data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password
    try:
        potential_user = crud.load_user(username)  # type: ignore
    except:
        raise DatabaseAccessException

    if not potential_user:
        raise InvalidCredentialsException

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


@router.get("/feed")
def display_feed(request: Request, user: models.User = Depends(crud.manager)):
    return templates.TemplateResponse(
        "feed.html", {"request": request, "username": str(user.username)}
    )


@router.post("/logout", status_code=201)
def logout(request: Request, user: models.User = Depends(crud.manager)):
    response = RedirectResponse("/", status_code=302)
    response.delete_cookie(key=crud.manager.cookie_name)
    return response
