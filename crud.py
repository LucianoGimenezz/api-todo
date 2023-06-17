from sqlalchemy.orm import Session
from fastapi import HTTPException
import bcrypt
from models.todo import Todo
from models.user import User
from schemas.todo import TodoCreate
from schemas.user import UserCreate, UserLogin

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = User(email=user.email, username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(User).get(user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="User not found")
    return None

def login_user(db: Session, user: UserLogin):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        if not bcrypt.checkpw(user.password.encode('utf-8'), db_user.hashed_password.encode('utf-8')):
            raise HTTPException(status_code=401, detail="Incorrect password")
        return db_user
    else:   
      raise HTTPException(status_code=404, detail="User not found")
    
# TODOS

def get_todos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Todo).offset(skip).limit(limit).all()

def get_todo_by_id(db: Session, todo_id: int):
    return db.query(Todo).filter(Todo.id == todo_id).first()

def create_user_todo(db: Session, todo: TodoCreate, user_id: int):
    db_item = Todo(**todo.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_todo(db: Session, todo_id: int):
    db_item = db.query(Todo).get(todo_id)

    if db_item:
        db.delete(db_item)
        db.commit()
    else:    
        raise HTTPException(status_code=404, detail="Todo not found")
    return None

def update_todo_state(db: Session, todo_id: int):
    db_todo = db.query(Todo).get(todo_id)
    if db_todo:
        db_todo.is_done = not db_todo.is_done
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

def update_todo(db: Session, todo_id: int, todo: TodoCreate):
    db_todo = db.query(Todo).get(todo_id)
    if db_todo:
        db_todo.title = todo.title
        db_todo.task = todo.task
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo