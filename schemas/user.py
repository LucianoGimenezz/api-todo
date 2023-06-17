from pydantic import BaseModel
from .todo import Todo

class UserBase(BaseModel):
    email: str
    username: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    todos: list[Todo] = []

    class Config:
        orm_mode = True