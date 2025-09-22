from httpx import AsyncClient
import pytest

pytestmark = pytest.mark.asyncio

async def test_create_user(client: AsyncClient):
    """
    Test para la creación exitosa de un usuario.
    """
    response = await client.post(
        "/users/",
        json={"email": "testuser@example.com", "password": "testpassword"},
    )
    assert response.status_code == 201
    
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert "id" in data
    assert "hashed_password" not in data  # Asegurarnos de que no se devuelve la contraseña

async def test_create_duplicate_user(client: AsyncClient):
    """
    Test para verificar que no se puede crear un usuario con un email duplicado.
    """
    # Primero, creamos el usuario
    await client.post(
        "/users/",
        json={"email": "duplicate@example.com", "password": "testpassword"},
    )
    
    # Luego, intentamos crearlo de nuevo
    response = await client.post(
        "/users/",
        json={"email": "duplicate@example.com", "password": "testpassword"},
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]