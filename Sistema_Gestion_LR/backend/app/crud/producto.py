from sqlalchemy.orm import Session
from app.models.producto import Producto
from app.schemas.producto import ProductoCreate

class CRUDProducto:
    def get(self, db: Session, id: int):
        return db.query(Producto).filter(Producto.id == id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(Producto).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: ProductoCreate):
        db_obj = Producto(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: Producto, obj_in: ProductoCreate):
        obj_data = obj_in.dict()
        for field in obj_data:
            setattr(db_obj, field, obj_data[field])
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, id: int):
        obj = db.query(Producto).get(id)
        db.delete(obj)
        db.commit()
        return obj

producto = CRUDProducto()

