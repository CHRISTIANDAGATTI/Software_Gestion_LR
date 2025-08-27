from fastapi import APIRouter
from app.api.api_v1.endpoints import stock, cliente, proveedor, tipo_operacion, usuario

api_router = APIRouter()
api_router.include_router(stock.router, prefix="", tags=["stock"])
api_router.include_router(cliente.router, prefix="", tags=["clientes"])
api_router.include_router(proveedor.router, prefix="", tags=["proveedores"])
api_router.include_router(tipo_operacion.router, prefix="", tags=["tipo_operacion"])
api_router.include_router(usuario.router, prefix="", tags=["usuario"])
