from config.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255),  unique=True, index=True)
    hashed_password = Column(String(255))
    username = Column(String(255),  unique=True, index=True)
    
    todos = relationship('Todo', back_populates='owner')