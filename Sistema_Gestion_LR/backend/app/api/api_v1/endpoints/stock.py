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

# CATEGORIAS
@router.get("/categorias", response_model=list[schemas.Categoria])
def listar_categorias(db: Session = Depends(get_db)):
    return crud.get_categorias(db)


@router.post("/categorias", response_model=schemas.Categoria)
def crear_categoria(categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    return crud.create_categoria(db, categoria)


# PRODUCTOS

# Obtener todos los productos
@router.get("/productos", response_model=list[schemas.producto.Producto])
def listar_productos(db: Session = Depends(get_db)):
    return crud.producto.get_productos(db)

# Obtener un producto por ID
@router.get("/productos/{producto_id}", response_model=schemas.producto.Producto)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = crud.producto.get_producto(db, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.post("/productos", response_model=schemas.Producto)
def crear_producto(producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    return crud.create_producto(db, producto)

@router.put("/productos/{producto_id}", response_model=schemas.producto.Producto)
def actualizar_producto(producto_id: int, producto: schemas.producto.ProductoUpdate, db: Session = Depends(get_db)):
    return crud.producto.update_producto(db, producto_id, producto)


@router.delete("/productos/{producto_id}", response_model=None)
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    eliminado = crud.producto.delete_producto(db, producto_id)
    if not eliminado:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"ok": True}




