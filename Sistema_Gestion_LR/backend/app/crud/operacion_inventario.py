from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.operacion_inventario import OperacionInventario
from app.models.producto import Producto
from app.schemas.operacion_inventario import OperacionInventarioCreate
from fastapi import HTTPException

def get_operaciones(db: Session):
    return db.query(OperacionInventario).all()

def create_operacion(db: Session, operacion: OperacionInventarioCreate):
    # Crear la operación de inventario
    db_operacion = OperacionInventario(**operacion.dict())
    db.add(db_operacion)

    # Actualizar el stock del producto
    producto = db.query(Producto).filter(Producto.id == operacion.producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Obtener el tipo de operación
    tipo_op = db_operacion.tipo_operacion_id
    # Buscar el nombre del tipo de operación
    tipo_nombre = db.execute(
        text("SELECT nombre FROM tipo_operacion WHERE id = :id"), {"id": tipo_op}
    ).scalar()

    if tipo_nombre == "COMPRA":
        producto.cantidad += operacion.cantidad
    elif tipo_nombre == "VENTA":
        if producto.cantidad < operacion.cantidad:
            raise HTTPException(
                status_code=400,
                detail=f"Stock insuficiente. Disponible: {producto.cantidad}"
            )
        producto.cantidad -= operacion.cantidad
    elif tipo_nombre in ["Extravío", "Rotura", "Insumo en producción"]:
        if producto.cantidad < operacion.cantidad:
            raise HTTPException(
                status_code=400,
                detail=f"Stock insuficiente. Disponible: {producto.cantidad}"
            )
        producto.cantidad -= operacion.cantidad
    else:  # AJUSTE, RECUENTO
        producto.cantidad += operacion.cantidad  # Puede ser positivo o negativo

    db.commit()
    db.refresh(db_operacion)
    db.refresh(producto)  # Para obtener la cantidad actualizada

    return db_operacion
