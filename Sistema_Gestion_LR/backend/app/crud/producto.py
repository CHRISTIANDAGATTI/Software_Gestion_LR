from sqlalchemy.orm import Session
from app.models.producto import Producto
from app.schemas.producto import ProductoCreate
from app.schemas.producto import ProductoUpdate
from sqlalchemy.orm import Session
from fastapi import HTTPException


def get_productos(db: Session):
    return db.query(Producto).all()

def create_producto(db: Session, producto: ProductoCreate):
    db_producto = Producto(**producto.dict())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

def update_producto(db: Session, producto_id: int, producto_update: ProductoUpdate):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    for key, value in producto_update.dict(exclude_unset=True).items():
        setattr(producto, key, value)
    db.commit()     
    db.refresh(producto) 
    return producto 
        
def delete_producto(db: Session, producto_id: int):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if producto:
        db.delete(producto)
        db.commit()
        return True
    return False

def get_producto(db: Session, producto_id: int):
    return db.query(Producto).filter(Producto.id == producto_id).first()

