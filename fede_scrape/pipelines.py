# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
from dotenv import load_dotenv
from app.models.result import Result
from app.models.team import Team
from app.database import SessionLocal
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
        self.session = SessionLocal()

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()

    def insert_result(self, data, table):
        if table == 'results':
            result = Result(**data)
            self.session.add(result)
            
        if table == 'teams':
            result = Team(**data)
            self.session.add(result)

    def process_item(self, item, spider):
        self.insert_result(item, spider.name)
        return item
