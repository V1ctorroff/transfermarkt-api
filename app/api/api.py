# app/main.py
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse

# Chave secreta fixa
API_SECRET_KEY = "oipi0asdi0vnjxçlkaosopjdieniubcjxlkncjbsuahwuhicenjbxiubaiuboid"

app = FastAPI()

def require_api_key(request: Request):
    """
    Verifica se a requisição possui a chave correta nos headers.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")

    token = auth_header.split(" ")[1]
    if token != API_SECRET_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")

    return True

@app.get("/")
async def root():
    return {"status": "ok", "message": "Service está rodando"}

@app.get("/secure-data")
async def secure_data(dep: bool = Depends(require_api_key)):
    return {"status": "ok", "data": "Aqui estão os dados seguros!"}
