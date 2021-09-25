# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Identity
from w3lib.html import remove_tags


def filter_price(value):
    return int(''.join([str(s) for s in value.split() if s.isdigit()]))


class LeroymerlinItem(scrapy.Item):
    url = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(remove_tags, filter_price), output_processor=TakeFirst())
    availability = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    features = scrapy.Field(output_processor=Identity())

    image_urls = scrapy.Field()
    images = scrapy.Field()
