from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.crud.tipo_operacion import tipo_operacion
from app.schemas.tipo_operacion import TipoOperacion, TipoOperacionCreate
from typing import List

router = APIRouter()

@router.get("/tipos_operacion", response_model=List[TipoOperacion])
def listar_tipos_operacion(db: Session = Depends(get_db)):
    # Crear tipos predefinidos si no existen
    tipo_operacion.crear_tipos_predefinidos_si_no_existen(db)
    return tipo_operacion.get_multi(db)

@router.post("/tipos_operacion", response_model=TipoOperacion)
def crear_tipo_operacion(tipo_data: TipoOperacionCreate, db: Session = Depends(get_db)):
    return tipo_operacion.create(db, obj_in=tipo_data)

@router.get("/tipos_operacion/{tipo_id}", response_model=TipoOperacion)
def obtener_tipo_operacion(tipo_id: int, db: Session = Depends(get_db)):
    return tipo_operacion.get(db, id=tipo_id)
