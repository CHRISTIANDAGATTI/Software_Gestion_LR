from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional

class UsuarioBase(BaseModel):
    nombre: Optional[str] = None
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    supabase_user_id: UUID

class UsuarioDB(UsuarioBase):
    id: UUID
    supabase_user_id: UUID
    fecha_creacion: datetime

    class Config:
        from_attributes = True

    class Config:
        from_attributes = True
