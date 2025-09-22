from fastapi import FastAPI
from app.api.endpoints import users, login, vault

app = FastAPI(title="Password Manager API", version="0.1.0")

@app.get("/", tags=["Root"])
def read_root():

    return {"message": "Welcome to your Password Manager API!"}

# Incluimos el router de usuarios en la aplicación principal
app.include_router(login.router, prefix="/login", tags=["Login"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(vault.router, prefix="/vault", tags=["Vault"])