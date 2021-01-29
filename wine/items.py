# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WineItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    m_name_cn = scrapy.Field()
    m_name_en = scrapy.Field()
    id = scrapy.Field()
    des = scrapy.Field()
    web = scrapy.Field()
    nation = scrapy.Field()

    country = scrapy.Field()
    main_area = scrapy.Field()
    sub_area = scrapy.Field()
    s_area = scrapy.Field()
    ss_area = scrapy.Field()

    country_en = scrapy.Field()
    main_area_en = scrapy.Field()
    sub_area_en = scrapy.Field()
    s_area_en = scrapy.Field()
    ss_area_en = scrapy.Field()

    phone = scrapy.Field()
    web = scrapy.Field()
    address = scrapy.Field()
    mail = scrapy.Field()
    remark = scrapy.Field()
    phone = scrapy.Field()
    phone = scrapy.Field()

    space = scrapy.Field()
    grade = scrapy.Field()
    soil = scrapy.Field()
    main_grape = scrapy.Field()
    other_grape = scrapy.Field()

    pass


class WineryItem(scrapy.Item):
    country = scrapy.Field()
    area = scrapy.Field()
    main_area = scrapy.Field()
    sub_area = scrapy.Field()

    id = scrapy.Field()
    des = scrapy.Field()

    m_name_cn = scrapy.Field()
    m_name_en = scrapy.Field()
    web = scrapy.Field()
    nation = scrapy.Field()
