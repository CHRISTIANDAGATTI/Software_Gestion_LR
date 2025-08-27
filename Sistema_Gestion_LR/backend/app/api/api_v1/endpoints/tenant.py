from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.crud.tenant import tenant
from app.schemas.tenant import Tenant, TenantCreate, TenantUpdate
from app.core.tenant_deps import get_current_tenant_id, get_current_tenant_obj, get_optional_tenant_id

router = APIRouter()

@router.get("/tenant/current")
def obtener_tenant_actual(
    tenant_id: str = Depends(get_current_tenant_id),
    tenant_obj: Tenant = Depends(get_current_tenant_obj)
):
    """Obtener información del tenant actual del contexto"""
    return {
        "tenant_id": tenant_id,
        "tenant": tenant_obj,
        "message": f"Contexto actual configurado para: {tenant_obj.nombre}"
    }

@router.get("/tenant/context")
def verificar_contexto():
    """Verificar si hay un tenant en el contexto (opcional)"""
    tenant_id = get_optional_tenant_id()
    return {
        "has_tenant": tenant_id is not None,
        "tenant_id": tenant_id,
        "message": "Tenant detectado" if tenant_id else "No hay tenant en el contexto"
    }

@router.get("/tenants", response_model=List[Tenant])
def listar_tenants(db: Session = Depends(get_db)):
    """Listar todos los tenants activos"""
    return tenant.get_multi(db)

@router.post("/tenants", response_model=Tenant)
def crear_tenant(tenant_data: TenantCreate, db: Session = Depends(get_db)):
    """Crear un nuevo tenant"""
    # Verificar que el slug no exista
    if tenant.get_by_slug(db, slug=tenant_data.slug):
        raise HTTPException(status_code=400, detail="Slug already exists")
    
    return tenant.create(db, obj_in=tenant_data)

@router.get("/tenants/{tenant_id}", response_model=Tenant)
def obtener_tenant(tenant_id: str, db: Session = Depends(get_db)):
    """Obtener un tenant por ID"""
    db_tenant = tenant.get(db, id=tenant_id)
    if not db_tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return db_tenant

@router.get("/tenants/slug/{slug}", response_model=Tenant)
def obtener_tenant_por_slug(slug: str, db: Session = Depends(get_db)):
    """Obtener un tenant por slug"""
    db_tenant = tenant.get_by_slug(db, slug=slug)
    if not db_tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return db_tenant

@router.put("/tenants/{tenant_id}", response_model=Tenant)
def actualizar_tenant(tenant_id: str, tenant_data: TenantUpdate, db: Session = Depends(get_db)):
    """Actualizar un tenant"""
    db_tenant = tenant.get(db, id=tenant_id)
    if not db_tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    return tenant.update(db, db_obj=db_tenant, obj_in=tenant_data)