from pydantic import BaseModel
from datetime import datetime


class BookBase(BaseModel):
    name: str
    price: float
    published: bool = True


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    # created_at: datetime

    class Config:
        orm_mode = True
