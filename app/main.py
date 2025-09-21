from fastapi import FastAPI
from app.api.endpoints import users, login

app = FastAPI(title="Password Manager API", version="0.1.0")

@app.get("/", tags=["Root"])
def read_root():
    """
    Un endpoint de bienvenida para verificar que la API está funcionando.
    """
    return {"message": "Welcome to your Password Manager API!"}

# Incluimos el router de usuarios en la aplicación principal
app.include_router(login.router, prefix="/login", tags=["Login"])
app.include_router(users.router, prefix="/users", tags=["Users"])