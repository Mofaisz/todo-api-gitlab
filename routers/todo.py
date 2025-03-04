from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
import schemas
from typing import List

router = APIRouter(prefix="/todos", tags=["To-Do"])

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.TodoResponse)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    new_todo = models.Todo(**todo.dict())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@router.get("/",response_model =List[schemas.TodoResponse])
def get_all_todo(db: Session = Depends(get_db)):
    return db.query(models.Todo).all()

@router.get("/{id}",response_model=schemas.TodoResponse)
def get_todo_id(id:int,db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(id == models.Todo.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="To-Do not found")
    return todo


@router.put("/{id}",response_model=schemas.TodoResponse)
def update_todo(id:int, updated_todo: schemas.TodoCreate,db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(id == models.Todo.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="To-Do not found")
    for key,value in updated_todo.dict().items():
        setattr(todo,key,value)
    
    db.commit()
    db.refresh(todo)
    return "todo-updated"


@router.delete("/{id}", response_model=schemas.TodoResponse)
def delete_todo(id:int ,db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(id == models.Todo.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="To-Do not found")
    db.delete(todo)
    db.commit()
    return "todo-deleted"