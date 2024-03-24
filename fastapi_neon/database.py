from fastapi_neon import settings
from sqlmodel import create_engine,SQLModel,Session
from fastapi import FastAPI
from contextlib import asynccontextmanager

connection_string = str(settings.Data_Base_URL).replace(
    "postgresql", "postgresql+psycopg"
)
engine = create_engine(
    connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating Tables----")
    create_db_and_tables()
    yield

def get_session():
    with Session(engine) as session:
        yield session
