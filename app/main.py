from fastapi import FastAPI
from app.api.endpoints import users, login, vault
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Password Manager API", version="0.1.0")

origins = [
    "http://localhost:5173",
    "http://localhost",
]

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