from fastapi import APIRouter, Depends
from schemas import TodoResponse, TodoCreate
from sqlalchemy.orm import Session
from models import User, Todo
from dependencies import get_current_user, get_db

router = APIRouter(prefix="/todos", tags=["Todos"])

@router.post("/create", response_model= TodoResponse)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_todo = Todo(
        title = todo.title, 
        owner_id = current_user.id
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.get("/get", response_model=list[TodoResponse])
def get_todo(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_todo = db.query(Todo).filter(Todo.owner_id == current_user.id).all()
    return db_todo