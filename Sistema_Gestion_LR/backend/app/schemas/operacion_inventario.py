from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
import uuid

class OperacionInventarioBase(BaseModel):
    producto_id: int
    tipo_operacion_id: int  # Relación con tipo_operacion
    cantidad: int
    observaciones: Optional[str] = None
    fecha: Optional[datetime] = None
    tenant_id: Optional[uuid.UUID] = None

class OperacionInventarioCreate(OperacionInventarioBase):
    pass

class OperacionInventario(OperacionInventarioBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
