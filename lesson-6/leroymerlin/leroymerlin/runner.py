from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from leroymerlin.leroymerlin import settings
from leroymerlin.leroymerlin.spiders.smart_house_goods import SmartHouseGoodsSpider

if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(SmartHouseGoodsSpider)
    process.start()
