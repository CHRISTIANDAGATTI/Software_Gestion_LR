from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from uuid import UUID
from typing import List, Optional

class CRUDUsuario:
    def get(self, db: Session, *, id: str) -> Optional[Usuario]:
        """Obtener usuario por ID"""
        return db.query(Usuario).filter(Usuario.id == id).first()
    
    def get_by_supabase_user_id(self, db: Session, supabase_user_id: UUID) -> Usuario | None:
        """Obtener usuario por Supabase user ID"""
        return db.query(Usuario).filter(Usuario.supabase_user_id == supabase_user_id).first()
    
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Usuario]:
        """Obtener múltiples usuarios"""
        return db.query(Usuario).offset(skip).limit(limit).all()
    
    def get_by_tenant(self, db: Session, *, tenant_id: UUID) -> List[Usuario]:
        """Obtener usuarios por tenant"""
        return db.query(Usuario).filter(Usuario.tenant_id == tenant_id).all()

    def create(self, db: Session, obj_in: UsuarioCreate) -> Usuario:
        """Crear nuevo usuario"""
        db_obj = Usuario(
            supabase_user_id=obj_in.supabase_user_id,
            nombre=obj_in.nombre,
            email=obj_in.email,
            tenant_id=obj_in.tenant_id  # Ahora obligatorio
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(self, db: Session, *, db_obj: Usuario, obj_in: UsuarioUpdate) -> Usuario:
        """Actualizar usuario (principalmente para cambio de tenant)"""
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

crud_usuario = CRUDUsuario()
