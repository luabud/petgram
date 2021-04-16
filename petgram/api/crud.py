from sqlalchemy.orm import Session
from petgram.db import users, database
from . import models
from fastapi_login import LoginManager
import os
from .. import db


secret = str(os.getenv("SECRET"))
manager = LoginManager(secret, tokenUrl="/auth/token", use_cookie=True)
session = db.SessionLocal()


@manager.user_loader
def load_user(username: str):  # could also be an asynchronous function
    return session.query(models.User).filter(models.User.username == username).first()