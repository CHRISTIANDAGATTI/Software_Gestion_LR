from sqlalchemy.orm import Session
from app.models.proveedor import Proveedor
from app.schemas.proveedor import ProveedorCreate, ProveedorUpdate

class CRUDProveedor:
    def get(self, db: Session, id: int):
        return db.query(Proveedor).filter(Proveedor.id == id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(Proveedor).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: ProveedorCreate):
        db_obj = Proveedor(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: Proveedor, obj_in: ProveedorUpdate):
        for field, value in obj_in.dict(exclude_unset=True).items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, id: int):
        obj = db.query(Proveedor).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

proveedor = CRUDProveedor()
