from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database.session import get_db
from app.core.tenant_deps import get_optional_tenant_id

router = APIRouter()

@router.get("/tipos_operacion", response_model=List[dict])
def listar_tipos_operacion(
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_optional_tenant_id)
):
    """Listar todos los tipos de operación disponibles filtrados por tenant si está disponible"""
    
    if tenant_id:
        # Query filtrando por tenant_id
        result = db.execute(
            text("SELECT id, nombre FROM tipo_operacion WHERE tenant_id = :tenant_id ORDER BY id"),
            {"tenant_id": tenant_id}
        )
    else:
        # Query sin filtro de tenant (compatibilidad hacia atrás)
        result = db.execute(text("SELECT id, nombre FROM tipo_operacion ORDER BY id"))
    
    tipos = result.fetchall()
    
    return [{"id": tipo.id, "nombre": tipo.nombre} for tipo in tipos]