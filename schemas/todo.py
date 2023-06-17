from pydantic import BaseModel

class TodoBase(BaseModel):
    title: str
    task: str

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    id: int
    is_done: bool
    owner_id: int

    class Config:
        orm_mode = True
