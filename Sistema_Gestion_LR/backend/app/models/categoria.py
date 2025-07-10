from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database.base_class import Base
from sqlalchemy.orm import relationship

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(String(255), nullable=True)
    fecha_creado = Column(DateTime(timezone=True), server_default=func.now())

    # Relación con Categoria
    productos = relationship("Producto", back_populates="categoria")

