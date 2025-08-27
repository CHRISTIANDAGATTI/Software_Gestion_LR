from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database.base_class import Base
from sqlalchemy.orm import relationship
import uuid

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(String(255), nullable=True)
    tenant_id = Column(UUID(as_uuid=True), nullable=True)  # NULL temporal hasta configurar tenants
    fecha_creado = Column(DateTime(timezone=True), server_default=func.now())

    # Relación con Categoria
    productos = relationship("Producto", back_populates="categoria")

