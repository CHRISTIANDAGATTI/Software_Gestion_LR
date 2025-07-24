from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.proveedor import Proveedor, ProveedorCreate, ProveedorUpdate
from app import crud
from app.database.session import get_db

router = APIRouter()

@router.get("/proveedores", response_model=List[Proveedor])
def listar_proveedores(db: Session = Depends(get_db)):
    return crud.proveedor.get_multi(db)

@router.get("/proveedores/{id}", response_model=Proveedor)
def obtener_proveedor(id: int, db: Session = Depends(get_db)):
    proveedor = crud.proveedor.get(db, id)
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return proveedor

@router.post("/proveedores", response_model=Proveedor)
def crear_proveedor(proveedor_in: ProveedorCreate, db: Session = Depends(get_db)):
    return crud.proveedor.create(db, proveedor_in)

@router.put("/proveedores/{id}", response_model=Proveedor)
def actualizar_proveedor(id: int, proveedor_in: ProveedorUpdate, db: Session = Depends(get_db)):
    db_proveedor = crud.proveedor.get(db, id)
    if not db_proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return crud.proveedor.update(db, db_proveedor, proveedor_in)

@router.delete("/proveedores/{id}", response_model=Proveedor)
def eliminar_proveedor(id: int, db: Session = Depends(get_db)):
    db_proveedor = crud.proveedor.get(db, id)
    if not db_proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return crud.proveedor.remove(db, id)
