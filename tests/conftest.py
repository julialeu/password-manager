# tests/conftest.py

import pytest
import asyncio
from typing import Generator, AsyncGenerator
from httpx import AsyncClient, ASGITransport

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.api import deps
from app.db.base_class import Base

# --- CONFIGURACIÓN DE BASE DE DATOS DE PRUEBA (SÍNCRONA Y ESTABLE) ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# --- SOBREESCRITURA DE DEPENDENCIAS ---
def override_get_db() -> Generator:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[deps.get_db] = override_get_db


# --- FIXTURES ---

@pytest.fixture(scope="session")
def event_loop():
    """Crea un bucle de eventos para toda la sesión de tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function", autouse=True)
def db_setup_and_teardown():
    """

    Crea las tablas antes de cada test y las borra después.
    El alcance 'function' asegura un estado limpio para cada test.
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    """
    Cliente HTTP no autenticado.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


@pytest.fixture(scope="function")
async def authenticated_client(client: AsyncClient) -> AsyncClient:
    """
    Cliente HTTP autenticado. Alcance de función para asegurar el aislamiento.
    """
    user_credentials = {"email": f"testauth-{id(client)}@example.com", "password": "testpassword"}
    await client.post("/users/", json=user_credentials)

    login_response = await client.post(
        "/login/token",
        data={"username": user_credentials["email"], "password": user_credentials["password"]},
    )
    token = login_response.json()["access_token"]

    client.headers["Authorization"] = f"Bearer {token}"
    yield client

    del client.headers["Authorization"]