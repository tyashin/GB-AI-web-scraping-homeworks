import scrapy
from scrapy.http import HtmlResponse
from items import BookscraperItem


class LabirintRuSpider(scrapy.Spider):

    name = "labirint_ru"
    allowed_domains = ["labirint.ru"]
    start_urls = ["https://www.labirint.ru/search/%D0%9F%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5/"]
    root_url = "https://www.labirint.ru"
    def parse(self, response):

        next_page = response.xpath("//a[@title='Следующая']/@href").extract_first()

        if next_page:
             yield response.follow(self.start_urls[0] + next_page, callback=self.parse)

        book_urls = response.xpath("//a[@class='product-title-link']/@href").extract()

        for url in book_urls:
            yield response.follow(self.root_url + url, callback=self.parse_book)


    def parse_book(self, response: HtmlResponse):
        
        url = response.url
        name = response.xpath("//h1/text()").extract_first()
        authors = response.xpath("//div[@class='authors']/a/text()").extract()
        price = response.xpath("//span[@class='buying-priceold-val-number']/text()").extract_first()
        discount_price = response.xpath("//span[@class='buying-pricenew-val-number']/text()").extract_first()
        rating = response.xpath("//div[@id='rate']/text()").extract_first()

        item = BookscraperItem(url = url, 
                                name=name, 
                                authors=authors, 
                                price=price, 
                                discount_price=discount_price, 
                                rating=rating)
        yield item
        