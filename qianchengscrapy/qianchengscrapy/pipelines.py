# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from utils.db import DBConn


class QianchengscrapyPipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        db = DBConn()
        db.insert('city_position', dict(item))
        return None

    def close_spider(self, spider):
        print('end------------')
