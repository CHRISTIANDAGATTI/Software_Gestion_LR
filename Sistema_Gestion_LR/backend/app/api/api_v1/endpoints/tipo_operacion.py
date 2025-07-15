from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.crud.tipo_operacion import get_tipos_operacion, crear_tipos_operacion_si_no_existen
from app.schemas.tipo_operacion import TipoOperacion

router = APIRouter()

@router.get("/tipos_operacion", response_model=list[TipoOperacion])
def listar_tipos_operacion(db: Session = Depends(get_db)):
    crear_tipos_operacion_si_no_existen(db)
    return get_tipos_operacion(db)
