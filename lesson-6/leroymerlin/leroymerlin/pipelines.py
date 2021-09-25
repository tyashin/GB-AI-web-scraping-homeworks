# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import hashlib

# useful for handling different item types with a single interface
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.python import to_bytes


class LeroymerlinPipeline(ImagesPipeline):
    # def process_item(self, item, spider):
    #     return item

    def file_path(self, request, response=None, info=None, *, item=None):
        item_guid = hashlib.sha1(to_bytes(item['url'])).hexdigest()
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f'full/{item_guid}/{image_guid}.jpg'
