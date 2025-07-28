from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

class UsuarioBase(BaseModel):
    nombre: str | None = None
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    supabase_user_id: UUID

class UsuarioDB(UsuarioBase):
    id: UUID
    supabase_user_id: UUID
    fecha_creacion: datetime

    class Config:
        orm_mode = True
