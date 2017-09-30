# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QianchengscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    position = scrapy.Field()
    url = scrapy.Field()
    company = scrapy.Field()
    address = scrapy.Field()
    salary = scrapy.Field()
    date = scrapy.Field()
