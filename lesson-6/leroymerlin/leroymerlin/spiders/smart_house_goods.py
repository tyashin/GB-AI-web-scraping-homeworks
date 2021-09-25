from urllib.parse import urljoin

import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

from leroymerlin.leroymerlin.items import LeroymerlinItem


class SmartHouseGoodsSpider(scrapy.Spider):
    name = 'smart_house_goods'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/catalogue/umnyy-dom/']
    root_url = 'https://leroymerlin.ru'

    def parse(self, response):
        next_page = response.xpath("//a[@data-qa-pagination-item='right']/@href").extract_first()

        if next_page:
            yield response.follow(urljoin(self.root_url, next_page), callback=self.parse)

        products_urls = response.xpath("//a[@data-qa='product-name']/@href").extract()
        yield from response.follow_all(products_urls, callback=self.parse_product)

    def parse_product(self, response: HtmlResponse):
        iloader = ItemLoader(item=LeroymerlinItem(), response=response)
        iloader.add_value('url', response.url)
        iloader.add_xpath('name', "///h1[@slot='title']")
        iloader.add_xpath('price', "//span[@slot='price']")
        iloader.add_xpath('availability', "//span[@class='label--available']")
        iloader.add_value('features', self.parse_product_features(response))
        iloader.add_value('image_urls',
                          response.xpath("//picture[@slot='pictures']//img[@itemprop='image']/@src").getall())

        yield iloader.load_item()

    def parse_product_features(self, response: HtmlResponse):
        product_features = response.xpath("//div[@class='def-list__group']")
        features = []
        for feature in product_features:
            feat = {'term': feature.xpath(".//dt[@class='def-list__term']/text()").get().strip(),
                    'value': feature.xpath(".//dd[@class='def-list__definition']/text()").get().strip()}
            features.append(feat)

        return features
