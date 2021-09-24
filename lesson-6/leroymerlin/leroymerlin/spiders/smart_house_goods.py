import scrapy


class SmartHouseGoodsSpider(scrapy.Spider):
    name = 'smart_house_goods'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/catalogue/umnyy-dom/']

    def parse(self, response):
        pass
