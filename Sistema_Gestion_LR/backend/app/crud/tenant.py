from sqlalchemy.orm import Session
from app.models.tenant import Tenant
from app.schemas.tenant import TenantCreate, TenantUpdate

class CRUDTenant:
    def get(self, db: Session, id: str):
        return db.query(Tenant).filter(Tenant.id == id).first()
    
    def get_by_cuit(self, db: Session, cuit: str):
        return db.query(Tenant).filter(Tenant.cuit == cuit).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(Tenant).filter(Tenant.activo == True).offset(skip).limit(limit).all()
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100):
        """Obtener todos los tenants (para admin)"""
        return db.query(Tenant).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: TenantCreate):
        db_obj = Tenant(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: Tenant, obj_in: TenantUpdate):
        obj_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            setattr(db_obj, field, obj_data[field])
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def habilitar(self, db: Session, db_obj: Tenant):
        """Habilitar tenant"""
        db_obj.habilitada = True
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def deshabilitar(self, db: Session, db_obj: Tenant):
        """Deshabilitar tenant (soft delete)"""
        db_obj.habilitada = False
        db.commit()
        db.refresh(db_obj)
        return db_obj

tenant = CRUDTenant()
