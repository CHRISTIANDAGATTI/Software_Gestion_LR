"""
Contexto y utilidades para manejo de multitenancy
"""
from contextvars import ContextVar
from typing import Optional
import uuid

# Variable de contexto para el tenant actual
current_tenant: ContextVar[Optional[str]] = ContextVar('current_tenant', default=None)

def get_current_tenant() -> Optional[str]:
    """Obtiene el tenant_id del contexto actual"""
    return current_tenant.get()

def set_current_tenant(tenant_id: str) -> None:
    """Establece el tenant_id en el contexto actual"""
    current_tenant.set(tenant_id)

def clear_current_tenant() -> None:
    """Limpia el tenant del contexto actual"""
    current_tenant.set(None)

def validate_tenant_id(tenant_id: str) -> bool:
    """Valida que el tenant_id sea un UUID válido"""
    try:
        uuid.UUID(tenant_id)
        return True
    except (ValueError, TypeError):
        return False
