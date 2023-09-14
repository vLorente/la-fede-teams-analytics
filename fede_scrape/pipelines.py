# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
import json
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Result
from app.database import engine
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class JsonWriterPipeline:
    def open_spider(self, spider):
        self.file = open(f'resources/data/{spider.name}.jsonl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(item) + '\n'
        self.file.write(line)
        return item

class SqlitePipeline:
    """SQLite Insert Pipeline"""
    def __init__(self):
        load_dotenv()
        self.session = sessionmaker(bind=engine)()

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()

    def insert_result(self, data, table):
        if table == 'results':
            result = Result(**data)
            self.session.add(result)

    def process_item(self, item, spider):
        self.insert_result(item, spider.name)
        return item
