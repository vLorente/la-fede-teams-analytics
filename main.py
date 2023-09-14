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

def main():
    """Main execution"""
    app = FastAPI()
    app.include_router(results_router, prefix="/results", tags=["results"])

    # Crea las tablas en la base de datos (si no existen)
    Base.metadata.create_all(bind=engine)

    # Obtener la información del Scraping
    process = CrawlerProcess(get_project_settings())
    process.crawl('results')
    process.start()

    # Inicia la aplicación FastAPI
    host = os.getenv('HOST')
    port = os.getenv('PORT')
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    load_dotenv()
    main()
