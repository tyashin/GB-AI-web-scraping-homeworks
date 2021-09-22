# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient


class BookscraperPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.labirint_ru_books

    def process_item(self, item, spider):

        item['price'] = float(item['price']) if item['price'] else 0
        item['discount_price'] = float(item['discount_price']) if item['discount_price'] else 0
        item['rating'] = float(item['rating']) if item['rating'] else 0
        
        collection = self.mongobase['labirint_ru']
        collection.insert_one(item)

        return item
