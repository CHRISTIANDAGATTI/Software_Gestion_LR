from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional

class UsuarioBase(BaseModel):
    nombre: str | None = None
    email: EmailStr
    tenant_id: UUID  # Obligatorio, no opcional

class UsuarioCreate(UsuarioBase):
    supabase_user_id: UUID

class UsuarioUpdate(BaseModel):
    """Schema para actualización de usuario (principalmente para cambio de tenant)"""
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    tenant_id: Optional[UUID] = None

class UsuarioDB(UsuarioBase):
    id: UUID
    supabase_user_id: UUID
    fecha_creacion: datetime

    class Config:
        from_attributes = True
