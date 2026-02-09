from fastapi import FastAPI, Depends, HTTPException
from db import Base, engine
from sqlalchemy.orm import Session
from schemas import UserRegister, UserLogin
from dependencies import get_db
from models import User
from auth import hash_password, verify_password, create_access_token
import todo

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(todo.router,prefix="/api")

@app.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="user already exists")
    
    db_user = User(
        name = user.name, 
        email = user.email, 
        hashed_password = hash_password(user.password)
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "Registered"}

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="wrong details")
    
    token = create_access_token({"sub": str(db_user.id)})
    return {"access_token": token, "token_type": "bearer"}