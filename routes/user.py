from fastapi import APIRouter, Depends, HTTPException, Path, status
from typing import Annotated
from schemas.user import UserCreate, User, UserLogin
from schemas.auth import Token
from sqlalchemy.orm import Session
from config.database import SessionLocal
import crud
from consts import ALGORITHM as algorithm
import os
from datetime import timedelta, datetime
import jwt

user_route = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@user_route.get('/', response_model=list[User])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)

@user_route.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@user_route.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return crud.delete_user(db=db, user_id=user_id)
    
@user_route.post("/logIn", response_model=Token)
def authenticate_user(user: UserLogin, db: Session = Depends(get_db)):
    user_response =  crud.login_user(db=db, user=user)
    print(os.environ.get('SECRET'))
    payload = {"sub": user_response.id, "username": user_response.username, "exp": datetime.utcnow() + timedelta(weeks=2)}
    access_token = jwt.encode(payload, os.environ.get('SECRET'), algorithm=algorithm)
    return {"access_token": access_token, "token_type": "Bearer"}

@user_route.get("/users/{user_id}", response_model=User)
def get_user_by_id(user_id: Annotated[int, Path(ge=0)], db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

