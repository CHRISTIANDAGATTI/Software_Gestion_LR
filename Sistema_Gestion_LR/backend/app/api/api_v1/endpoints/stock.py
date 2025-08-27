from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app import crud
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
    return crud.categoria.get_multi(db)

@router.post("/categorias", response_model=categoria_schemas.Categoria)
def crear_categoria(categoria: categoria_schemas.CategoriaCreate, db: Session = Depends(get_db)):
    print(f"🔍 Datos recibidos: {categoria.dict()}")
    try:
        result = crud.categoria.create(db, obj_in=categoria)
        print(f"✅ Categoría creada: {result.id}")
        return result
    except Exception as e:
        print(f"❌ Error al crear categoría: {e}")
        raise

@router.put("/categorias/{categoria_id}", response_model=categoria_schemas.Categoria)
def actualizar_categoria(
    categoria_id: int, 
    categoria: categoria_schemas.CategoriaCreate, 
    db: Session = Depends(get_db)
):
    db_categoria = crud.categoria.get(db, id=categoria_id)
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return crud.categoria.update(db, db_obj=db_categoria, obj_in=categoria)

@router.delete("/categorias/{categoria_id}")
def eliminar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    db_categoria = crud.categoria.get(db, id=categoria_id)
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    # Verificar si hay productos asociados
    productos_asociados = db.query(Producto).filter_by(categoria_id=categoria_id).count()
    if productos_asociados > 0:
        raise HTTPException(
            status_code=400, 
            detail="No se puede eliminar la categoría porque tiene productos asociados"
        )
    
    crud.categoria.remove(db, id=categoria_id)
    return {"message": "Categoría eliminada exitosamente"}


# PRODUCTOS
@router.get("/productos", response_model=List[producto_schemas.Producto])
def listar_productos(db: Session = Depends(get_db)):
    return crud.producto.get_multi(db)

@router.get("/productos/{producto_id}", response_model=producto_schemas.Producto)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = crud.producto.get(db, id=producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.post("/productos", response_model=producto_schemas.Producto)
def crear_producto(producto: producto_schemas.ProductoCreate, db: Session = Depends(get_db)):
    return crud.producto.create(db, obj_in=producto)

@router.put("/productos/{producto_id}", response_model=producto_schemas.Producto)
def actualizar_producto(
    producto_id: int, 
    producto: producto_schemas.ProductoCreate, 
    db: Session = Depends(get_db)
):
    db_producto = crud.producto.get(db, id=producto_id)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return crud.producto.update(db, db_obj=db_producto, obj_in=producto)

@router.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = crud.producto.get(db, id=producto_id)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    crud.producto.remove(db, id=producto_id)
    return {"message": "Producto eliminado exitosamente"}

# OPERACIONES DE INVENTARIO
@router.post("/operaciones_inventario", response_model=operacion_schemas.OperacionInventario)
def registrar_operacion_inventario(
    operacion: operacion_schemas.OperacionInventarioCreate,
    db: Session = Depends(get_db)
):
    return crud.operacion_inventario.create(db, obj_in=operacion)




