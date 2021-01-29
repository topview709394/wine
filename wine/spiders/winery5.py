from collections import namedtuple
import scrapy
import re
from copy import deepcopy
from scrapy import item  # 把item作为一个数据集传递要导入这个
from w3lib import html


class Winery5Spider(scrapy.Spider):
    name = 'winery5'
    allowed_domains = ['www.wine-world.com']
    start_urls = [
        'https://www.wine-world.com/winery/chateau-lafite-rothschild/data'
    ]

    def parse(self, response):
        item = {}
        # # 国家
        # item['nation'] = response.xpath(
        #     '//*[@id="ulChain"]/li[2]/a/span/text()').get()
        # nation_cn = response.xpath('//*[@id="ulChain"]/li[2]/a/text()').get()
        # nation_cn = nation_cn.strip()
        # item['nation_cn'] = nation_cn.replace("酒庄", "")

        # # 总产区
        # item['main_region'] = response.xpath(
        #     '//*[@id="ulChain"]/li[3]/a/span/text()').get()
        # main_region = response.xpath('//*[@id="ulChain"]/li[3]/a/text()').get()
        # main_region = main_region.strip()
        # item['main_region_cn'] = main_region.replace("酒庄", "")

        # # 大产区
        # item['big_region'] = response.xpath(
        #     '//*[@id="ulChain"]/li[4]/a/span/text()').get()
        # big_region_cn = response.xpath(
        #     '//*[@id="ulChain"]/li[4]/a/text()').get()
        # big_region_cn = big_region_cn.strip()
        # item['big_region_cn'] = big_region_cn.replace("酒庄", "")

        # # 小产区
        # item['small_region'] = response.xpath(
        #     '//*[@id="ulChain"]/li[5]/a/span/text()').get()
        # small_region_cn = response.xpath(
        #     '//*[@id="ulChain"]/li[5]/a/text()').get()
        # small_region_cn = small_region_cn.strip()
        # item['small_region_cn'] = small_region_cn.replace("酒庄", "")

        # 子产区
        # sub_region = response.xpath(
        #     '//*[@id="leftContainer"]/div[2]/div/div[1]/span/text()').get()
        # item['sub_region'] = self.english(sub_region)

        # r = response.xpath(
        #     '//*[@id="leftContainer"]/div[2]/div/div[1]/text()').getall()
        # r = "".join(r)
        # r = r.strip()
        # item['sub_region_cn'] = r.replace("产区酒庄", "")

        # url = response.xpath('//div[@class="pages"]/a/@href').get()
        # url = url.rstrip("2")

        # # print(url)

        # for i in range(2, 20):
        #     path = url + str(i)
        #     print(path)

        # print("-" * 100)

        # 酒庄基本信息
        url = response.xpath('//div[@class="winery-nr"]/div')
        for i in url:

            item_name = i.xpath('./span[@class="base-n"]/text()').get()
            item_name = item_name.replace("：", "")
            item_cont = i.xpath('./span[@class="base-txt"]/text()').get()
            if item_cont is not None:
                item_cont = item_cont.replace("\r\n", "")
                item_cont = item_cont.strip()
            item[item_name] = item_cont

        # 酒庄扩展信息
        a = response.xpath('//div[@class="winery-ext"]')
        for i in a:
            item_name = i.xpath('.//span[@class="ext-item"]/text()').get()
            item_name = item_name.replace("：", "")
            item_name = "".join(item_name.split())
            item_cont = i.xpath('.//span[@class="ext-cont"]/text()').get()
            if item_cont is not None:
                item_cont = item_cont.replace("\r\n", "")
                item_cont = item_cont.strip()
            item[item_name] = item_cont

        b = response.xpath('//div[@class="winery-ext doub"]')
        for i in b:
            item_name = i.xpath('.//span[@class="ext-item"]/text()').get()
            item_name = item_name.replace("：", "")
            item_name = "".join(item_name.split())
            item_cont = i.xpath('.//span[@class="ext-cont"]/text()').get()
            if item_cont is not None:
                item_cont = item_cont.replace("\r\n", "")
                item_cont = item_cont.strip()
            item[item_name] = item_cont
        item['酒庄网址'] = response.xpath(
            '//div[@class="winery-ext"]//a/@href').get()
        print(item)

    def english(self, name):
        simple_punctuation = '[’!"#$%&\'()·（）：*+,-/:;<=>?@[\\]^_`{|}~，。,]'
        name = re.sub(simple_punctuation, '', name)  #去除标点符号
        name = re.sub('[\u4e00-\u9fa5]', '', name)  #去除中文
        name = name.strip()
        return name

    def chinese(self, name):
        simple_punctuation = '[’!"#$%&\'()·（）：*+,-/:;<=>?@[\\]^_`{|}~，。,]'
        name = re.sub(simple_punctuation, '', name)  #去除标点符号
        name = re.sub("[A-Za-z0-9\!\%\[\]\,\。]", "", name)  #去除英文
        name = name.strip()
        return name