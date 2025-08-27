from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.schemas.usuario import UsuarioCreate, UsuarioDB, UsuarioUpdate
from app.schemas.tenant import TenantCreate
from app.crud.usuario import crud_usuario
from app.crud.tenant import tenant as crud_tenant
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List
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

def get_or_create_demo_tenant(db: Session):
    """Obtiene el tenant demo o lo crea si no existe"""
    demo_tenant = crud_tenant.get_by_slug(db, slug="demo")
    
    if not demo_tenant:
        # Crear tenant demo
        demo_tenant_data = TenantCreate(
            nombre="Tenant Demo",
            slug="demo",
            descripcion="Tenant de demostración para nuevos usuarios. Los usuarios inician aquí hasta ser asignados a una empresa específica.",
            activo=True
        )
        demo_tenant = crud_tenant.create(db, obj_in=demo_tenant_data)
        print(f"✅ Tenant demo creado: {demo_tenant.id}")
    
    return demo_tenant

@router.get("/usuario/me", tags=["usuario"])
def get_usuario_actual(payload=Depends(verify_token), db: Session = Depends(SessionLocal)):
    """Obtener información completa del usuario actual incluyendo su tenant"""
    user_id = payload["sub"]
    usuario = crud_usuario.get_by_supabase_user_id(db, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return {
        "user_id": user_id,
        "email": payload.get("email"),
        "usuario_db": usuario,
        "tenant": usuario.tenant,
        "es_demo": usuario.tenant.slug == "demo"
    }

@router.post("/usuario/registrar", response_model=UsuarioDB, tags=["usuario"])
def registrar_usuario(
    usuario: UsuarioCreate,
    payload=Depends(verify_token),
    db: Session = Depends(SessionLocal)
):
    """Registrar nuevo usuario asignándolo automáticamente al tenant demo"""
    # Solo permite registrar si el supabase_user_id coincide con el del token
    if str(usuario.supabase_user_id) != str(payload["sub"]):
        raise HTTPException(status_code=403, detail="No autorizado")
    
    db_usuario = crud_usuario.get_by_supabase_user_id(db, usuario.supabase_user_id)
    if db_usuario:
        raise HTTPException(status_code=400, detail="Usuario ya registrado")
    
    # SIEMPRE asignar tenant demo a nuevos usuarios
    demo_tenant = get_or_create_demo_tenant(db)
    usuario.tenant_id = demo_tenant.id
    
    print(f"🆕 Registrando nuevo usuario {usuario.email} con tenant demo: {demo_tenant.id}")
    
    # Crear el usuario con el tenant demo asignado
    nuevo_usuario = crud_usuario.create(db, usuario)
    
    print(f"✅ Usuario registrado exitosamente: {nuevo_usuario.id} con tenant demo: {nuevo_usuario.tenant_id}")
    
    return nuevo_usuario

# ENDPOINTS DE ADMINISTRACIÓN

@router.get("/admin/usuarios", response_model=List[UsuarioDB], tags=["admin"])
def listar_usuarios_admin(
    db: Session = Depends(SessionLocal),
    payload=Depends(verify_token)
):
    """Listar todos los usuarios (solo para administradores)"""
    # TODO: Verificar que el usuario es admin
    usuarios = crud_usuario.get_multi(db)
    return usuarios

@router.get("/admin/usuarios/demo", response_model=List[UsuarioDB], tags=["admin"])
def listar_usuarios_demo(
    db: Session = Depends(SessionLocal),
    payload=Depends(verify_token)
):
    """Listar usuarios que están en tenant demo esperando asignación"""
    demo_tenant = get_or_create_demo_tenant(db)
    usuarios_demo = crud_usuario.get_by_tenant(db, tenant_id=demo_tenant.id)
    return usuarios_demo

@router.put("/admin/usuarios/{usuario_id}/asignar-tenant", response_model=UsuarioDB, tags=["admin"])
def asignar_tenant_a_usuario(
    usuario_id: str,
    usuario_update: UsuarioUpdate,
    db: Session = Depends(SessionLocal),
    payload=Depends(verify_token)
):
    """Asignar un usuario a un tenant específico (migración desde demo a empresa)"""
    # TODO: Verificar que el usuario es admin
    
    # Obtener usuario
    db_usuario = crud_usuario.get(db, id=usuario_id)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Verificar que el nuevo tenant existe
    if usuario_update.tenant_id:
        nuevo_tenant = crud_tenant.get(db, id=str(usuario_update.tenant_id))
        if not nuevo_tenant:
            raise HTTPException(status_code=404, detail="Tenant no encontrado")
        if not nuevo_tenant.activo:
            raise HTTPException(status_code=400, detail="Tenant inactivo")
    
    # Actualizar usuario
    usuario_actualizado = crud_usuario.update(db, db_obj=db_usuario, obj_in=usuario_update)
    
    print(f"✅ Usuario {usuario_actualizado.email} migrado a tenant: {nuevo_tenant.nombre} ({nuevo_tenant.id})")
    
    return usuario_actualizado

