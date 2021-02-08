# 酒款详情页面测试
# from typing import Dict, Any, Union, Optional
import scrapy
# from copy import deepcopy
# from scrapy import item  # 把item作为一个数据集传递要导入这个


class Winetest2Spider(scrapy.Spider):
    name = 'winetest2'
    allowed_domains = ['www.wine-world.com']
    start_urls = [
        'https://www.wine-world.com//wineinfo/E2F0FD24-0FBD-48B4-8F46-98587A4F35BD'
    ]

    def parse(self, response):

        item = {}

        item['link'] = response.request.url
        # 获取评分信息——————————————————————————————————————————————————————
        urls = response.xpath('//ul[@class="vintage-wrap"]/li/a')
        for i in urls:
            year = i.xpath('./text()').get()
            link = i.xpath('./@href').get()
            if year != "NV":
                url = "https://www.wine-world.com/" + link
                yield scrapy.Request(url=url,
                                     callback=self.parse_winerate,
                                     meta={"item": item})

    def parse_winerate(self, response):
        item = response.meta["item"]
        # 评分信息 -------------------------------------------
        ev_url = response.xpath(
            '//div[@class="wine-evalue"]/div[@class="evalue-list"]')
        xx = []  # 评分作为一个List 放入到 字典key=年份的值
        if ev_url is not None:
            for i in ev_url:
                wine_year = i.xpath('./div[@class="ev-vintage"]/text()').get()

                rater = i.xpath('.//div[@class="ev-name"]/text()').get()
                rater = rater.strip()

                score = i.xpath('.//div[@class="ev-score"]/text()').get()
                if score is not None:
                    score = score.strip()
                else:
                    score = ""
                rate = {"rater": rater, "score": score}
                xx.append(rate)
                item[wine_year] = xx

        yield scrapy.Request(url=item['link'],
                             callback=self.wine_info,
                             meta={'item': item})

    def wine_info(self, response):

        item = response.meta['item']
        # 酒款描述 -------------------------------------------
        des = response.xpath('//div[@class="overview"]/text()').getall()
        des = "".join(des)
        des = des.strip()
        item['des'] = des

        # 酒款信息 -------------------------------------------
        for k in range(2, 5):
            item_name = response.xpath('//div[@class="attribute"]/dl[' +
                                       str(k) + ']/dt/text()').get().replace(
                                           "：", "")
            item_cont = response.xpath('//div[@class="attribute"]/dl[' +
                                       str(k) + ']/dd/a/text()').getall()

            item_cont = " ".join(item_cont)
            item_cont = item_cont.replace("\r\n",
                                          "").replace("\xa0", "").replace(
                                              "&nbsp", "-").replace(" ", "")
            item[item_name] = item_cont.strip()

        item['wine_type'] = response.xpath(
            '//div[@class="attribute"]/dl[1]/dd/text()').get().strip()
        taste = response.xpath('//div[@id="Winetaste"]//dd/text()').get()
        if taste is not None:
            taste = taste.replace("\r\n", "").replace("\xa0", "").replace(
                "&nbsp", "-").replace(" ", "")
        item['taste'] = taste

        # 酒款名字 -------------------------------------------
        name_cn = response.xpath('//div[@class="wineChi"]/text()').get()
        item['name_cn'] = name_cn.strip()

        name_en = response.xpath('//div[@class="wineEng"]/text()').get()
        item['name_en'] = name_en.strip()

        yield item
