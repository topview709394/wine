# 酒款评分测试

import scrapy
import re
from copy import deepcopy
from scrapy import item  # 把item作为一个数据集传递要导入这个


class Winetest3Spider(scrapy.Spider):
    name = 'winetest3'
    allowed_domains = ['www.wine-world.com']
    start_urls = [
        'https://www.wine-world.com/wineinfo/53563719-5bd7-4f82-b842-0060f7318701/2019'
    ]

    def parse(self, response):
        item = {}
        ev_url = response.xpath(
            '//div[@class="wine-evalue"]/div[@class="evalue-list"]')
        xx = []  # 评分作为一个List 放入到 字典key=年份的值
        rate = {}
        if ev_url is not None:
            for i in ev_url:
                wine_year = i.xpath('./div[@class="ev-vintage"]/text()').get()

                rater = i.xpath('.//div[@class="ev-name"]/text()').get()
                rater = rater.strip()

                score = i.xpath('.//div[@class="ev-score"]/text()').get()
                score = score.strip()

                rate = {"rater": rater, "score": score}
                xx.append(rate)

                item[wine_year] = xx
            print(item)
            # item['ev'] =
