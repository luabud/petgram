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


class LoginError(StrEnum):
    DatabaseError = "DatabaseError"
    InvalidUserNameOrPassword = "InvalidUserNameOrPassword"


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
        return login(request)


@router.get("/login")
def login(request: Request, error: LoginError | None = None):
    return templates.TemplateResponse("login.html", {"request": request, "error": error})


@router.post("/auth")
def login_auth(request: Request, data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password

    error = None
    try:
        potential_user = crud.load_user(username)  # type: ignore
    except:
        error = LoginError.DatabaseError

    if not potential_user or not security.is_same_password(password, potential_user.hashed_password):
        error = LoginError.InvalidUserNameOrPassword

    if error:
        return login(request, error)

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
