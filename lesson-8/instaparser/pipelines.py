# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient, ASCENDING


class InstaparserPipeline:
    def __init__(self):
        super()
        client = MongoClient('localhost', 27017)
        self.mongobase = client.instafollowers
        self.mongobase['followers'].create_index([("parent_name", ASCENDING)])
        self.mongobase['following'].create_index([("parent_name", ASCENDING)])
        self.item_keys = ['parent_id', 'parent_name', 'user_id', 'user_photo', 'user_photo_file', 'user_name', '_id']

    def process_item(self, item, spider):
        super()
        collection = self.mongobase[item['connection_type']]
        mongo_item = dict((k, item[k]) for k in self.item_keys if k in item)
        collection.insert_one(mongo_item)

        return item


