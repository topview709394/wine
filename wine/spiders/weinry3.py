from collections import namedtuple
import scrapy
import re
from copy import deepcopy
from scrapy import item  # 把item作为一个数据集传递要导入这个


class Winery3Spider(scrapy.Spider):
    name = 'winery3'
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
            item['web_list'] = []

            yield scrapy.Request(
                url=xxx,
                callback=self.parse_region,
                dont_filter=True,
                # 把整个item{}传递到下一个函数，使用deepcopy，保证下次循环的时候不会覆盖之前的内容
                meta={"item": deepcopy(item)})

    def parse_region(self, response):
        item = response.meta["item"]
        region_list = response.xpath('//ul[@class="wineRegion2"]/li')
        web_list = response.xpath(
            '//ul[@class="wineRegion2"]/li/a/@href').getall()

        if item['web_list'] == web_list:
            #----------------
            # 判断酒庄列表不为空才进行后续操作
            li = response.xpath('//ul[@class="listItem"]/li[1]/a/@href').get()
            if li is not None:
                # 从页面 获取层级信息 写入item
                # 国家
                item['nation'] = response.xpath(
                    '//*[@id="ulChain"]/li[2]/a/span/text()').get()
                nation_cn = response.xpath(
                    '//*[@id="ulChain"]/li[2]/a/text()').get()
                nation_cn = nation_cn.strip()
                item['nation_cn'] = nation_cn.replace("酒庄", "")

                # 总产区
                item['main_region'] = response.xpath(
                    '//*[@id="ulChain"]/li[3]/a/span/text()').get()
                main_region_cn = response.xpath(
                    '//*[@id="ulChain"]/li[3]/a/text()').get()
                if main_region_cn is not None:
                    main_region_cn = main_region_cn.strip()
                    item['main_region_cn'] = main_region_cn.replace("酒庄", "")
                else:
                    item['main_region_cn'] = ""

                # 大产区
                item['big_region'] = response.xpath(
                    '//*[@id="ulChain"]/li[4]/a/span/text()').get()
                big_region_cn = response.xpath(
                    '//*[@id="ulChain"]/li[4]/a/text()').get()
                if big_region_cn is not None:
                    big_region_cn = big_region_cn.strip()
                    item['big_region_cn'] = big_region_cn.replace("酒庄", "")
                else:
                    item['big_region_cn'] = ""
                # 小产区
                item['small_region'] = response.xpath(
                    '//*[@id="ulChain"]/li[5]/a/span/text()').get()
                small_region_cn = response.xpath(
                    '//*[@id="ulChain"]/li[5]/a/text()').get()
                if small_region_cn is not None:
                    small_region_cn = small_region_cn.strip()
                    item['small_region_cn'] = small_region_cn.replace("酒庄", "")
                else:
                    item['small_region_cn'] = ""

                # 子产区
                sub_region = response.xpath(
                    '//*[@id="leftContainer"]/div[2]/div/div[1]/span/text()'
                ).get()
                item['sub_region'] = self.english(sub_region)

                r = response.xpath(
                    '//*[@id="leftContainer"]/div[2]/div/div[1]/text()'
                ).getall()
                r = "".join(r)
                r = r.strip()
                item['sub_region_cn'] = r.replace("产区酒庄", "")
                # 从酒庄列表中获取每个酒庄的链接并发行给下个函数处理
                urls = response.xpath(
                    '//ul[@class="listItem"]/li/a/@href').getall()
                for url in urls:
                    yield scrapy.Request(url=url,
                                         callback=self.parse_winery,
                                         meta={"item": deepcopy(item)})

            # 下一页
            url = response.xpath('//div[@class="pages"]/a/@href').get()
            if url is not None:
                url = url.rstrip("2")
                for i in range(2, 10):
                    path = url + str(i)
                    yield scrapy.Request(url=path, callback=self.parse)

        # --------
        else:
            for li in region_list:
                item['web_list'] = web_list
                url_new = li.xpath('./a/@href').get()
                yield scrapy.Request(url=url_new,
                                     callback=self.parse_region,
                                     dont_filter=True,
                                     meta={"item": item})

    def parse_winery(self, response):
        item = response.meta['item']
        # 酒庄名字
        name_en = response.xpath(
            '//div[@class="winery-name"]/h1/text()').getall()
        name_en = "\n".join(name_en)
        item['name_en'] = name_en.strip()
        # 中文名字
        name_cn = response.xpath(
            '//div[@class="winery-name"]/h1/strong/text()').get()
        item['name_cn'] = name_cn.strip()

        # 酒庄简介
        dess = response.xpath('//div[@class="winery-nr"]//text()').getall()
        des = "".join(dess)  # 合并描述中的每一段文字，用换行分割
        des = des.strip()
        des = des.replace("\n\n",
                          "").replace("\t", "").replace("\r", "").replace(
                              "\xa0", "").replace("\u3000",
                                                  "").replace("  ", "")
        item['description'] = des

        url = response.xpath(
            '//div[@class="winery-menu"]/ul/li[2]/a/@href').get()
        yield scrapy.Request(url=url,
                             callback=self.parse_wineryinfo,
                             meta={"item": item})

    def parse_wineryinfo(self, response):
        item = response.meta['item']

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
        yield item

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