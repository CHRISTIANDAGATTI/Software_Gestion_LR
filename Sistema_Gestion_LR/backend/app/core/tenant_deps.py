"""
Dependencias de FastAPI para multitenancy
"""
from typing import Optional
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.tenant_context import get_current_tenant
from app.database.session import get_db
from app.crud.tenant import tenant as tenant_crud
from app.models.tenant import Tenant


def get_current_tenant_id() -> str:
    """
    Dependencia que obtiene el tenant_id del contexto actual
    Lanza excepción si no hay tenant configurado
    """
    tenant_id = get_current_tenant()
    if not tenant_id:
        raise HTTPException(
            status_code=400, 
            detail="No tenant context available. Please specify tenant via subdomain or X-Tenant-ID header"
        )
    return tenant_id


def get_current_tenant_obj(
    tenant_id: str = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
) -> Tenant:
    """
    Dependencia que obtiene el objeto Tenant completo del contexto actual
    """
    tenant_obj = tenant_crud.get(db, id=tenant_id)
    if not tenant_obj:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant_obj


def get_optional_tenant_id() -> Optional[str]:
    """
    Dependencia que obtiene el tenant_id opcional (sin lanzar excepción)
    Útil para endpoints que pueden funcionar sin tenant
    """
    return get_current_tenant()
