import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from tortoise import Tortoise

from main import app
from models.user import User

# Initialize the TestClient
client = TestClient(app)

# Database configuration for testing
DB_URL = "sqlite://:memory:"

DB_CONFIG = {
    "connections": {
        "default": DB_URL
    },
    "apps": {
        "models": {
            "models": ["models.user"],
            "default_connection": "default",
        }
    }
}

@pytest_asyncio.fixture(scope="module")
async def event_loop():
    """Create an instance of the default event loop for each test case."""
    import asyncio
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="module", autouse=True)
async def initialize_tests():
    """Initialize the test database."""
    try:
        await Tortoise.init(config=DB_CONFIG)
        await Tortoise.generate_schemas()
        yield
    finally:
        await Tortoise.close_connections()

@pytest_asyncio.fixture(autouse=True)
async def cleanup_db():
    """Clean database before each test."""
    await User.all().delete()

@pytest.mark.asyncio
async def test_get_empty_users():
    response = client.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] is True
    assert data["data"] == []
    assert "errors" in data

@pytest.mark.asyncio
async def test_create_user():
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass"
    }
    response = client.post("/user", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] is True
    assert data["data"]["email"] == user_data["email"]
    assert data["data"]["username"] == user_data["username"]
    assert "password" not in data["data"]  # Password should not be returned

@pytest.mark.asyncio
async def test_get_users_after_creation():
    # Create a test user directly
    await User.create(
        email="test@example.com",
        username="testuser",
        password="testpass"
    )
    
    response = client.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] is True
    assert len(data["data"]) == 1
    assert data["data"][0]["email"] == "test@example.com"
    assert data["data"][0]["username"] == "testuser"
    assert "password" not in data["data"][0]

@pytest.mark.asyncio
async def test_update_user():
    # Create a test user directly
    user = await User.create(
        email="test@example.com",
        username="testuser",
        password="testpass"
    )
    
    updated_data = {
        "email": "updated@example.com",
        "username": "updateduser",
        "password": "updatedpass"
    }
    
    response = client.put(f"/users/{user.id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] is True
    assert data["data"]["email"] == updated_data["email"]
    assert data["data"]["username"] == updated_data["username"]
    
    # Verify in database
    updated_user = await User.get(id=user.id)
    assert updated_user.email == updated_data["email"]
    assert updated_user.username == updated_data["username"]

@pytest.mark.asyncio
async def test_delete_user():
    # Create a test user directly
    user = await User.create(
        email="test@example.com",
        username="testuser",
        password="testpass"
    )
    
    response = client.delete(f"/users/{user.id}")
    assert response.status_code == 200
    assert response.json()["status"] is True
    assert response.json()["data"] == f"User {user.id} deleted"
    
    # Verify user is actually deleted
    assert await User.filter(id=user.id).count() == 0

@pytest.mark.asyncio
async def test_get_non_existent_user():
    # Try to update a non-existent user
    non_existent_id = 9999
    response = client.put(
        f"/users/{non_existent_id}",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpass"
        }
    )
    assert response.status_code == 404
    
    # Try to delete a non-existent user
    response = client.delete(f"/users/{non_existent_id}")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_create_user_duplicate_email():
    # Create initial user
    await User.create(
        email="test@example.com",
        username="testuser1",
        password="testpass"
    )
    
    # Try to create another user with same email
    user_data = {
        "email": "test@example.com",
        "username": "testuser2",
        "password": "testpass"
    }
    response = client.post("/user", json=user_data)
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "email" in data["detail"].lower()

@pytest.mark.asyncio
async def test_create_user_duplicate_username():
    # Create initial user
    await User.create(
        email="test1@example.com",
        username="testuser",
        password="testpass"
    )
    
    # Try to create another user with same username
    user_data = {
        "email": "test2@example.com",
        "username": "testuser",
        "password": "testpass"
    }
    response = client.post("/user", json=user_data)
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "username" in data["detail"].lower()