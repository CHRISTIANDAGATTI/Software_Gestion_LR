from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database.base_class import Base
import uuid

class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(100), nullable=False)
    slug = Column(String(50), nullable=False, unique=True, index=True)
    descripcion = Column(String(255), nullable=True)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones se agregarán después cuando todos los modelos estén listos
