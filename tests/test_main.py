from fastapi.testclient import TestClient
from fastapi import HTTPException
from sqlmodel import SQLModel,Field,Session,create_engine,select
from fastapi_neon.database import get_session
from fastapi_neon.main import app
from fastapi_neon.model import Todo
from fastapi_neon import settings

def get_client_with_Override_session():
    connection_string = str(settings.Test_Data_Base_URL).replace(
    "postgresql", "postgresql+psycopg")
    engine = create_engine(connection_string, connect_args={"sslmode": "require"}, pool_recycle=300)
    SQLModel.metadata.create_all(engine)
    def get_session_override():
        return Session(engine)

    app.dependency_overrides[get_session] = get_session_override

    return TestClient(app=app)
    

def test_read_main():
    client = TestClient(app=app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello":"World"}

def test_write_main():
        client=get_client_with_Override_session()
        todo_data = {"title": "Test Todo", "description": "This is a test todo","complete":False}
        response = client.post("/todos/", json=todo_data)
        assert response.status_code == 200
        created_todo = response.json()
        assert created_todo["title"] == todo_data["title"]
        assert created_todo["description"] == todo_data["description"]
        assert "id" in created_todo
                 
 
def test_read_list_main():
        client=get_client_with_Override_session()
        response=client.get("/todos/")
        assert response.status_code==200
def test_read_Id():
        client=get_client_with_Override_session()
        todo_id=32
        response=client.get(f"/todos/by_id/{todo_id}")
        assert response.status_code==200
def test_read_Id_non_existant():
        client=get_client_with_Override_session()
        todo_id=2
        response=client.get(f"/todos/by_id/{todo_id}")
        assert response.status_code==400
        assert response.json()== {"detail":"Todo does not exist"}
def test_read_title():
        client=get_client_with_Override_session()
        todo_title="Updated Title"
        response=client.get(f"/todos/by_title/{todo_title}")
        assert response.status_code==200
def test_read_title_non_existant():
        client=get_client_with_Override_session()
        todo_title="Excercise"
        response=client.get(f"/todos/by_title/{todo_title}")
        assert response.status_code==400
        assert response.json()== {"detail":"Todo does not exist"}





def test_update_main():
        client=get_client_with_Override_session()
        todo_id=26
        updated_todo_data={"title":"Updated Title","description":"Updated Description","complete":True}
        response=client.patch(f"/todos/{todo_id}",json=updated_todo_data)
        assert response.status_code == 200
        updated_todo=response.json()
        assert updated_todo["title"]==updated_todo_data["title"]   
        assert updated_todo["description"]==updated_todo_data["description"]   
        assert updated_todo["complete"]==updated_todo_data["complete"]
def test_update_non_existant_todo():
        client=get_client_with_Override_session()
        todo_id_non_existant=7
        updated_todo_data={"title":"Updated Title","description":"Updated Description","complete":True}
        response=client.patch(f"/todos/{todo_id_non_existant}",json=updated_todo_data)
        assert response.status_code == 400
        assert response.json() == {'detail': 'Todo ID not exist'}  
def test_delete_main():
        client=get_client_with_Override_session()
        todo_id=27
        response=client.delete(f"/todos/{todo_id}")
        assert response.status_code == 200
        
def test_delete_non_existant_todo():
        client=get_client_with_Override_session()
        todo_id_non=15
        response=client.delete(f"/todos/{todo_id_non}")
        assert response.status_code == 400
        assert response.json()=={"detail":"Todo ID not exist"}
        
