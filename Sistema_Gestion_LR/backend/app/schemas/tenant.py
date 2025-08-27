from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class TenantBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    slug: str = Field(..., min_length=1, max_length=50, pattern=r'^[a-z0-9-]+$')
    descripcion: Optional[str] = None
    activo: bool = True

class TenantCreate(TenantBase):
    pass

class TenantUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None

class Tenant(TenantBase):
    id: uuid.UUID
    fecha_creacion: datetime

    class Config:
        from_attributes = True