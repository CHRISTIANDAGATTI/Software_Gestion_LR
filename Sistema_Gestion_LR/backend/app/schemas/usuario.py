from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional
from app.models.usuario import UserStatus, UserRole

class UsuarioBase(BaseModel):
    nombre: Optional[str] = None
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    supabase_user_id: UUID
    tenant_id: Optional[UUID] = None  # Se asigna después para usuarios demo

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    status: Optional[UserStatus] = None
    role: Optional[UserRole] = None
    tenant_id: Optional[UUID] = None

class UsuarioSimple(UsuarioBase):
    id: UUID
    status: UserStatus
    role: UserRole
    fecha_creacion: datetime

    class Config:
        from_attributes = True

class UsuarioDB(UsuarioSimple):
    supabase_user_id: UUID
    tenant_id: Optional[UUID] = None

    class Config:
        from_attributes = True
