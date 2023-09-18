"""Main"""
import os
import uvicorn
from dotenv import load_dotenv
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from app.database import engine
from app.main import app
from app.crud.results import search_results
from app.crud.teams import search_teams
from app.database import SessionLocal, Base

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

    # Check para teams
    results = search_teams(session, limit=1)
    if not results:
        # Obtener la información del Scraping
        process.crawl('teams')
    process.start()


def main():
    """Ejecución principal"""

    # Crea las tablas en la base de datos (si no existen)
    Base.metadata.create_all(bind=engine)

    # Carga de datos desde el scraping web
    scraping_web()

    # Arrancar la API
    load_dotenv()
    host = os.getenv('HOST')
    port = int(os.getenv('PORT'))
    uvicorn.run(app, host=host, port=port)

if __name__ == '__main__':
    main()
