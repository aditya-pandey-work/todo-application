from fastapi import APIRouter, Depends, HTTPException
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

@router.put("/alter", response_model= TodoResponse)
def alter_todo(todo: TodoResponse, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_todo = db.query(Todo).filter(Todo.id == todo.id, Todo.owner_id == current_user.id).first()

    if not db_todo:
        raise HTTPException(status_code=404, detail="not found")
    
    db_todo.title = todo.title
    db_todo.completed = todo.completed

    db.commit()
    db.refresh(db_todo)
    
    return db_todo

@router.delete("/remove")
def delete_todo(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_todo = db.query(Todo).filter(Todo.id == id, Todo.owner_id == current_user.id).first()

    if not db_todo:
        raise HTTPException(status_code= 404, detail="todo not found")

    db.delete(db_todo)
    db.commit()

    return {"message": "todo not found"}