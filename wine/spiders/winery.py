import scrapy
import re
from w3lib import html
from wine.items import WineItem


def winery_detail(response):
    id = response.meta['id']

    title = response.xpath(
        '/div[@class="wine-base"]//span[@class="base-n"]/text()').getall()
    print(title)


class WinerySpider(scrapy.Spider):
    name = 'winery'
    allowed_domains = ['www.wine-world.com/winery/']

    # baseUrl = "http://www.wine-world.com/winery/area/p"
    start_urls = [
        'https://wine-world.com/winery/area/usa/california/sonoma-county'
    ]

    def parse(self, response):
        id = 0
        url_list = response.xpath(
            '//ul[@class="listItem"]/li/a/@href').getall()
        for url in url_list:
            # print(id)
            # print(url)
            # print("-" * 100)

            yield scrapy.Request(url,
                                 callback=self.parse_winery,
                                 dont_filter=True,
                                 meta={"xxx": id})
            id += 1

    def parse_winery(self, response):
        item = WineItem()

        name = response.xpath('//li[@class="last"]/text()').get()
        name = name.strip()
        simple_punctuation = '[’!"#$%&\'()·（）：*+,-/:;<=>?@[\\]^_`{|}~，。,]'
        name = re.sub(simple_punctuation, '', name)  # 去除标点符号

        # 中文名字处理
        name_cn = re.sub("[A-Za-z0-9\!\%\[\]\,\。]", "", name)  # 去除英文
        name_cn = name_cn.strip()

        # 英文名字处理
        name_en = re.sub('[\u4e00-\u9fa5]', '', name)  # 去除中文
        name_en = name_en.strip()

        # id 传递
        id = response.meta['xxx']

        # 酒庄简介处理
        des_list = response.xpath('//div[@class="winery-nr"]/p').getall()

        # ---------------------------------------------------------------------------
        # 处理列表中项目合并的方法 1 优点是可以去除每个字块前后的空格，再叠加
        # des = ""
        # for index in range(len(des_list)):
        #     des = des_list[index] + des
        #     des = html.remove_tags(des)  #去除文本中的 html tags
        #     des.strip()
        #     des = des.replace("\r",
        #                       "").replace("\n", "").replace("\t", "").replace(
        #                           "\u3000", "").replace("\xa0", "")  #去除换行符。。。
        # ---------------------------------------------------------------------------

        # 合并列表中各个字符串的方法 2 ，优点是简单，缺点是无法去除每一项前后的空格
        des = ''.join(des_list)  # 列表转换为字符串
        des = html.remove_tags(des)  # 去除文本中的 html tags
        des.strip()
        des = des.replace("\r",
                          "").replace("\n", "").replace("\t", "").replace(
            "\u3000", "").replace("\xa0", "")  # 去除换行符。。。

        # print(des)
        # print("-" * 100)

        # 获取酒庄资料链接
        url = response.xpath(
            '//div[@class="winery-menu"]//li[2]/a/@href').get()
        yield scrapy.Request(url, callback=winery_detail, meta={"id": id})
