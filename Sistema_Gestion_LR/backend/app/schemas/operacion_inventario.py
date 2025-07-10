from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OperacionInventarioBase(BaseModel):
    producto_id: int
    tipo: str  # COMPRA, VENTA, AJUSTE
    cantidad: int
    observaciones: Optional[str] = None

class OperacionInventarioCreate(OperacionInventarioBase):
    pass

class OperacionInventario(OperacionInventarioBase):
    id: int
    fecha: datetime

    class Config:
        orm_mode = True
