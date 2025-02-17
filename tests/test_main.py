import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
token = None  # ✅ Global variable to store token

def test_register_user():
    """
    Test registering a new user.
    """
    response = client.post("/users", json={"username": "testuser", "password": "testpass"})
    assert response.status_code in [200, 400]  # 400 if user already exists

def test_login_user():
    """
    Test logging in the user and store the token in a global variable.
    """
    global token
    response = client.post("/login", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200, f"Login failed: {response.json()}"

    token = response.json().get("access_token")
    assert token is not None, "JWT token was not returned"

def get_auth_headers():
    """
    Utility function to get the authorization headers.
    """
    assert token is not None, "Token is not set. Ensure test_login_user runs first."
    return {"Authorization": f"Bearer {token}"}

def test_create_item():
    """Test creating an item with authentication."""
    headers = get_auth_headers()
    response = client.post("/items", json={"name": "Test Item", "description": "This is a test"}, headers=headers)
    assert response.status_code == 200
    assert "id" in response.json()

def test_read_items():
    """Retrieve all items with authentication."""
    headers = get_auth_headers()
    response = client.get("/items", headers=headers)
    assert response.status_code == 200

def test_create_and_fetch_item():
    """Create and fetch an item with authentication."""
    headers = get_auth_headers()
    response = client.post("/items", json={"name": "Test Item", "description": "This is a test item"}, headers=headers)
    assert response.status_code == 200
    item = response.json()
    assert "id" in item
    item_id = item["id"]

    response = client.get(f"/items/{item_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Item"

def test_read_item():
    """Create and read an item with authentication."""
    headers = get_auth_headers()
    response = client.post("/items", json={"name": "Temporary Item", "description": "This is temporary"}, headers=headers)
    assert response.status_code == 200
    item_id = response.json()["id"]

    response = client.get(f"/items/{item_id}", headers=headers)
    assert response.status_code == 200

def test_update_item():
    """Create and update an item with authentication."""
    headers = get_auth_headers()
    response = client.post("/items", json={"name": "Item to Update", "description": "This needs updating"}, headers=headers)
    assert response.status_code == 200
    item_id = response.json()["id"]

    response = client.put(f"/items/{item_id}", json={"name": "Updated", "description": "Updated description"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated"

def test_delete_item():
    """Create and delete an item with authentication."""
    headers = get_auth_headers()
    response = client.post("/items", json={"name": "Item to Delete", "description": "To be deleted"}, headers=headers)
    assert response.status_code == 200
    item_id = response.json()["id"]

    response = client.delete(f"/items/{item_id}", headers=headers)
    assert response.status_code == 200
