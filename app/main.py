from fastapi import FastAPI

app = FastAPI(title="Password Manager API", version="0.1.0")

@app.get("/", tags=["Root"])
def read_root():
   
    return {"message": "Welcome to your Password Manager API!"}