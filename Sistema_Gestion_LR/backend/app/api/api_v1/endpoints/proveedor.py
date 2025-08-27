from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.proveedor import Proveedor, ProveedorCreate
from app import crud
from app.database.session import get_db
from app.core.tenant_deps import get_optional_tenant_id

router = APIRouter()

@router.get("/proveedores", response_model=List[Proveedor])
def listar_proveedores(
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_optional_tenant_id)
):
    """Listar proveedores filtrados por tenant si está disponible"""
    proveedores = crud.proveedor.get_multi(db)
    
    # Si hay tenant, filtrar solo los proveedores de ese tenant
    if tenant_id:
        proveedores = [proveedor for proveedor in proveedores if str(proveedor.tenant_id) == tenant_id]
    
    return proveedores

@router.get("/proveedores/{id}", response_model=Proveedor)
def obtener_proveedor(
    id: int, 
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_optional_tenant_id)
):
    """Obtener proveedor por ID, verificando que pertenezca al tenant"""
    proveedor = crud.proveedor.get(db, id=id)
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    
    # Verificar que el proveedor pertenezca al tenant actual
    if tenant_id and str(proveedor.tenant_id) != tenant_id:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    
    return proveedor

@router.post("/proveedores", response_model=Proveedor)
def crear_proveedor(
    proveedor_in: ProveedorCreate, 
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_optional_tenant_id)
):
    """Crear proveedor asociado al tenant actual"""
    print(f"🔍 Datos de proveedor recibidos: {proveedor_in.dict()}")
    print(f"🏢 Tenant ID: {tenant_id}")
    
    # Si hay tenant, crear nuevo objeto con el tenant_id
    if tenant_id:
        proveedor_dict = proveedor_in.dict()
        proveedor_dict['tenant_id'] = tenant_id
        proveedor_in = ProveedorCreate(**proveedor_dict)
    
    try:
        result = crud.proveedor.create(db, obj_in=proveedor_in)
        print(f"✅ Proveedor creado: {result.id} para tenant: {tenant_id}")
        return result
    except Exception as e:
        print(f"❌ Error al crear proveedor: {e}")
        raise

@router.put("/proveedores/{id}", response_model=Proveedor)
def actualizar_proveedor(
    id: int, 
    proveedor_in: ProveedorCreate, 
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_optional_tenant_id)
):
    """Actualizar proveedor verificando que pertenezca al tenant"""
    db_proveedor = crud.proveedor.get(db, id=id)
    if not db_proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    
    # Verificar que el proveedor pertenezca al tenant actual
    if tenant_id and str(db_proveedor.tenant_id) != tenant_id:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    
    return crud.proveedor.update(db, db_obj=db_proveedor, obj_in=proveedor_in)

@router.delete("/proveedores/{id}")
def eliminar_proveedor(
    id: int, 
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_optional_tenant_id)
):
    """Eliminar proveedor verificando que pertenezca al tenant"""
    db_proveedor = crud.proveedor.get(db, id=id)
    if not db_proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    
    # Verificar que el proveedor pertenezca al tenant actual
    if tenant_id and str(db_proveedor.tenant_id) != tenant_id:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    
    crud.proveedor.remove(db, id=id)
    return {"detail": "Proveedor eliminado correctamente"}

@router.delete("/proveedores/{id}")
def eliminar_proveedor(id: int, db: Session = Depends(get_db)):
    db_proveedor = crud.proveedor.get(db, id=id)
    if not db_proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    crud.proveedor.remove(db, id=id)
    return {"message": "Proveedor eliminado exitosamente"}
