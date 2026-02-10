from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key= True, index= True)
    name = Column(String, nullable= False)
    email = Column(String, nullable= False)
    age = Column(Integer, nullable=True)
    hashed_password = Column(String)

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key= True, index= True)
    title = Column(String, nullable= False)
    completed = Column(Boolean, default= False, nullable= False)
    owner_id = Column(Integer, ForeignKey("users.id"))
