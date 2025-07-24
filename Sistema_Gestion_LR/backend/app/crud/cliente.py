from sqlalchemy.orm import Session
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate

class CRUDCliente:
    def get(self, db: Session, id: int):
        return db.query(Cliente).filter(Cliente.id == id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(Cliente).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: ClienteCreate):
        db_obj = Cliente(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: Cliente, obj_in: ClienteUpdate):
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
