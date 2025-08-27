from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.base_class import Base

class OperacionInventario(Base):
    __tablename__ = "operaciones_inventario"

    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    tipo_operacion_id = Column(Integer, ForeignKey("tipo_operacion.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    fecha = Column(DateTime(timezone=True), server_default=func.now())
    observaciones = Column(String(255), nullable=True)

    # Relaciones
    producto = relationship("Producto", back_populates="operaciones")
    # tipo_operacion = relationship("TipoOperacion")  # Comentado temporalmente
