from httpx import AsyncClient
import pytest

pytestmark = pytest.mark.asyncio

async def test_create_user(client: AsyncClient):
    """
    Test for successful user creation.
    Verify that the endpoint returns a JWT token.
    """
    response = await client.post(
        "/users/",
        json={"email": "testuser@example.com", "password": "testpassword"},
    )
    assert response.status_code == 201
    
    data = response.json()
    
    assert "access_token" in data
    assert data["token_type"] == "bearer"

async def test_create_duplicate_user(client: AsyncClient):
    """
    Test to verify that a user cannot be created with a duplicate email address.
    """
    await client.post(
        "/users/",
        json={"email": "duplicate@example.com", "password": "testpassword"},
    )
    
    response = await client.post(
        "/users/",
        json={"email": "duplicate@example.com", "password": "testpassword"},
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]