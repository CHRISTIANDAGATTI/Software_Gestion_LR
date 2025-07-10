from sqlalchemy.orm import Session
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

    if operacion.tipo == "COMPRA":
        producto.cantidad += operacion.cantidad
    elif operacion.tipo == "VENTA":
        if producto.cantidad < operacion.cantidad:
            raise HTTPException(
                status_code=400,
                detail=f"Stock insuficiente. Disponible: {producto.cantidad}"
            )
        producto.cantidad -= operacion.cantidad
    elif operacion.tipo == "AJUSTE":
        producto.cantidad += operacion.cantidad  # Puede ser positivo o negativo
    else:
        raise HTTPException(status_code=400, detail="Tipo de operación inválido")

    db.commit()
    db.refresh(db_operacion)
    db.refresh(producto)  # Para obtener la cantidad actualizada

    return db_operacion
