from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import uuid

class ProveedorBase(BaseModel):
    nombre: Optional[str] = None
    razon_social: Optional[str] = None
    cuit: Optional[str] = None
    dni: Optional[str] = None
    condicion_fiscal: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None
    direccion: Optional[str] = None
    localidad: Optional[str] = None
    provincia: Optional[str] = None
    observaciones: Optional[str] = None
    tenant_id: Optional[uuid.UUID] = None  # UUID para multitenancy

class ProveedorCreate(ProveedorBase):
    pass

class ProveedorInDBBase(ProveedorBase):
    id: int

    class Config:
        from_attributes = True

class Proveedor(ProveedorInDBBase):
    pass
