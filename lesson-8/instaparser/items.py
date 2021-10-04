# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst
from scrapy.utils.python import to_bytes
import hashlib


def getFileName(value):
    return str(hashlib.sha1(to_bytes(value[0])).hexdigest()) + '.jpg'

class InstaparserItem(scrapy.Item):
    # define the fields for your item here like:
    parent_id = scrapy.Field(output_processor=TakeFirst())
    parent_name = scrapy.Field(output_processor=TakeFirst())
    user_name = scrapy.Field(output_processor=TakeFirst())
    user_id = scrapy.Field(output_processor=TakeFirst())
    connection_type = scrapy.Field(output_processor=TakeFirst())
    user_photo = scrapy.Field(output_processor=TakeFirst())
    user_photo_file = scrapy.Field(output_processor=getFileName)
    _id = scrapy.Field(output_processor=TakeFirst())

    image_urls = scrapy.Field()
    images = scrapy.Field()
