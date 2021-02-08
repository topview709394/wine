import scrapy


class RateSpider(scrapy.Spider):
    name = 'rate'
    allowed_domains = ['www.wine-world.com']
    start_urls = [
        'https://www.wine-world.com/winery/domaine-de-chevalier/wine'
    ]

    def parse(self, response):
        wine_list = response.xpath('//a[@class="wine-enm"]/@href').getall()
        for i in wine_list:
            yield scrapy.Request(
                url=i,
                callback=self.parse_wine,
                dont_filter=True,
            )

    def parse_wine(self, response):
        item = {}
        # 获取评分信息 的 年份 -------------------------------------------
        urls = response.xpath('//ul[@class="vintage-wrap"]/li/a')
        item['name_en'] = response.xpath(
            '//div[@class="wineEng"]/text()').get().strip()
        for i in urls:
            year = i.xpath('./text()').get()
            link = i.xpath('./@href').get()
            if year != "NV":
                url = "https://www.wine-world.com/" + link
                yield scrapy.Request(url=url,
                                     callback=self.parse_rate,
                                     dont_filter=True,
                                     meta={"item": item})

    def parse_rate(self, response, xx=[]):
        item = response.meta['item']
        # 评分信息 -------------------------------------------
        ev_url = response.xpath(
            '//div[@class="wine-evalue"]/div[@class="evalue-list"]')
        # xx = []  # 评分作为一个List 放入到 字典key=年份的值
        if ev_url is not None:
            wine_year = ev_url.xpath('./div[@class="ev-vintage"]/text()').get()
            for i in ev_url:
                rater = i.xpath(
                    './/div[@class="ev-name"]/text()').get().strip()
                score = i.xpath(
                    './/div[@class="ev-score"]/text()').get().strip()

                rate = {"rater": rater, "score": score}
                xx.append(rate)
                # item[wine_year] = xx
        print(xx)
        # yield item
