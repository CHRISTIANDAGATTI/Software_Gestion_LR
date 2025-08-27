from sqlalchemy.orm import Session
from app.models.categoria import Categoria
from app.schemas.categoria import CategoriaCreate

class CRUDCategoria:
    def get(self, db: Session, id: int):
        return db.query(Categoria).filter(Categoria.id == id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(Categoria).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: CategoriaCreate):
        db_obj = Categoria(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: Categoria, obj_in: CategoriaCreate):
        obj_data = obj_in.dict()
        for field in obj_data:
            setattr(db_obj, field, obj_data[field])
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, id: int):
        obj = db.query(Categoria).get(id)
        db.delete(obj)
        db.commit()
        return obj

categoria = CRUDCategoria()
