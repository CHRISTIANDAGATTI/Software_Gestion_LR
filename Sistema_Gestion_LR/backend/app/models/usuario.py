from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.base_class import Base
import uuid

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    supabase_user_id = Column(UUID(as_uuid=True), nullable=False, unique=True)
    nombre = Column(String(100))
    email = Column(String(100), nullable=False)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)  # Obligatorio
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relación con tenant
    tenant = relationship("Tenant", back_populates="usuarios")
