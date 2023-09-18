"""Punto de entrada"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv
from app.routers.results import router as results_router
from app.routers.teams import router as teams_router

def run_api():
    """Configuración servicio FastAPI"""
    load_dotenv()


    api_description = """
    ## EndPoints

    * Resultados de temporadas anteriores
    * Información sobre los equipos por temporada
    * **Calendarios de temporadas anteriores** (_not implemented_).
    """

    app = FastAPI(
        title="LaFedeAPI",
        summary='LA FEDE API: obtén información sobre 2ª Autonómica Masculina.',
        description=api_description,
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

    app.include_router(results_router, prefix="/results", tags=["results"])
    app.include_router(teams_router, prefix="/teams", tags=["teams"])

    # Inicia la aplicación FastAPI
    host = os.getenv('HOST')
    port = int(os.getenv('PORT'))
    uvicorn.run(app, host=host, port=port)

