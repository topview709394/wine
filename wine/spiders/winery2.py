import scrapy
import re
from copy import deepcopy
from scrapy import item  # 把item作为一个数据集传递要导入这个


class Winery2Spider(scrapy.Spider):
    name = 'winery2'
    allowed_domains = ['www.wine-world.com']
    start_urls = ['http://www.wine-world.com/']

    # 根据列表中的地址遍历国家
    def parse(self, response):
        baseUrl = "https://www.wine-world.com/winery/area/"
        urls = [
            # "spain"
            "france",
            # "italy", "spain",
            # "portugal",
            # "germany", "australia",
            # "new-zealand", "chile", "argentina", "usa", "south-africa"
        ]

        for i in urls:
            item = {}
            nation = str(i)
            xxx = baseUrl + nation
            item["nation"] = nation
            item['web'] = xxx
            item['region'] = 0
            yield scrapy.Request(
                url=xxx,
                callback=self.parse_region,
                dont_filter=True,
                # 把整个item{}传递到下一个函数，使用deepcopy，保证下次循环的时候不会覆盖之前的内容
                meta={"item": item})

    def parse_region(self, response):
        item = response.meta["item"]
        region = item['region']
        url_last = str(item['web'])

        region_list = response.xpath('//ul[@class="wineRegion2"]/li')

        for li in region_list:
            url_new = li.xpath('./a/@href').get()

            name = li.xpath('./a/@title').get()
            name_en = re.sub('[\u4e00-\u9fa5]', '', name)  #去除中文
            item['region_name'] = name_en.strip()

            if url_new != url_last:
                item['web'] = url_new
                item['region'] = region + 1
                # print(item)
                print("NEWS:" + url_new)
                print("LAST:" + url_last)
                print(item['region'], "CLASS:", item['region_name'])
                print("-" * 100)

                yield scrapy.Request(url=url_new,
                                     callback=self.parse_region,
                                     meta={"item": item})
            else:
                print('@@@@' * 10)
                print("NEWS:" + url_new)
                print("LAST:" + url_last)
                print('@@@@' * 10)
