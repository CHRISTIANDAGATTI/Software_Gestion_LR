from sqlalchemy.orm import Session
from ..models.tipo_operacion import TipoOperacion

TIPOS_PREDEFINIDOS = [
    "Compra",
    "Venta",
    "Rotura",
    "Recuento",
    "Extravío",
    "Insumo en producción"
]

def get_tipos_operacion(db: Session):
    return db.query(TipoOperacion).all()

def crear_tipos_operacion_si_no_existen(db: Session):
    for nombre in TIPOS_PREDEFINIDOS:
        if not db.query(TipoOperacion).filter_by(nombre=nombre).first():
            db.add(TipoOperacion(nombre=nombre))
    db.commit()
