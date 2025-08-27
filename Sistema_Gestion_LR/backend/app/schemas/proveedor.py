from pydantic import BaseModel, EmailStr, Field
from typing import Optional

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
    tenant_id: int

class ProveedorInDBBase(ProveedorBase):
    id: int

    class Config:
        orm_mode = True

class Proveedor(ProveedorInDBBase):
    pass
