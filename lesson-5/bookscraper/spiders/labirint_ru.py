import scrapy
from scrapy.http import HtmlResponse

from bookscraper.items import BookscraperItem


class LabirintRuSpider(scrapy.Spider):
    name = "labirint_ru"
    allowed_domains = ["labirint.ru"]
    start_urls = [
        "https://www.labirint.ru/search/%D0%9F%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5/"]

    def parse(self, response):
        next_page = response.xpath("//a[@title='Следующая']/@href").extract_first()

        if next_page:
            yield response.follow(self.start_urls[0] + next_page, callback=self.parse)

        book_urls = response.xpath("//a[@class='product-title-link']/@href").extract()
        yield from response.follow_all(book_urls, callback=self.parse_book)

    def parse_book(self, response: HtmlResponse):
        item = BookscraperItem()
        item['url'] = response.url
        item['name'] = response.xpath("//h1/text()").extract_first()
        item['authors'] = response.xpath("//div[@class='authors']/a/text()").extract()
        item['price'] = response.xpath("//span[@class='buying-priceold-val-number']/text()").extract_first()
        item['discount_price'] = response.xpath("//span[@class='buying-pricenew-val-number']/text()").extract_first()
        item['rating'] = response.xpath("//div[@id='rate']/text()").extract_first()

        yield item
