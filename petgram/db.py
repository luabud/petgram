import os

from databases import Database
from sqlalchemy.sql import func
from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URI = str(os.getenv("DATABASE_URL"))
engine = create_engine(SQLALCHEMY_DATABASE_URI)
metadata = MetaData()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(30)),
    Column("name", String(50)),
    Column("bio", String(250)),
    Column("hashed_password", String(250)),
    Column("created_date", DateTime, default=func.now(), nullable=False),
)

metadata.create_all(engine)
# databases query builder
database = Database(SQLALCHEMY_DATABASE_URI)
