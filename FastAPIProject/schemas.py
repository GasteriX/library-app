from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    author: str
    description: str = None

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
