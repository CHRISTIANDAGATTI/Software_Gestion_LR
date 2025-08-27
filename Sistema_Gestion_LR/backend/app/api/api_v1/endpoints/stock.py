from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.crud.categoria import categoria
from app.crud.producto import producto
from app.crud.operacion_inventario import operacion_inventario
from app.schemas import categoria as categoria_schemas
from app.schemas import producto as producto_schemas
from app.schemas import operacion_inventario as operacion_schemas
from app.models.producto import Producto
from typing import List

router = APIRouter()

@router.get("/ping")
def ping():
    return {"message": "El módulo Stock está activo ✅"}


# CATEGORIAS
@router.get("/categorias", response_model=List[categoria_schemas.Categoria])
def listar_categorias(db: Session = Depends(get_db)):
    return categoria.get_multi(db)

@router.post("/categorias", response_model=categoria_schemas.Categoria)
def crear_categoria(categoria_data: categoria_schemas.CategoriaCreate, db: Session = Depends(get_db)):
    return categoria.create(db, obj_in=categoria_data)

@router.put("/categorias/{categoria_id}", response_model=categoria_schemas.Categoria)
def actualizar_categoria(
    categoria_id: int, 
    categoria_data: categoria_schemas.CategoriaCreate, 
    db: Session = Depends(get_db)
):
    db_categoria = categoria.get(db, id=categoria_id)
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria.update(db, db_obj=db_categoria, obj_in=categoria_data)

@router.delete("/categorias/{categoria_id}")
def eliminar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    db_categoria = categoria.get(db, id=categoria_id)
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    # Verificar si hay productos asociados
    productos_asociados = db.query(Producto).filter_by(categoria_id=categoria_id).count()
    if productos_asociados > 0:
        raise HTTPException(
            status_code=400, 
            detail="No se puede eliminar la categoría porque tiene productos asociados"
        )
    
    categoria.remove(db, id=categoria_id)
    return {"message": "Categoría eliminada exitosamente"}


# PRODUCTOS
@router.get("/productos", response_model=List[producto_schemas.Producto])
def listar_productos(db: Session = Depends(get_db)):
    return producto.get_multi(db)

@router.get("/productos/{producto_id}", response_model=producto_schemas.Producto)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = producto.get(db, id=producto_id)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto

@router.post("/productos", response_model=producto_schemas.Producto)
def crear_producto(producto_data: producto_schemas.ProductoCreate, db: Session = Depends(get_db)):
    return producto.create(db, obj_in=producto_data)

@router.put("/productos/{producto_id}", response_model=producto_schemas.Producto)
def actualizar_producto(
    producto_id: int, 
    producto_data: producto_schemas.ProductoCreate, 
    db: Session = Depends(get_db)
):
    db_producto = producto.get(db, id=producto_id)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto.update(db, db_obj=db_producto, obj_in=producto_data)

@router.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = producto.get(db, id=producto_id)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    producto.remove(db, id=producto_id)
    return {"message": "Producto eliminado exitosamente"}

# OPERACIONES DE INVENTARIO
@router.post("/operaciones_inventario", response_model=operacion_schemas.OperacionInventario)
def registrar_operacion_inventario(
    operacion: operacion_schemas.OperacionInventarioCreate,
    db: Session = Depends(get_db)
):
    return operacion_inventario.create(db, obj_in=operacion)




