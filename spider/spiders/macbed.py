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

        what_new = sel.xpath('//div[contains(@class, "article")]//div[contains(@class,"text")]//p|//div[contains(@class, "article")]//div[contains(@class,"text")]//ul|//div[contains(@class, "article")]//div[contains(@class,"text")]//h3')[1:].extract()

        requirements = sel.xpath('//div[contains(@class, "article")]//div[contains(@class,"text")]//p|//div[contains(@class, "article")]//div[contains(@class,"text")]//ul|//div[contains(@class, "article")]//div[contains(@class,"text")]//h3')[1:].extract()

        download_url = sel.xpath('//div[contains(@class, "appdl")]//a/@href').extract()
        
        print ''.join(category)
        print '------'
        print ''.join(content)
        print '22222222'
        print ''.join(what_new)
        print '33333333'
        print ''.join(requirements)
        yield Request(download_url, callback=self.parse_url, meta={
            'category':''.join(category),'content': ''.join(content),
            'what_new':''.join(what_new),'requirements':''.join(requirements),
        })

    def parse_url(self,response):
        category = response.meta.get('category')
        content = response.meta.get('content')
        what_new = response.meta.get('what_new')
        requirements = response.meta.get('requirements')
        print what_new,
        print requirements

        sel = Selector(response)



