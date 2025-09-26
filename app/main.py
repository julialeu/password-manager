from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import users, login, vault
from app.core.config import settings
from app.db.init_db import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código que se ejecuta ANTES de que la aplicación empiece a aceptar peticiones
    print("--- Application starting up ---")
    create_db_and_tables()
    yield
    print("--- Application shutting down ---")

app = FastAPI(
    title="Password Manager API",
    version="0.1.0",
    lifespan=lifespan
)


origins = []
if settings.CORS_ORIGINS:
    origins.extend([origin.strip() for origin in settings.CORS_ORIGINS.split(",")])
else:
    origins.extend([
        "http://localhost",
        "http://localhost:5173",
    ])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to your Password Manager API!"}

app.include_router(login.router, prefix="/login", tags=["Login"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(vault.router, prefix="/vault", tags=["Vault"])