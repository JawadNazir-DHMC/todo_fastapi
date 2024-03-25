from fastapi import FastAPI, HTTPException,Depends
from typing import Union, Optional
from contextlib import asynccontextmanager
from fastapi_neon import settings
from fastapi_neon.database import engine,lifespan,get_session
from fastapi_neon.model import Todo
from sqlmodel import Session,select


app = FastAPI(
    lifespan=lifespan,
    title="Todo App",
    description="Todo App",
    version="0.0.1",
    servers=[{"url": "http://127.0.0.1:8000", "description": "Developmental Server"}],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/todos/", response_model=Todo)
def create_todos(todo: Todo, session: Session = Depends(get_session)):
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


@app.get("/todos/", response_model=list[Todo])
def read_todos(session: Session = Depends(get_session)):
    todos = session.exec(select(Todo)).all()
    return todos
@app.get("/todos/by_id/{todo_id}", response_model=Todo)
def read_todos_by_ID(todo_id:int,session: Session = Depends(get_session)):
    todos = session.exec(select(Todo).where(Todo.id==todo_id)).first()
    if not todos:
        raise HTTPException(status_code=400,detail="Todo does not exist")
    return todos
@app.get("/todos/by_title/{todo_title}", response_model=Todo)
def read_todos_by_Title(todo_title:str,session: Session = Depends(get_session)):
    todos = session.exec(select(Todo).where(Todo.title==todo_title)).first()
    if not todos:
        raise HTTPException(status_code=400,detail="Todo does not exist")
    return todos


@app.patch("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo: Todo, session: Session = Depends(get_session)):
    todo_query = session.exec(select(Todo).where(Todo.id == todo_id)).first()
    if not todo_query:
        raise HTTPException(status_code=400, detail="Todo ID not exist")
    todo_query.title = todo.title
    todo_query.description = todo.description
    todo_query.complete = todo.complete
    session.commit()
    session.refresh(todo_query)
    return todo_query


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, session: Session = Depends(get_session)):
    todo_query = session.exec(select(Todo).where(Todo.id == todo_id)).first()
    if not todo_query:
        raise HTTPException(status_code=400, detail="Todo ID not exist")
    session.delete(todo_query)

    session.commit()
    return {"message": "Todo Deleted"}
