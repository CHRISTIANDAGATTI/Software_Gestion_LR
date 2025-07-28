from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.schemas.usuario import UsuarioCreate, UsuarioDB
from app.crud.usuario import crud_usuario
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import requests

router = APIRouter()
security = HTTPBearer()

# Obtiene las claves públicas de Supabase
SUPABASE_JWKS_URL = "https://jpeibrtqlktbrhwemnbi.supabase.co/auth/v1/keys"

def get_supabase_public_keys():
    jwks = requests.get(SUPABASE_JWKS_URL).json()
    return jwks["keys"]

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    jwks = get_supabase_public_keys()
    try:
        payload = jwt.decode(token, jwks, algorithms=["RS256"], options={"verify_aud": False})
        return payload  # contiene el user_id en 'sub'
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

@router.get("/usuario/me", tags=["usuario"])
def get_usuario_actual(payload=Depends(verify_token)):
    return {"user_id": payload["sub"], "email": payload.get("email")}

@router.post("/usuario/registrar", response_model=UsuarioDB, tags=["usuario"])
def registrar_usuario(
    usuario: UsuarioCreate,
    payload=Depends(verify_token),
    db: Session = Depends(SessionLocal)
):
    # Solo permite registrar si el supabase_user_id coincide con el del token
    if str(usuario.supabase_user_id) != str(payload["sub"]):
        raise HTTPException(status_code=403, detail="No autorizado")
    db_usuario = crud_usuario.get_by_supabase_user_id(db, usuario.supabase_user_id)
    if db_usuario:
        raise HTTPException(status_code=400, detail="Usuario ya registrado")
    return crud_usuario.create(db, usuario)
