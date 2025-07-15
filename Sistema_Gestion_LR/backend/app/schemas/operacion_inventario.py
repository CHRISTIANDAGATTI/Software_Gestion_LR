from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OperacionInventarioBase(BaseModel):
    producto_id: int
    tipo_operacion_id: int  # Relación con tipo_operacion
    cantidad: int
    observaciones: Optional[str] = None
    fecha: Optional[datetime] = None

class OperacionInventarioCreate(OperacionInventarioBase):
    pass

class OperacionInventario(OperacionInventarioBase):
    id: int

    class Config:
        orm_mode = True
