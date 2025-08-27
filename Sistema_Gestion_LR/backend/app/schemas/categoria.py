from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

class CategoriaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    tenant_id: Optional[uuid.UUID] = None  # UUID para multitenancy

class CategoriaCreate(CategoriaBase):
    pass
   
class Categoria(CategoriaBase):
    id: int
    fecha_creado: datetime

    class Config:
        from_attributes = True
