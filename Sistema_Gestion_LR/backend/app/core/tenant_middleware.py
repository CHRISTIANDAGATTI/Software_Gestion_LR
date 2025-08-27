"""
Middleware para detección automática de tenant en requests
"""
import re
from typing import Optional
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from sqlalchemy.orm import Session

from app.core.tenant_context import set_current_tenant, clear_current_tenant, validate_tenant_id
from app.database.session import SessionLocal
from app.crud.tenant import tenant as tenant_crud


class TenantMiddleware(BaseHTTPMiddleware):
    """
    Middleware que detecta el tenant actual y configura el contexto
    """
    
    async def dispatch(self, request: Request, call_next):
        # Limpiar contexto anterior
        clear_current_tenant()
        
        try:
            # 1. Intentar obtener tenant desde el subdominio
            tenant_id = self._extract_tenant_from_subdomain(request)
            
            # 2. Si no hay subdominio, intentar desde header X-Tenant-ID
            if not tenant_id:
                tenant_id = self._extract_tenant_from_header(request)
            
            # 3. Si no hay header, intentar desde el token JWT (futuro)
            if not tenant_id:
                tenant_id = await self._extract_tenant_from_token(request)
            
            # 4. Validar y verificar que el tenant existe
            if tenant_id:
                if not validate_tenant_id(tenant_id):
                    raise HTTPException(status_code=400, detail="Invalid tenant ID format")
                
                # Verificar que el tenant existe y está activo
                db = SessionLocal()
                try:
                    db_tenant = tenant_crud.get(db, id=tenant_id)
                    if not db_tenant:
                        raise HTTPException(status_code=404, detail="Tenant not found")
                    if not db_tenant.activo:
                        raise HTTPException(status_code=403, detail="Tenant is disabled")
                    
                    # Establecer contexto del tenant
                    set_current_tenant(tenant_id)
                    
                    # Nota: La configuración de RLS se manejará en cada sesión individual
                    # por ahora no configuramos RLS globalmente
                    
                finally:
                    db.close()
            
            # Procesar la request
            response = await call_next(request)
            return response
            
        except HTTPException:
            raise
        except Exception as e:
            # Log del error en producción
            print(f"Error en TenantMiddleware: {e}")
            print(f"Tipo de error: {type(e)}")
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
        finally:
            # Limpiar contexto al final
            clear_current_tenant()
    
    def _extract_tenant_from_subdomain(self, request: Request) -> Optional[str]:
        """
        Extrae el tenant desde el subdominio
        Ejemplo: tenant1.miapp.com -> buscar tenant con slug 'tenant1'
        """
        host = request.headers.get("host", "")
        if not host:
            return None
        
        # Extraer subdominio (formato: subdominio.dominio.com)
        parts = host.split(".")
        if len(parts) >= 3:  # subdominio.dominio.com
            subdomain = parts[0]
            
            # Si es un slug válido, buscar el tenant
            if re.match(r'^[a-z0-9-]+$', subdomain) and subdomain not in ['www', 'api', 'admin']:
                db = SessionLocal()
                try:
                    db_tenant = tenant_crud.get_by_slug(db, slug=subdomain)
                    if db_tenant and db_tenant.activo:
                        return str(db_tenant.id)
                finally:
                    db.close()
        
        return None
    
    def _extract_tenant_from_header(self, request: Request) -> Optional[str]:
        """
        Extrae el tenant desde el header X-Tenant-ID
        """
        return request.headers.get("X-Tenant-ID")
    
    async def _extract_tenant_from_token(self, request: Request) -> Optional[str]:
        """
        Extrae el tenant desde el token JWT del usuario
        (Para implementar cuando tengamos auth completo)
        """
        # TODO: Implementar cuando tengamos sistema de auth con JWT
        # authorization = request.headers.get("Authorization")
        # if authorization and authorization.startswith("Bearer "):
        #     token = authorization.split(" ")[1]
        #     # Decodificar JWT y obtener tenant_id del usuario
        return None
