from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api_v1.api import api_router

app = FastAPI(title="Sistema de Gestión Integral")

# Incluir las rutas de la API v1
app.include_router(api_router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # ["http://localhost:4200"] para limitarlo a Angular
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

