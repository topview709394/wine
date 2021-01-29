import scrapy
import re
from copy import deepcopy
from scrapy import item  # 把item作为一个数据集传递要导入这个
from wine.items import WineryItem
from scrapy.http.request import Request


class Winery1Spider(scrapy.Spider):
    name = 'winery1'
    allowed_domains = ['www.wine-world.com']
    start_urls = ['http://www.wine-world.com/']

    # 根据列表中的地址遍历国家
    def parse(self, response):
        baseUrl = "https://www.wine-world.com/winery/area/"
        urls = [
            "france",
            # "italy",
            # "spain",
            # "portugal", "germany", "australia",
            # "new-zealand", "chile", "argentina", "usa", "south-africa"
        ]

        for i in urls:
            item = {}
            nation = str(i)
            xxx = baseUrl + nation
            item["nation"] = nation
            item['web'] = xxx

            yield scrapy.Request(
                url=xxx,
                callback=self.parse_main_region,
                # dont_filter=True,
                # 把整个item{}传递到下一个函数，使用deepcopy，保证下次循环的时候不会覆盖之前的内容
                meta={"item": item})

    # 根据传过来的国家，遍历主产区
    def parse_main_region(self, response):
        url_list = response.xpath('//ul[@class="wineRegion2"]/li')
        item = response.meta["item"]
        last_url = item['web']

        for i in url_list:
            new_url = i.xpath('./a/@href').get()
            name = i.xpath('./a/@title').get()
            name_cn = re.sub("[A-Za-z0-9\!\%\[\]\,\。]", "", name)  #去除英文
            item['region1_cn'] = name_cn.strip()

            name_en = re.sub('[\u4e00-\u9fa5]', '', name)  #去除中文
            item['region1_en'] = name_en.strip()
            if last_url != new_url:
                item['web'] = new_url
                yield scrapy.Request(
                    url=new_url,
                    callback=self.parse_bigarea,
                    #  dont_filter=True,
                    meta={"item": item})

    # 根据主产区，遍历大产区，可能为空
    def parse_bigarea(self, response):
        item = response.meta["item"]
        url_list = response.xpath('//ul[@class="wineRegion2"]/li')
        last_url = item['web']

        for i in url_list:
            new_url = i.xpath('./a/@href').get()

            name = i.xpath('./a/@title').get()
            name_cn = re.sub("[A-Za-z0-9\!\%\[\]\,\。]", "", name)  #去除英文
            item['region2_cn'] = name_cn.strip()

            name_en = re.sub('[\u4e00-\u9fa5]', '', name)  #去除中文
            item['region2_en'] = name_en.strip()

            if last_url != new_url:
                item['web'] = new_url

                print(item['region1_cn'], "~~", item['region2_cn'])
                # yield scrapy.Request(url=item['web'],
                #                      callback=self.parse_smallarea,
                #                      dont_filter=True,
                #                      meta={"item": deepcopy(item)})
            else:
                print("--end--" * 10)
            # winery_urls = response.xpath(
            #     '//div[@class="sch-kng"]//li/a/@href').getall()
            # for i in winery_urls:
            #     yield scrapy.Request(url=i,
            #                          callback=self.parse_winery,
            #                          meta={"item": deepcopy(item)})

    def parse_smallarea(self, response):
        item = response.meta["item"]
        url_list = response.xpath('//ul[@class="wineRegion2"]/li')

        for i in url_list:
            url = i.xpath('./a/@href').get()

            name = i.xpath('./a/@title').get()
            name_cn = re.sub("[A-Za-z0-9\!\%\[\]\,\。]", "", name)  #去除英文
            item['region3_cn'] = name_cn.strip()

            name_en = re.sub('[\u4e00-\u9fa5]', '', name)  #去除中文
            item['region3_en'] = name_en.strip()

            if url != item['web']:
                item['web'] = url
                yield scrapy.Request(url=item['web'],
                                     callback=self.parse_subarea,
                                     dont_filter=True,
                                     meta={"item": deepcopy(item)})
            else:
                print("--end--")

    def parse_subarea(self, response):
        item = response.meta["item"]
        url_list = response.xpath('//ul[@class="wineRegion2"]/li')

        for i in url_list:
            url = i.xpath('./a/@href').get()

            name = i.xpath('./a/@title').get()
            name_cn = re.sub("[A-Za-z0-9\!\%\[\]\,\。]", "", name)  #去除英文
            item['region4_cn'] = name_cn.strip()

            name_en = re.sub('[\u4e00-\u9fa5]', '', name)  #去除中文
            item['region4_en'] = name_en.strip()

            if url != item['web']:
                item['web'] = url
                print(item)
                print("-" * 100)
                # yield scrapy.Request(url=item['web'],
                #                      callback=self.parse_subarea,
                #                      meta={"item": deepcopy(item)})
            else:
                print("--end--")