from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


# class ItemBase(BaseModel):
#     title: str
#     description: Optional[str] = None


# class ItemCreate(ItemBase):
#     pass


# class Item(ItemBase):
#     id: int
#     owner_id: int

#     class Config:
#         orm_mode = True


class UserBase(BaseModel):
    username: str
    bio: str
    name: str


class UserCreate(UserBase):
    password: str
    created_date: datetime


class User(UserBase):
    id: int

    # is_active: bool
    # items: List[Item] = []

    class Config:
        orm_mode = True