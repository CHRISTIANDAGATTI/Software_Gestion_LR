from fastapi import APIRouter, Depends, HTTPException
from app.models.operacion_inventario import OperacionInventario
from sqlalchemy.orm import Session
from app.database.session import get_db
from app import crud, schemas
from app.models.producto import Producto
from app.models.operacion_inventario import OperacionInventario
from app.schemas.operacion_inventario import OperacionInventarioCreate, OperacionInventario as OperacionInventarioSchema
from app.crud import operacion_inventario as crud_operacion

router = APIRouter()

@router.get("/ping")
def ping():
    return {"message": "El módulo Stock está activo ✅"}


# CATEGORIAS
@router.get("/categorias", response_model=list[schemas.Categoria])
def listar_categorias(db: Session = Depends(get_db)):
    return crud.get_categorias(db)



@router.post("/categorias", response_model=schemas.Categoria)
def crear_categoria(categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    return crud.create_categoria(db, categoria)

@router.put("/categorias/{categoria_id}", response_model=schemas.Categoria)
def actualizar_categoria(categoria_id: int, categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    db_categoria = crud.get_categoria(db, categoria_id)
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    db_categoria.nombre = categoria.nombre
    db_categoria.descripcion = categoria.descripcion
    db.commit()
    db.refresh(db_categoria)
    return db_categoria


# Eliminar categoría con validación de productos asociados
@router.delete("/categorias/{categoria_id}", response_model=None)
def eliminar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    db_categoria = crud.get_categoria(db, categoria_id)
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    # Verificar si hay productos asociados a la categoría
    productos_asociados = db.query(Producto).filter_by(categoria_id=categoria_id).count()
    if productos_asociados > 0:
        raise HTTPException(status_code=400, detail="No se puede eliminar la categoría porque tiene productos asociados")
    # Eliminar la categoría
    eliminado = crud.delete_categoria(db, categoria_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="No se pudo eliminar la categoría")
    return {"ok": True}


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
    # Forzar stock inicial en 0
    producto_dict = producto.dict()
    producto_dict["stock"] = 0
    return crud.create_producto(db, schemas.ProductoCreate(**producto_dict))

@router.put("/productos/{producto_id}", response_model=schemas.producto.Producto)
def actualizar_producto(producto_id: int, producto: schemas.producto.ProductoUpdate, db: Session = Depends(get_db)):
    return crud.producto.update_producto(db, producto_id, producto)


@router.delete("/productos/{producto_id}", response_model=None)
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    # Verificar si hay operaciones asociadas al producto
    operaciones_asociadas = db.query(OperacionInventario).filter_by(producto_id=producto_id).count()
    if operaciones_asociadas > 0:
        raise HTTPException(status_code=400, detail="No se puede eliminar el producto porque tiene operaciones asociadas")
    eliminado = crud.producto.delete_producto(db, producto_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"ok": True}

# OPERACIONES DE INVENTARIO
@router.post("/operaciones_inventario", response_model=OperacionInventarioSchema)
def registrar_operacion_inventario(
    operacion: OperacionInventarioCreate,
    db: Session = Depends(get_db)
):
    return crud_operacion.create_operacion(db, operacion)




