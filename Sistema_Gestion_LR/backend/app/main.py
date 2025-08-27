from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api_v1.api import api_router

app = FastAPI(title="Sistema de Gestión Integral")

# Incluir las rutas de la API v1
app.include_router(api_router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://software-gestion-lr-frontend.onrender.com",
        "http://localhost:4200",  # Para desarrollo local
        "https://*.onrender.com"  # Cualquier subdominio de Render
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

