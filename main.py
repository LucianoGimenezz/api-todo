from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from config.database import  engine
from routes.user import user_route
from routes.todo import todo_route
from dotenv import load_dotenv
from consts import ALGORITHM as algorithm
import models.todo as todo
import models.user as user
import os
import jwt


load_dotenv()
user.Base.metadata.create_all(bind=engine)
todo.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.middleware("http")
async def check_permissions(request: Request, call_next):
    path = request.url.path
    if path.startswith("/api/users/logIn") or (path.startswith('/api/users') and request.method == "POST"):
        response = await call_next(request)
        return response
    if path.startswith('/api/todos'):
        header = request.headers.get("Authorization")
        if header is None or header.lower().startswith('bearer') is False:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Not found"})
        token = header.split(' ')[1]
        try:
           jwt.decode(token, key=os.environ.get('SECRET'), algorithms=[algorithm])
        except: 
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Not found"})
        response = await call_next(request)
        return response
    response = await call_next(request)
    return response 

app.include_router(user_route, prefix="/api/users", tags=["users"])
app.include_router(todo_route, prefix="/api/todos", tags=["todos"])


