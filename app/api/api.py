from fastapi import APIRouter, Request, HTTPException, Depends

from app.api.endpoints import clubs, competitions, players

API_SECRET_KEY = "oipi0asdi0vnjxçlkaosopjdieniubcjxlkncjbsuahwuhicenjbxiubaiuboid"

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


api_router = APIRouter()

api_router.include_router(
    competitions.router,
    prefix="/competitions",
    tags=["competitions"],
    dependencies=[Depends(require_api_key)]
)
api_router.include_router(
    clubs.router,
    prefix="/clubs",
    tags=["clubs"],
    dependencies=[Depends(require_api_key)]
)
api_router.include_router(
    players.router,
    prefix="/players",
    tags=["players"],
    dependencies=[Depends(require_api_key)]
)
