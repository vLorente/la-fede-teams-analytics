"""MAIN"""
import os
from fastapi import FastAPI
import uvicorn
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from dotenv import load_dotenv
from app.models import Base
from app.database import engine
from app.api.results import router as results_router
from app.api.teams import router as teams_router
from app.database import SessionLocal
from app.selectors.results import search_results
from app.selectors.teams import search_teams

def scraping_web():
    """
    Genera los datos en BBDD a partir del web scrapting
    si no hay ningún valor previo.
    """

    session = SessionLocal()
    process = CrawlerProcess(get_project_settings())
    # Check para results
    results = search_results(session, limit=1)

    if not results:
        # Obtener la información del Scraping
        process.crawl('results')
        process.start()

    # Check para teams
    results = search_teams(session, limit=1)
    if not results:
        # Obtener la información del Scraping
        process.crawl('teams')
        process.start()

def main():
    """Main execution"""
    load_dotenv()

    app = FastAPI()
    app.include_router(results_router, prefix="/results", tags=["results"])
    app.include_router(teams_router, prefix="/teams", tags=["teams"])

    # Crea las tablas en la base de datos (si no existen)
    Base.metadata.create_all(bind=engine)

    # Carga de datos desde el scraping web
    scraping_web()

    # Inicia la aplicación FastAPI
    host = os.getenv('HOST')
    port = int(os.getenv('PORT'))
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    main()
