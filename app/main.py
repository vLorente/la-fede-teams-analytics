"""Punto de entrada"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api import api_router

app = FastAPI(
    title="LaFedeAPI",
    summary='LA FEDE API: obtén información sobre 2ª Autonómica Masculina.',
    description="""
    ## EndPoints

    * Resultados de temporadas anteriores
    * Información sobre los equipos por temporada
    * **Calendarios de temporadas anteriores** (_not implemented_).
    """,
    version="0.0.1",
    contact={
        "name": "Valentín Lorente Jiménez",
        "url": "https://github.com/vLorente",
        "email": "vlorentejimenez@gmail.com",
    },
)

# Configuración de CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
