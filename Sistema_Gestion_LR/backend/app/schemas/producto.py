from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.categoria import Categoria  #  Importar Categoria

class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    cantidad: int
    categoria_id: int

class ProductoCreate(ProductoBase):
    pass

class Producto(ProductoBase):
    id: int
    fecha_creado: datetime
    categoria: Categoria | None  # Relación con categoría

class ProductoUpdate(BaseModel):
    nombre: Optional[str]
    descripcion: Optional[str]
    precio: Optional[float]
    cantidad: Optional[int]
    categoria_id: Optional[int]

    class Config:
        orm_mode = True
