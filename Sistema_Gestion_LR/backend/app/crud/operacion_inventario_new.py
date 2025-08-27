from sqlalchemy.orm import Session
from app.models.operacion_inventario import OperacionInventario
from app.schemas.operacion_inventario import OperacionInventarioCreate

class CRUDOperacionInventario:
    def get(self, db: Session, id: int):
        return db.query(OperacionInventario).filter(OperacionInventario.id == id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(OperacionInventario).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: OperacionInventarioCreate):
        db_obj = OperacionInventario(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, id: int):
        obj = db.query(OperacionInventario).get(id)
        db.delete(obj)
        db.commit()
        return obj

operacion_inventario = CRUDOperacionInventario()
