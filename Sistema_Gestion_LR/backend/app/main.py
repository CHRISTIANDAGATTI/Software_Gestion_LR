from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.api.api_v1.api import api_router
from app.database.session import engine
from sqlalchemy import text
import time

app = FastAPI(title="Sistema de Gestión Integral")

# Health check endpoint
@app.get("/health")
async def health_check():
    try:
        # Test DB connection
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": f"error: {str(e)}"}

# Middleware para debug
@app.middleware("http")
async def debug_middleware(request: Request, call_next):
    start_time = time.time()
    print(f"🔄 {request.method} {request.url}")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    print(f"✅ Response: {response.status_code} in {process_time:.2f}s")
    
    return response

# Incluir las rutas de la API v1
app.include_router(api_router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://software-gestion-lr-frontend.onrender.com"],  # producción: frontend en Render
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

