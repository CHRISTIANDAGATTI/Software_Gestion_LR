from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid
from app.schemas.categoria import Categoria  #  Importar Categoria

class ProductoBase(BaseModel):
    codigo: str
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    cantidad: int
    categoria_id: int
    tenant_id: Optional[uuid.UUID] = None  # UUID para multitenancy

class ProductoCreate(ProductoBase):
    pass

class Producto(ProductoBase):
    id: int
    fecha_creado: datetime
    categoria: Optional[Categoria] = None  # Relación con categoría

    class Config:
        from_attributes = True
