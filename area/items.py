# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AreaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    number = scrapy.Field()
    distinct = scrapy.Field()
    location = scrapy.Field()
    area = scrapy.Field()
    application = scrapy.Field()
    way = scrapy.Field()
    date = scrapy.Field()
    price = scrapy.Field()
    pass
