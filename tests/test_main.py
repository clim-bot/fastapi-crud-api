from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_item():
    response = client.post("/items", json={"name": "Test Item", "description": "This is a test"})
    assert response.status_code == 200
    item = response.json()
    assert "id" in item
    assert item["name"] == "Test Item"

def test_read_items():
    response = client.get("/items")
    assert response.status_code == 200

def test_create_and_fetch_item():
    response = client.post("/items", json={"name": "Test Item", "description": "This is a test item"})
    assert response.status_code == 200
    item = response.json()
    assert "id" in item
    item_id = item["id"]

    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Item"

def test_read_item():
    response = client.post("/items", json={"name": "Temporary Item", "description": "This is temporary"})
    assert response.status_code == 200
    item_id = response.json()["id"]

    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200

def test_update_item():
    response = client.post("/items", json={"name": "Item to Update", "description": "This needs updating"})
    assert response.status_code == 200
    item_id = response.json()["id"]
    
    response = client.put(f"/items/{item_id}", json={"name": "Updated", "description": "Updated description"})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated"

def test_delete_item():
    response = client.post("/items", json={"name": "Item to Delete", "description": "To be deleted"})
    assert response.status_code == 200
    item_id = response.json()["id"]
    
    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 200