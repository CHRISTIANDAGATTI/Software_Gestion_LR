from sqlalchemy import Column, Integer, String
from ..database.base_class import Base

class TipoOperacion(Base):
    __tablename__ = "tipo_operacion"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True, nullable=False)
