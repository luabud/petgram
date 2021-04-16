from sqlalchemy.orm import Session
from petgram.db import users, database
from . import models
from fastapi_login import LoginManager
import os


secret = str(os.getenv("SECRET"))
manager = LoginManager(secret, tokenUrl="/auth/token")


@manager.user_loader
def load_user(db: Session, username: str):  # could also be an asynchronous function
    return db.query(models.User).filter(models.User.username == "blacknight").first()