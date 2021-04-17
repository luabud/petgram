from sqlalchemy import Boolean, Column, ForeignKey, TIMESTAMP, Integer, String, DateTime

# from sqlalchemy.orm import relationship

from ..db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    name = Column(String)
    bio = Column(String)
    hashed_password = Column(String)
    created_date = Column(TIMESTAMP)
    # created_date = Column(DateTime, default=True)

    # items = relationship("Item", back_populates="owner")


# class Item(Base):
#     __tablename__ = "photo"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))

#     owner = relationship("User", back_populates="items")