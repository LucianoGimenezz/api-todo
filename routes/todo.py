from fastapi import APIRouter, Depends, HTTPException, status, Path
from config.database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
import crud
from schemas.todo import TodoCreate, Todo

todo_route = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@todo_route.post('/users/{user_id}', response_model=Todo)
def create_todo(user_id: int,todo: TodoCreate, db: Session = Depends(get_db)):
    return crud.create_user_todo(db=db, todo=todo, user_id=user_id)


@todo_route.get('/', response_model=list[Todo])
def get_todos(skip: int = 0, limit: int = 10,db: Session = Depends(get_db)):
    todos = crud.get_todos(db, skip=skip, limit=limit)
    return todos

@todo_route.get('/{todo_id}')
def get_todo_by_id(todo_id: Annotated[int, Path(ge=0)], db: Session = Depends(get_db)):
    response = crud.get_todo_by_id(db, todo_id=todo_id)
    if response is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return response

@todo_route.delete('/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    return crud.delete_todo(db=db, todo_id=todo_id)


@todo_route.put('/switchState/{todo_id}', response_model=Todo)
def update_todo_state(todo_id: int, db: Session = Depends(get_db)):
    return crud.update_todo_state(db=db, todo_id=todo_id)



@todo_route.put('/{todo_id}', response_model=Todo)
def update_todo(todo_id: int, todo: TodoCreate, db: Session = Depends(get_db)):
    return crud.update_todo(db=db, todo_id=todo_id, todo=todo)
