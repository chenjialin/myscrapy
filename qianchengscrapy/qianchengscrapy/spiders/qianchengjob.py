# -*- coding: utf-8 -*-
import scrapy
import logging

from scrapy import Request
from qianchengscrapy.items import QianchengscrapyItem
# from scrapy.spiders import Rule
# from scrapy.linkextractor import LinkExtractor
# from scrapy.spiders import CrawlSpider
from bs4 import BeautifulSoup
from utils.db import DBConn

logging.basicConfig(filename='qiancheng.log', level=logging.INFO,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


class QianchengjobSpider(scrapy.Spider):
    name = 'qianchengjob'
    allowed_domains = ['www.51job.com']
    start_urls = [
        # 'http://jobs.51job.com/',  # get all city from here
        # 'http://js.51jobcdn.com/in/js/2016/layer/area_array_c.js?20170824'
        # 'http://search.51job.com/list/090200,000000,0000,00,9,99,python,2,1.html'  # get chengdu python position
    ]
    # rules = (
    #     Rule(LinkExtractor(allow=(), allow_domains=allowed_domains), callback='parse', follow=True),
    # )
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def __init__(self, url=None, *arg, **kwargs):
        super(QianchengjobSpider, self).__init__(*arg, **kwargs)
        if url:
            self.start_urls = [url]
            print("要爬取的网址为： %s" % url)

    def parse(self, response):
        item = QianchengscrapyItem()
        html_objs = response.xpath("//div[@id='resultList']/div[@class='el']")
        for html_obj in html_objs:
            try:
                item["position"] = (html_obj.xpath("./p//a/@title").extract() or [''])[0]
                item["url"] = (html_obj.xpath("./span[@class='t2']/a/@href").extract() or [''])[0]
                item["company"] = (html_obj.xpath("./span[@class='t2']/a/@title").extract() or [''])[0]
                item["address"] = (html_obj.xpath("./span[@class='t3']/text()").extract() or [''])[0]
                item["salary"] = (html_obj.xpath("./span[@class='t4']/text()").extract() or [''])[0]
                item["date"] = (html_obj.xpath("./span[@class='t5']/text()").extract() or [''])[0]
            except Exception as err:
                logging.error('------------------------------------------------------')
                logging.error(err)
                logging.error(html_obj.xpath("./p//a/@title"))
                logging.error(html_obj.xpath("./span[@class='t2']/a/@href"))
                logging.error(html_obj.xpath("./span[@class='t2']/a/@title"))
                logging.error(html_obj.xpath("./span[@class='t3']/text()"))
                logging.error(html_obj.xpath("./span[@class='t4']/text()"))
                logging.error(html_obj.xpath("./span[@class='t5']/text()"))
                logging.error('------------------------------------------------------')
            finally:
                yield item
        next_url = response.xpath("//div[@class='p_in']/ul/li[@class='bk'][last()]/a/@href").extract()
        if next_url:
            logging.info("Found next url %s." % next_url[0])
            yield Request(next_url[0], headers=self.headers, dont_filter=True, callback=self.parse)

    def start_requests(self):
        db = DBConn()
        results = db.execute("SELECT area_code FROM QianCheng.area_code WHERE id>37")
        for row in results:
            print('began handle %s.' % row[0])
            url = 'http://search.51job.com/list/' + str(row[0]) + ',000000,0000,00,9,99,%2B,2,1.html?' \
                  'lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&' \
                  'lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=102&dibiaoid=0&address=&line=&' \
                  'specialarea=00&from=&welfare='
            yield self.make_requests_from_url(url)

    # def make_requests_from_url(self, url):
    #     print('********make_requests_from_url*******************')

    def close(self, reason):
        print("spider closed!")

    # def log(self, message, level=logging.DEBUG, **kw):
    #     print("log function used!!")


