from sqlalchemy.orm import Session
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteBase

class CRUDCliente:
    def get(self, db: Session, id: int):
        return db.query(Cliente).filter(Cliente.id == id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(Cliente).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: ClienteBase):
        data = obj_in.dict()
        # Convertir cadenas vacías en None para cuit y dni
        for campo in ["cuit", "dni"]:
            if campo in data and (data[campo] is not None) and (data[campo] == ""):
                data[campo] = None
        db_obj = Cliente(**data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: Cliente, obj_in: ClienteBase):
        for field, value in obj_in.dict(exclude_unset=True).items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, id: int):
        obj = db.query(Cliente).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

cliente = CRUDCliente()
