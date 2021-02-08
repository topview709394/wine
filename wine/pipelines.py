
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
# from scrapy.conf import settings
import pymongo


class WinePipeline:
    def __init__(self):

        # def open_spider(self, item, spider):
        # 连接数据库
        self.table = self.db['wine']
        self.client = pymongo.MongoClient(host="127.0.0.1", port=27017)
        self.db = self.client["test"]  # 创建库
        # self.table = self.db["wine"]  # 创建表

    def process_item(self, item, spider):

        if "winery" in spider.name:  # 判断爬虫名字中是否包含winery
            self.table = self.db["winery"]
        # elif "rate" in spider.name:  # 判断爬虫名字中是否包含winery
        #     self.table = self.db["rate"]
        else:
            # del item['link']
            self.table.insert(dict(item))  # 直接将item写入数据库

        # return item
