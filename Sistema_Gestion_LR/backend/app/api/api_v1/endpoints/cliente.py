from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.cliente import Cliente, ClienteCreate
from app import crud
from app.database.session import get_db
from app.core.tenant_deps import get_optional_tenant_id

router = APIRouter()

@router.get("/clientes", response_model=List[Cliente])
def listar_clientes(
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_optional_tenant_id)
):
    """Listar clientes filtrados por tenant si está disponible"""
    clientes = crud.cliente.get_multi(db)
    
    # Si hay tenant, filtrar solo los clientes de ese tenant
    if tenant_id:
        clientes = [cliente for cliente in clientes if str(cliente.tenant_id) == tenant_id]
    
    return clientes

@router.get("/clientes/{id}", response_model=Cliente)
def obtener_cliente(
    id: int, 
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_optional_tenant_id)
):
    """Obtener cliente por ID, verificando que pertenezca al tenant"""
    cliente = crud.cliente.get(db, id=id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # Verificar que el cliente pertenezca al tenant actual
    if tenant_id and str(cliente.tenant_id) != tenant_id:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    return cliente

@router.post("/clientes", response_model=Cliente)
def crear_cliente(
    cliente_in: ClienteCreate, 
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_optional_tenant_id)
):
    """Crear cliente asociado al tenant actual"""
    print(f"🔍 Datos de cliente recibidos: {cliente_in.dict()}")
    print(f"🏢 Tenant ID: {tenant_id}")
    
    # Si hay tenant, crear nuevo objeto con el tenant_id
    if tenant_id:
        cliente_dict = cliente_in.dict()
        cliente_dict['tenant_id'] = tenant_id
        cliente_in = ClienteCreate(**cliente_dict)
    
    try:
        result = crud.cliente.create(db, obj_in=cliente_in)
        print(f"✅ Cliente creado: {result.id} para tenant: {tenant_id}")
        return result
    except Exception as e:
        print(f"❌ Error al crear cliente: {e}")
        raise

@router.put("/clientes/{id}", response_model=Cliente)
def actualizar_cliente(
    id: int, 
    cliente_in: ClienteCreate, 
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_optional_tenant_id)
):
    """Actualizar cliente verificando que pertenezca al tenant"""
    db_cliente = crud.cliente.get(db, id=id)
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # Verificar que el cliente pertenezca al tenant actual
    if tenant_id and str(db_cliente.tenant_id) != tenant_id:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    return crud.cliente.update(db, db_obj=db_cliente, obj_in=cliente_in)

@router.delete("/clientes/{id}")
def eliminar_cliente(
    id: int, 
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_optional_tenant_id)
):
    """Eliminar cliente verificando que pertenezca al tenant"""
    db_cliente = crud.cliente.get(db, id=id)
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # Verificar que el cliente pertenezca al tenant actual
    if tenant_id and str(db_cliente.tenant_id) != tenant_id:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    crud.cliente.remove(db, id=id)
    return {"detail": "Cliente eliminado correctamente"}

@router.delete("/clientes/{id}")
def eliminar_cliente(id: int, db: Session = Depends(get_db)):
    db_cliente = crud.cliente.get(db, id=id)
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    crud.cliente.remove(db, id=id)
    return {"message": "Cliente eliminado exitosamente"}
