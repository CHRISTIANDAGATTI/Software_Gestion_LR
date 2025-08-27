from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.crud.tenant import tenant
from app.schemas import tenant as tenant_schemas

router = APIRouter()

@router.get("/tenants", response_model=List[tenant_schemas.Tenant])
def listar_tenants(db: Session = Depends(get_db)):
    """Listar todas las empresas activas"""
    return tenant.get_multi(db)

@router.post("/tenants", response_model=tenant_schemas.Tenant)
def crear_tenant(tenant_data: tenant_schemas.TenantCreate, db: Session = Depends(get_db)):
    """Crear nueva empresa"""
    # Verificar que el slug no exista
    existing = tenant.get_by_slug(db, slug=tenant_data.slug)
    if existing:
        raise HTTPException(status_code=400, detail="Ya existe una empresa con ese slug")
    
    return tenant.create(db, obj_in=tenant_data)

@router.get("/tenants/{tenant_id}", response_model=tenant_schemas.Tenant)
def obtener_tenant(tenant_id: str, db: Session = Depends(get_db)):
    """Obtener empresa por ID"""
    db_tenant = tenant.get(db, id=tenant_id)
    if not db_tenant:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return db_tenant

@router.get("/tenants/slug/{slug}", response_model=tenant_schemas.Tenant)
def obtener_tenant_por_slug(slug: str, db: Session = Depends(get_db)):
    """Obtener empresa por slug"""
    db_tenant = tenant.get_by_slug(db, slug=slug)
    if not db_tenant:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return db_tenant

@router.put("/tenants/{tenant_id}", response_model=tenant_schemas.Tenant)
def actualizar_tenant(
    tenant_id: str, 
    tenant_data: tenant_schemas.TenantUpdate, 
    db: Session = Depends(get_db)
):
    """Actualizar empresa"""
    db_tenant = tenant.get(db, id=tenant_id)
    if not db_tenant:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return tenant.update(db, db_obj=db_tenant, obj_in=tenant_data)

@router.delete("/tenants/{tenant_id}")
def eliminar_tenant(tenant_id: str, db: Session = Depends(get_db)):
    """Desactivar empresa (soft delete)"""
    db_tenant = tenant.get(db, id=tenant_id)
    if not db_tenant:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return tenant.remove(db, id=tenant_id)
