from sqlalchemy import Column, String, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.base_class import Base
import uuid
import enum

class UserStatus(str, enum.Enum):
    PENDING = "pending"      # Registrado, esperando aprobación
    ACTIVE = "active"        # Aprobado y activo
    INACTIVE = "inactive"    # Desactivado

class UserRole(str, enum.Enum):
    ADMIN = "admin"          # Administrador de empresa
    USER = "user"            # Usuario normal

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    supabase_user_id = Column(UUID(as_uuid=True), nullable=False, unique=True)
    nombre = Column(String(100))
    email = Column(String(100), nullable=False)
    status = Column(Enum(UserStatus), default=UserStatus.PENDING)
    role = Column(Enum(UserRole), default=UserRole.USER)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relación con Tenant - comentada temporalmente
    # tenant = relationship("Tenant", back_populates="usuarios")
