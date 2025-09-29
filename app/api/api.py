from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from clerk_backend_api import Clerk   # import correto do SDK oficial
from app.api.api import api_router  

# Coloque sua chave aqui (não recomendado para produção)
CLERK_SECRET_KEY = "sk_test_y4kxPs5EjcUEEVdUkBGT1kV1VPNtcOqKnSaxbjcmpd"

clerk = Clerk(api_key=CLERK_SECRET_KEY)

app = FastAPI()

def require_clerk_session(request: Request):
    """
    Verifica se há sessão válida com Clerk.
    Levanta HTTPException(401) se não for válido.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")

    token = auth_header.split(" ")[1]

    try:
        session = clerk.sessions.verify_session(token)
        return session
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid Clerk session: {str(e)}")

app.include_router(
    api_router,
    prefix="/api",
    dependencies=[Depends(require_clerk_session)]
)

@app.get("/")
async def root():
    return {"status": "ok", "message": "Service está rodando"}
