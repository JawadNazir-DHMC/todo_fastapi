from fastapi import FastAPI,HTTPException
from typing import Union,Optional
from contextlib import asynccontextmanager
from sqlmodel import SQLModel,create_engine,Session,Field,select
from fastapi_neon import settings
from fastapi import Depends

class Todo(SQLModel,table=True):
    id:Optional[int]=Field(default=None,primary_key=True)
    title:str=Field(index=True)
    description:str
    complete:bool

connection_string=str(settings.Data_Base_URL).replace("postgresql","postgresql+psycopg")
engine=create_engine(connection_string,connect_args={"sslmode":"require"},pool_recycle=300)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Creating Tables----")
    create_db_and_tables()
    yield
        

app=FastAPI(lifespan=lifespan,title="Todo App",description="Todo App",version="0.0.1",servers=[{"url":"http://127.0.0.1:8000","description":"Developmental Server"}])

def get_session():
    with Session(engine) as session:
        yield session

@app.get("/")
def read_root():
    return {"Hello":"World"}

@app.post("/todos/",response_model=Todo)
def create_todos(todo:Todo,session:Session=Depends(get_session)):
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo
@app.get("/todos/", response_model=list[Todo])
def read_todos(session:Session=Depends(get_session)):
    todos=session.exec(select(Todo)).all()
    return todos
@app.patch("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id:int, todo:Todo, session:Session=Depends(get_session)):
    todo_query=session.exec(select(Todo).where(Todo.id==todo_id)).first()
    if not todo_query:
        raise HTTPException(status_code=400,detail="Todo ID not exist")
    todo_query.title=todo.title
    todo_query.description=todo.description
    todo_query.complete=todo.complete
    session.commit()
    session.refresh(todo_query)
    return todo_query
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id:int, session:Session=Depends(get_session)):
    todo_query=session.exec(select(Todo).where(Todo.id==todo_id)).first()
    if not todo_query:
        raise HTTPException(status_code=400,detail="Todo ID not exist")
    session.delete(todo_query)

    session.commit()
    return {"message":"Todo Deleted"}