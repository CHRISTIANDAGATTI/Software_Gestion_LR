from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate
from uuid import UUID

class CRUDUsuario:
    def get_by_supabase_user_id(self, db: Session, supabase_user_id: UUID) -> Usuario | None:
        return db.query(Usuario).filter(Usuario.supabase_user_id == supabase_user_id).first()

    def create(self, db: Session, obj_in: UsuarioCreate) -> Usuario:
        db_obj = Usuario(
            supabase_user_id=obj_in.supabase_user_id,
            nombre=obj_in.nombre,
            email=obj_in.email
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

crud_usuario = CRUDUsuario()
