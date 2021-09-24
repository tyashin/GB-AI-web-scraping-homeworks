from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

import settings
from spiders.labirint_ru import LabirintRuSpider

if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LabirintRuSpider)
    process.start()
