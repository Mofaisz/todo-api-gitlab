from fastapi import FastAPI
from routers import todo
from database import engine
import models

app = FastAPI(title="To-Do List API", version="1.0")

models.Base.metadata.create_all(bind=engine)

app.include_router(todo.router)

@app.get("/")
def home():
    return {"message": "Welcome to the FastAPI To-Do List API"}
