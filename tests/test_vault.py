from httpx import AsyncClient
import pytest

pytestmark = pytest.mark.asyncio

async def test_create_vault_item(authenticated_client: AsyncClient):
    """
    Test para crear un item en la bóveda con un cliente autenticado.
    """
    response = await authenticated_client.post(
        "/vault/",
        json={
            "username": "test_vault_user",
            "password": "vault_password",
            "url": "https://test-vault.com",
            "notes": "Some notes here"
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "test_vault_user"
    assert data["url"] == "https://test-vault.com/" # Pydantic normaliza la URL
    assert "password" not in data # La contraseña no debe devolverse

async def test_read_vault_items(authenticated_client: AsyncClient):
    """
    Test para leer los items de la bóveda de un usuario.
    """
    # Paso 1: Crear un item primero para tener algo que leer.
    item_data = {
        "username": "user_to_read",
        "password": "password_to_read",
        "url": "https://readable.com"
    }
    await authenticated_client.post("/vault/", json=item_data)
    
    # Paso 2: Ahora sí, pedir la lista de items.
    response = await authenticated_client.get("/vault/")
    
    # Paso 3: Verificar la respuesta.
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1  # Sabemos que debe haber exactamente 1 item.
    assert data[0]["username"] == "user_to_read"
    assert data[0]["url"] == "https://readable.com/"

async def test_unauthenticated_access_to_vault(client: AsyncClient):
    """
    Test para verificar que un cliente no autenticado no puede acceder a la bóveda.
    """
    response = await client.get("/vault/")
    assert response.status_code == 401 # Unauthorized
    assert "Not authenticated" in response.json()["detail"]