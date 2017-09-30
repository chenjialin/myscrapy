from scrapy import Spider


class FirstSpider(Spider):
    name = "first"
    allow_domains = ["baidu.com"]
    start_url = ["http://www.baidu.com",]

    def parse(self, response):
        pass
