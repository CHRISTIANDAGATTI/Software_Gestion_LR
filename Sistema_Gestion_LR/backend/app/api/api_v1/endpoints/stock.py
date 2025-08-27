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
from app.core.tenant_deps import get_optional_tenant_id
from typing import List

router = APIRouter()

@router.get("/ping")
def ping(tenant_id: str = Depends(get_optional_tenant_id)):
    return {
        "message": "El módulo Stock está activo ✅",
        "tenant_context": tenant_id if tenant_id else "Sin tenant"
    }


# CATEGORIAS
@router.get("/categorias", response_model=List[categoria_schemas.Categoria])
def listar_categorias(
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_optional_tenant_id)
):
    """Listar categorías filtradas por tenant si está disponible"""
    categorias = categoria.get_multi(db)
    
    # Si hay tenant, filtrar solo las categorías de ese tenant
    if tenant_id:
        categorias = [cat for cat in categorias if str(cat.tenant_id) == tenant_id]
    
    return categorias

@router.post("/categorias", response_model=categoria_schemas.Categoria)
def crear_categoria(
    categoria_data: categoria_schemas.CategoriaCreate, 
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_optional_tenant_id)
):
    """Crear categoría asociada al tenant actual"""
    print(f"🔍 Datos recibidos: {categoria_data.dict()}")
    print(f"🏢 Tenant ID: {tenant_id}")
    
    # Si hay tenant, crear nuevo objeto con el tenant_id
    if tenant_id:
        categoria_dict = categoria_data.dict()
        categoria_dict['tenant_id'] = tenant_id
        categoria_data = categoria_schemas.CategoriaCreate(**categoria_dict)
    
    try:
        result = categoria.create(db, obj_in=categoria_data)
        print(f"✅ Categoría creada: {result.id} para tenant: {tenant_id}")
        return result
    except Exception as e:
        print(f"❌ Error al crear categoría: {e}")
        raise

@router.get("/categorias/{categoria_id}", response_model=categoria_schemas.Categoria)
def obtener_categoria(
    categoria_id: int, 
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_optional_tenant_id)
):
    """Obtener categoría por ID, verificando que pertenezca al tenant"""
    db_categoria = categoria.get(db, id=categoria_id)
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    # Verificar que la categoría pertenezca al tenant actual
    if tenant_id and str(db_categoria.tenant_id) != tenant_id:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    return db_categoria

@router.put("/categorias/{categoria_id}", response_model=categoria_schemas.Categoria)
def actualizar_categoria(
    categoria_id: int, 
    categoria_data: categoria_schemas.CategoriaCreate, 
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_optional_tenant_id)
):
    """Actualizar categoría verificando que pertenezca al tenant"""
    db_categoria = categoria.get(db, id=categoria_id)
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    # Verificar que la categoría pertenezca al tenant actual
    if tenant_id and str(db_categoria.tenant_id) != tenant_id:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    return categoria.update(db, db_obj=db_categoria, obj_in=categoria_data)

@router.delete("/categorias/{categoria_id}")
def eliminar_categoria(
    categoria_id: int, 
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_optional_tenant_id)
):
    """Eliminar categoría verificando que pertenezca al tenant"""
    db_categoria = categoria.get(db, id=categoria_id)
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    # Verificar que la categoría pertenezca al tenant actual
    if tenant_id and str(db_categoria.tenant_id) != tenant_id:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    # Verificar si hay productos asociados (filtrados por tenant también)
    productos_query = db.query(Producto).filter_by(categoria_id=categoria_id)
    if tenant_id:
        productos_query = productos_query.filter_by(tenant_id=tenant_id)
    
    productos_asociados = productos_query.count()
    if productos_asociados > 0:
        raise HTTPException(
            status_code=400, 
            detail="No se puede eliminar la categoría porque tiene productos asociados"
        )
    
    categoria.remove(db, id=categoria_id)
    return {"message": "Categoría eliminada exitosamente"}


# PRODUCTOS
@router.get("/productos", response_model=List[producto_schemas.Producto])
def listar_productos(
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_optional_tenant_id)
):
    """Listar productos filtrados por tenant si está disponible"""
    productos = producto.get_multi(db)
    
    # Si hay tenant, filtrar solo los productos de ese tenant
    if tenant_id:
        productos = [prod for prod in productos if str(prod.tenant_id) == tenant_id]
    
    return productos

@router.get("/productos/{producto_id}", response_model=producto_schemas.Producto)
def obtener_producto(
    producto_id: int, 
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_optional_tenant_id)
):
    """Obtener producto por ID, verificando que pertenezca al tenant"""
    db_producto = producto.get(db, id=producto_id)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # Verificar que el producto pertenezca al tenant actual
    if tenant_id and str(db_producto.tenant_id) != tenant_id:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    return db_producto

@router.post("/productos", response_model=producto_schemas.Producto)
def crear_producto(
    producto_data: producto_schemas.ProductoCreate, 
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_optional_tenant_id)
):
    """Crear producto asociado al tenant actual"""
    print(f"🔍 Datos de producto recibidos: {producto_data.dict()}")
    print(f"🏢 Tenant ID: {tenant_id}")
    
    # Si hay tenant, crear nuevo objeto con el tenant_id
    if tenant_id:
        producto_dict = producto_data.dict()
        producto_dict['tenant_id'] = tenant_id
        producto_data = producto_schemas.ProductoCreate(**producto_dict)
    
    try:
        result = producto.create(db, obj_in=producto_data)
        print(f"✅ Producto creado: {result.id} para tenant: {tenant_id}")
        return result
    except Exception as e:
        print(f"❌ Error al crear producto: {e}")
        raise

@router.put("/productos/{producto_id}", response_model=producto_schemas.Producto)
def actualizar_producto(
    producto_id: int, 
    producto_data: producto_schemas.ProductoCreate, 
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_optional_tenant_id)
):
    """Actualizar producto verificando que pertenezca al tenant"""
    db_producto = producto.get(db, id=producto_id)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # Verificar que el producto pertenezca al tenant actual
    if tenant_id and str(db_producto.tenant_id) != tenant_id:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    return producto.update(db, db_obj=db_producto, obj_in=producto_data)

@router.delete("/productos/{producto_id}")
def eliminar_producto(
    producto_id: int, 
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_optional_tenant_id)
):
    """Eliminar producto verificando que pertenezca al tenant"""
    db_producto = producto.get(db, id=producto_id)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # Verificar que el producto pertenezca al tenant actual
    if tenant_id and str(db_producto.tenant_id) != tenant_id:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    producto.remove(db, id=producto_id)
    return {"message": "Producto eliminado exitosamente"}

# OPERACIONES DE INVENTARIO
@router.post("/operaciones_inventario", response_model=operacion_schemas.OperacionInventario)
def registrar_operacion_inventario(
    operacion: operacion_schemas.OperacionInventarioCreate,
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_optional_tenant_id)
):
    """Registrar operación de inventario asociada al tenant actual"""
    print(f"🔍 Datos de operación recibidos: {operacion.dict()}")
    print(f"🏢 Tenant ID: {tenant_id}")
    
    # Si hay tenant, crear nuevo objeto con el tenant_id
    if tenant_id:
        operacion_dict = operacion.dict()
        operacion_dict['tenant_id'] = tenant_id
        operacion = operacion_schemas.OperacionInventarioCreate(**operacion_dict)
    
    try:
        result = operacion_inventario.create(db, obj_in=operacion)
        print(f"✅ Operación de inventario creada: {result.id} para tenant: {tenant_id}")
        return result
    except Exception as e:
        print(f"❌ Error al crear operación de inventario: {e}")
        raise

@router.get("/operaciones_inventario", response_model=List[operacion_schemas.OperacionInventario])
def listar_operaciones_inventario(
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_optional_tenant_id)
):
    """Listar operaciones de inventario filtradas por tenant si está disponible"""
    operaciones = operacion_inventario.get_multi(db)
    
    # Si hay tenant, filtrar solo las operaciones de ese tenant
    if tenant_id:
        operaciones = [operacion for operacion in operaciones if str(operacion.tenant_id) == tenant_id]
    
    return operaciones

@router.get("/operaciones_inventario/{id}", response_model=operacion_schemas.OperacionInventario)
def obtener_operacion_inventario(
    id: int, 
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_optional_tenant_id)
):
    """Obtener operación de inventario por ID, verificando que pertenezca al tenant"""
    operacion = operacion_inventario.get(db, id=id)
    if not operacion:
        raise HTTPException(status_code=404, detail="Operación de inventario no encontrada")
    
    # Verificar que la operación pertenezca al tenant actual
    if tenant_id and str(operacion.tenant_id) != tenant_id:
        raise HTTPException(status_code=404, detail="Operación de inventario no encontrada")
    
    return operacion




