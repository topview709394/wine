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

        # # 取到settings里面数据库连接参数
        # host = settings['MONGODB_HOST']
        # port = settings['MONGODB_PORT']
        # db = settings['MONGODB_DBNAME']
        # table = settings['MONGODB_TABLENAME']
        # client = pymongo.MongoClient(host=host, port=port)
        # mydb = client['db']

        # def open_spider(self, item, spider):
        #连接数据库
        self.client = pymongo.MongoClient(host="127.0.0.1", port=27017)
        # self.client = pymongo.MongoClient(host=host, port=port)
        self.db = self.client["test"]  #创建库
        self.table = self.db["wine"]  #创建表

    def process_item(self, item, spider):
        # del item['web_list']
        # data = {
        #     "main_region": item["main_region"],
        #     "big_region": item["big_region"],
        #     "small_region": item["small_region"],
        #     "sub_region": item["sub_region"],
        #     "nation": item["nation"],
        #     "name_cn": item["name_cn"],
        #     "name_en": item["name_en"]
        # }

        # self.table.insert(dict(data))  # 数据处理以后写入数据库

        # 两种写法，判断爬虫名字确认表名
        if "winery" in spider.name:  # 判断爬虫名字中是否包含winery
            self.table = self.db["winery"]
        else:
            self.table = self.db['wine']

        self.table.insert(dict(item))  # 直接将item写入数据库

        return item

    # def clean(slef,item):
    #     xx =  item
