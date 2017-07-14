#coding=utf-8

from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.selector import Selector
from spider.items import SpiderItem
 
 
class MacbedSpider(CrawlSpider):
    name = "macbed"
    download_delay = 1
    allowed_domains = ["macbed.com"]
    #start_urls = [
    #    "https://www.macbed.com/page/%s/"  % page for page in range(10000,1,-1)
    #]

    start_urls = [
        "https://www.macbed.com/"
    ]
 
    def parse(self, response):
        sel = Selector(response)

        last_page = int(sel.xpath('//a[contains(@class,"page-numbers")]//text()')[-2].extract())
 
        for url in range(1,2):
            next_url =  "https://www.macbed.com/page/%s/" % str(url)
            yield Request(next_url, callback=self.parse_results)



    def parse_results(self,response):
        sel = Selector(response)

        urls = sel.xpath('//div[contains(@class, "entry")]//h2//a/@href')
        for url in urls:
            print url
            yield Request(url.extract(), callback=self.parse_product, meta={
                'splash': {
                    'args': {'wait': 0.5}},
                'url': url.extract()
            })


    def parse_product(self,response):
        sel = Selector(response)
        
        item = SpiderItem()

        category = sel.xpath('//div[contains(@class, "entry")]//div[contains(@class,"desc")]//a/text()')[-1].extract()
        content = sel.xpath('//div[contains(@class, "article")]//div[contains(@class,"text")]//p|//div[contains(@class, "article")]//div[contains(@class,"text")]//ul|//div[contains(@class, "article")]//div[contains(@class,"text")]//h5')[1:].extract()






        print category
        print content



