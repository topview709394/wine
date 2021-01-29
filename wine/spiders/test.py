import scrapy
from wine.items import WineItem


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['https://www.wine-world.com']
    start_urls = ['https://www.wine-world.com/']

    def parse(self, response):
        item = {}
        item["name_cn"] = "木桐"
        item["name_en"] = "mudopng"
        item["desxxx"] = [{"产地": "France", "面积": "120公顷"}]

        yield item
