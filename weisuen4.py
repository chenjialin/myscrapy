# -*- coding: utf-8 -*-
from scrapy.spiders import XMLFeedSpider


class Weisuen4Spider(XMLFeedSpider):
    name = 'weisuen4'
    allowed_domains = ['iqianyue.com']
    start_urls = ['http://iqianyue.com/feed.xml']
    iterator = 'iternodes' # you can change this; see the docs
    itertag = 'item' # change it accordingly

    def parse_node(self, response, selector):
        i = {}
        #i['url'] = selector.select('url').extract()
        #i['name'] = selector.select('name').extract()
        #i['description'] = selector.select('description').extract()
        return i
