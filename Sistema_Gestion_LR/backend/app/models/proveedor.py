from sqlalchemy import Column, Integer, String
from app.database.base_class import Base

class Proveedor(Base):
    __tablename__ = "proveedores"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=True)
    razon_social = Column(String(100), nullable=True)
    cuit = Column(String(20), nullable=True, unique=True)
    dni = Column(String(20), nullable=True, unique=True)
    condicion_fiscal = Column(String(50), nullable=True)
    telefono = Column(String(30), nullable=True)
    email = Column(String(100), nullable=True)
    direccion = Column(String(200), nullable=True)
    localidad = Column(String(100), nullable=True)
    provincia = Column(String(100), nullable=True)
    observaciones = Column(String(300), nullable=True)
    tenant_id = Column(Integer, nullable=False)
