from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.cliente import Cliente, ClienteBase
from app import crud
from app.database.session import get_db

router = APIRouter()

@router.get("/clientes", response_model=List[Cliente])
def listar_clientes(db: Session = Depends(get_db)):
    return crud.cliente.get_multi(db)

@router.get("/clientes/{id}", response_model=Cliente)
def obtener_cliente(id: int, db: Session = Depends(get_db)):
    cliente = crud.cliente.get(db, id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@router.post("/clientes", response_model=Cliente)
def crear_cliente(cliente_in: ClienteBase, db: Session = Depends(get_db)):
    return crud.cliente.create(db, cliente_in)

@router.put("/clientes/{id}", response_model=Cliente)
def actualizar_cliente(id: int, cliente_in: ClienteBase, db: Session = Depends(get_db)):
    db_cliente = crud.cliente.get(db, id)
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return crud.cliente.update(db, db_cliente, cliente_in)

@router.delete("/clientes/{id}", response_model=Cliente)
def eliminar_cliente(id: int, db: Session = Depends(get_db)):
    db_cliente = crud.cliente.get(db, id)
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return crud.cliente.remove(db, id)
