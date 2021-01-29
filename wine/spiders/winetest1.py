import scrapy
import re
from copy import deepcopy
from scrapy import item  # 把item作为一个数据集传递要导入这个


class Winetest1Spider(scrapy.Spider):
    name = 'winetest1'
    allowed_domains = ['www.wine-world.com']
    start_urls = ['https://www.wine-world.com/winery/domaine-vacheron/wine']

    def parse(self, response):
        item = {}
        wine_list = response.xpath(
            '//div[@class="winery-sj"]/div[@class="sch-cont"]')
        for i in wine_list:
            item['name_en'] = i.xpath(
                './div[@class="wine-f"]/a[@class="wine-enm"]/text()').get()
            item['name_cn'] = i.xpath(
                './div[@class="wine-f"]/div[@class="wine-cnm"]/a/text()').get(
                )
            link = i.xpath(
                './div[@class="wine-f"]/a[@class="wine-enm"]/@href').get()

            yield scrapy.Request(url=link,
                                 callback=self.parse_wineinfo,
                                 meta={"item": item})

        # 酒款列表翻页

    def parse_wineinfo(self, response):
        item = response.meta['item']

        years = response.xpath('//ul[@class="vintage-wrap"]/li')
        for i in years:
            url = i.xpath('./a/@href').get()
            item['year'] = i.xpath('./a/text()').get()

            des = response.xpath('//div[@class="overview"]/text()').get()
            # 评分信息 -------------------------------------------

            evalues = response.xpath('//div[@class="evalue-list"]')
            if evalues is not None:
                for i in evalues:
                    item['rate_year'] = i.xpath(
                        './div[@class="ev-vintage"]/text()').get()
                    item['rater'] = i.xpath(
                        './div[@class="ev-name"]/text()').get()
                    item['score'] = i.xpath(
                        './div[@class="ev-score"]/text()').get()

            # 酒款信息 -------------------------------------------
            attrs = response.xpath('//div[@class="attribute"]/dl')
            for i in attrs:
                item_name = i.xpath('./dt/text()')
                item_cont = i.xpath('./dd/text()')
                item[item_name] = item_cont

            yield scrapy.Request(url=url,
                                 callback=self.parse_wineinfo,
                                 meta={"item": deepcopy(item)})
