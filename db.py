import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise RuntimeError("database not set")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autoflush= False, 
    autocommit= False, 
    bind=engine
)

class Base(DeclarativeBase):
    pass