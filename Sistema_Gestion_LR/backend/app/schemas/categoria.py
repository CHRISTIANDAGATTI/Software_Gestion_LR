from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CategoriaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class CategoriaCreate(CategoriaBase):
    pass
   
class Categoria(CategoriaBase):
    id: int
    fecha_creado: datetime

    class Config:
        orm_mode = True
