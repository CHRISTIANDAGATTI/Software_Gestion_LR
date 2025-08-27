from typing import List, Optional
from sqlalchemy.orm import Session
from app.schemas.tenant import TenantCreate, TenantUpdate
from app.models.tenant import Tenant


class CRUDTenant:
    def get(self, db: Session, *, id: str) -> Optional[Tenant]:
        return db.query(Tenant).filter(Tenant.id == id).first()

    def get_by_slug(self, db: Session, *, slug: str) -> Optional[Tenant]:
        return db.query(Tenant).filter(Tenant.slug == slug).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Tenant]:
        return db.query(Tenant).filter(Tenant.activo == True).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: TenantCreate) -> Tenant:
        db_obj = Tenant(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: Tenant, obj_in: TenantUpdate) -> Tenant:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: str) -> Tenant:
        obj = db.query(Tenant).get(id)
        db.delete(obj)
        db.commit()
        return obj


tenant = CRUDTenant()