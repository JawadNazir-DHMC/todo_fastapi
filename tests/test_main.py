from fastapi.testclient import TestClient
from sqlmodel import SQLModel,Field,Session,create_engine,select
from fastapi_neon.main import app,get_session,Todo
from fastapi_neon import settings

def test_read_main():
    client = TestClient(app=app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello":"World"}

def test_write_main():
    connection_string = str(settings.Test_Data_Base_URL).replace(
    "postgresql", "postgresql+psycopg")
    engine = create_engine(connection_string, connect_args={"sslmode": "require"}, pool_recycle=300)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        def get_session_override():
            return session

        app.dependency_overrides[get_session] = get_session_override

        client = TestClient(app=app)
        
        # Test creating a todo
        todo_data = {"title": "Test Todo", "description": "This is a test todo","complete":False}
        response = client.post("/todos/", json=todo_data)
        assert response.status_code == 200
        created_todo = response.json()
        assert created_todo["title"] == todo_data["title"]
        assert created_todo["description"] == todo_data["description"]
        assert "id" in created_todo
            

        
 
def test_read_list_main():
        connection_string = str(settings.Test_Data_Base_URL).replace(
    "postgresql", "postgresql+psycopg")
        engine=create_engine(connection_string,connect_args={"sslmode":"require"},pool_recycle=300)
        SQLModel.metadata.create_all(engine)    
        with Session(engine) as session:
            def get_session_override():
                return session
            app.dependency_overrides[get_session]=get_session_override

            client=TestClient(app=app)
            response=client.get("/todos/")
            assert response.status_code==200
def test_update_main():
    connection_string = str(settings.Test_Data_Base_URL).replace(
    "postgresql", "postgresql+psycopg")
    engine = create_engine(connection_string, connect_args={"sslmode": "require"}, pool_recycle=300)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        def get_session_override():
            return session

        app.dependency_overrides[get_session] = get_session_override

        client = TestClient(app=app)
        todo_id=9
        updated_todo_data={"title":"Updated Title","description":"Updated Description","complete":True}
        response=client.patch(f"/todos/{todo_id}",json=updated_todo_data)
        assert response.status_code == 200
        updated_todo=response.json()
        assert updated_todo["title"]==updated_todo_data["title"]   
        assert updated_todo["description"]==updated_todo_data["description"]   
        assert updated_todo["complete"]==updated_todo_data["complete"]
def test_delete_main():
    connection_string = str(settings.Test_Data_Base_URL).replace(
    "postgresql", "postgresql+psycopg")
    engine = create_engine(connection_string, connect_args={"sslmode": "require"}, pool_recycle=300)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        def get_session_override():
            return session

        app.dependency_overrides[get_session] = get_session_override
        client=TestClient(app=app)
        todo_id=9
        response=client.delete(f"/todos/{todo_id}")
        assert response.status_code == 200