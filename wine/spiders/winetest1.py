# 测试从酒庄酒款页面开始进入到酒款详情页面抓取信息
# 这是成功的，爬取酒款信息，但不包含评分信息
# 评分信息需要单独使用

import scrapy
from copy import deepcopy


class Winetest1Spider(scrapy.Spider):
    name = 'winetest1'
    allowed_domains = ['www.wine-world.com']
    start_urls = [
        'https://www.wine-world.com/winery/domaine-de-chevalier/wine'
    ]

    def parse(self, response):
        item = {}
        wine_list = response.xpath('//a[@class="wine-enm"]/@href').getall()
        for i in wine_list:
            yield scrapy.Request(url=i,
                                 callback=self.parse_wineinfo,
                                 meta={"item": item})

    # 酒款列表翻页
    # next_page = response.xpath('//div[@class="pages"]/a')
    # if next_page.xpath('./text()').get() == "下一页":
    #     next_link = next_page.xpath('./@href')
    #     yield scrapy.Request(url=next_link,
    #                          callback=self.parse,
    #                          meta={'item': item})

    def parse_wineinfo(self, response):

        item = response.meta['item']
        # 酒款描述 -------------------------------------------
        des = response.xpath('//div[@class="overview"]/text()').getall()
        des = "".join(des)
        des = des.strip()
        item['overview'] = des

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
        item['name_cn'] = response.xpath(
            '//div[@class="wineChi"]/text()').get().strip()

        item['name_en'] = response.xpath(
            '//div[@class="wineEng"]/text()').get().strip()

        item['winery_name'] = response.xpath(
            '//div[@class="pathbox"]/ul/li[last()-1]/a/text()').get().strip()

        yield item
