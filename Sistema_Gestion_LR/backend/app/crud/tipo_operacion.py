from sqlalchemy.orm import Session
from app.models.tipo_operacion import TipoOperacion
from app.schemas.tipo_operacion import TipoOperacionCreate

TIPOS_PREDEFINIDOS = [
    "Compra",
    "Venta",
    "Rotura",
    "Recuento",
    "Extravío",
    "Insumo en producción"
]

class CRUDTipoOperacion:
    def get(self, db: Session, id: int):
        return db.query(TipoOperacion).filter(TipoOperacion.id == id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(TipoOperacion).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: TipoOperacionCreate):
        db_obj = TipoOperacion(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: TipoOperacion, obj_in: TipoOperacionCreate):
        for field, value in obj_in.dict(exclude_unset=True).items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, id: int):
        obj = db.query(TipoOperacion).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def crear_tipos_predefinidos_si_no_existen(self, db: Session):
        """Crear tipos de operación predefinidos si no existen"""
        for nombre in TIPOS_PREDEFINIDOS:
            if not db.query(TipoOperacion).filter_by(nombre=nombre).first():
                db.add(TipoOperacion(nombre=nombre))
        db.commit()

tipo_operacion = CRUDTipoOperacion()
