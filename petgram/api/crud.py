from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import now
from petgram.db import users, database
from . import schemas
from . import models
from . import security
from fastapi_login import LoginManager
import os
from .. import db


secret = str(os.getenv("SECRET"))
manager = LoginManager(secret, tokenUrl="/auth/token", use_cookie=True)
session = db.SessionLocal()


@manager.user_loader
def load_user(username: str):  # could also be an asynchronous function
    return session.query(models.User).filter(models.User.username == username).first()


def create_user(username: str, password: str, bio: str):
    hashed_password = security.hash_password(password)
    db_user = models.User(
        username=username, hashed_password=hashed_password, bio=bio, created_date=now()
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user