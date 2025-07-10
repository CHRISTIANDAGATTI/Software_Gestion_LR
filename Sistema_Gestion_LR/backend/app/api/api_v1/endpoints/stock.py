from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app import crud, schemas

router = APIRouter()

@router.get("/ping")
def ping():
    return {"message": "El módulo Stock está activo ✅"}

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 📦 Categorías
@router.get("/categorias", response_model=list[schemas.Categoria])
def listar_categorias(db: Session = Depends(get_db)):
    return crud.get_categorias(db)

@router.post("/categorias", response_model=schemas.Categoria)
def crear_categoria(categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    return crud.create_categoria(db, categoria)

# 📦 Productos
@router.get("/productos", response_model=list[schemas.producto.Producto])
def listar_productos(db: Session = Depends(get_db)):
    return crud.producto.get_productos(db)

@router.post("/productos", response_model=schemas.Producto)
def crear_producto(producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    return crud.create_producto(db, producto)

@router.put("/productos/{producto_id}", response_model=schemas.producto.Producto)
def actualizar_producto(producto_id: int, producto: schemas.producto.ProductoUpdate, db: Session = Depends(get_db)):
    return crud.producto.update_producto(db, producto_id, producto)




