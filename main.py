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
from app.database import SessionLocal
from app.selectors.results import search_results

def scraping_web():
    """
    Genera los datos en BBDD a partir del web scrapting
    si no hay ningún valor previo.
    """
    session = SessionLocal()
    results = search_results(session, limit=1)

    if not results:
        # Obtener la información del Scraping
        process = CrawlerProcess(get_project_settings())
        process.crawl('results')
        process.start()

def main():
    """Main execution"""
    load_dotenv()

    app = FastAPI()
    app.include_router(results_router, prefix="/results", tags=["results"])

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
