#coding=utf-8

from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.selector import Selector
from spider.items import SpiderItem
 
 
class MacbedSpider(CrawlSpider):
    name = "macbed"
    download_delay = 1
    allowed_domains = ["macbed.com","www.macbed.com"]
    #start_urls = [
    #    "https://www.macbed.com/page/%s/"  % page for page in range(10000,1,-1)
    #]

    start_urls = [
        "https://www.macbed.com/"
    ]


    def __init__(self):
        self.category = None
        self.name = None
        self.tag = None
        self.content = None

        self.image_urls = None
        self.images = None
        self.unique_name = None
        self.full_name = None

    def parse(self, response):
        sel = Selector(response)
        last_page = int(sel.xpath('//a[contains(@class,"page-numbers")]//text()')[-2].extract())
 
        for url in range(1,3):
            next_url =  "https://www.macbed.com/page/%s/" % str(url)
            yield Request(next_url, callback=self.parse_results)


    def parse_results(self,response):
        sel = Selector(response)

        urls = sel.xpath('//div[contains(@class, "entry")]//h2//a/@href')
        for url in urls[:1]:
            yield Request(url.extract(), callback=self.parse_product, meta={
                'splash': {
                    'args': {'wait': 0.5}},
                'url': url.extract()
            })


    def parse_product(self,response):
        sel = Selector(response)
        
        item = SpiderItem()

        self.category = sel.xpath('//div[contains(@class, "entry")]//div[contains(@class,"desc")]//a/text()')[-1].extract()
        self.content = sel.xpath('//div[contains(@class, "article")]//div[contains(@class,"text")]//p|//div[contains(@class, "article")]//div[contains(@class,"text")]//ul|//div[contains(@class, "article")]//div[contains(@class,"text")]//h5|//div[contains(@class, "article")]//div[contains(@class,"text")]//h3[position() < 2]|//div[contains(@class, "article")]//div[contains(@class,"text")]//br')[1:].extract()

        what_new = sel.xpath('//div[contains(@class, "article")]//div[contains(@class,"text")]//p|//div[contains(@class, "article")]//div[contains(@class,"text")]//ul|//div[contains(@class, "article")]//div[contains(@class,"text")]//h3')[1:].extract()

        requirements = sel.xpath('//div[contains(@class, "article")]//div[contains(@class,"text")]//p|//div[contains(@class, "article")]//div[contains(@class,"text")]//ul|//div[contains(@class, "article")]//div[contains(@class,"text")]//h3')[1:].extract()

        download_url = sel.xpath('//div[contains(@class, "appdl")]//a/@href')
        name = sel.xpath('//div[contains(@class, "entry")]//h2//a/text()').extract()
        print name
        self.unique_name = name[0].split(u'\u2013')[0].strip()
        self.full_name = name[0]

        self.image_urls = sel.xpath('//div[contains(@class, "article")]//div[contains(@class,"text")]//p//img/@src').extract()

        file_urls  = sel.xpath('//div[contains(@class, "article")]//div[contains(@class,"text")]//img/@src').extract()
        for index,url in enumerate(file_urls):
            if index == 1 and  url.startswith('http'):
                self.file_urls = url
                break
        print '========='
        print self.file_urls

        return [Request(download_url.extract()[0], callback=self.parse_link, meta={
            'splash': {
                'args': {'wait': 0.5}},
        })]

    def parse_link(self,response):

        item = SpiderItem()
        sel = Selector(response)

        link1 = sel.xpath('//div[contains(@class, "downloadlink")]//a/@href')[0].extract()
        link1_text = sel.xpath('//div[contains(@class, "downloadlink")]//a/text()')[0].extract()


        link2 = sel.xpath('//div[contains(@class, "downloadlink")]//a/@href')[1].extract()
        link2_text = sel.xpath('//div[contains(@class, "downloadlink")]//a/text()')[1].extract()

        link3 = sel.xpath('//div[contains(@class, "downloadlink")]//a/@href')[2].extract()
        link3_text = sel.xpath('//div[contains(@class, "downloadlink")]//a/text()')[2].extract()


        link4 = sel.xpath('//div[contains(@class, "downloadlink")]//a/@href')[3].extract()
        link4_text = sel.xpath('//div[contains(@class, "downloadlink")]//a/text()')[3].extract()

        link5 = sel.xpath('//div[contains(@class, "downloadlink")]//a/@href')[4].extract()
        link5_text = sel.xpath('//div[contains(@class, "downloadlink")]//a/text()')[4].extract()

        link6 = sel.xpath('//div[contains(@class, "downloadlink")]//a/@href')[5].extract()
        link6_text = sel.xpath('//div[contains(@class, "downloadlink")]//a/text()')[5].extract()


        item['unique_name'] = self.unique_name
        item['full_name'] = self.full_name
        item['content'] = self.content
        item['category'] = self.category

        item['link1'] = link1
        item['link1_text'] = link1_text
        item['link2'] = link2
        item['link2_text'] = link2_text

        item['link3'] = link3
        item['link3_text'] = link3_text

        item['link4'] = link4
        item['link4_text'] = link4_text

        item['link5'] = link5
        item['link5_text'] = link5_text

        item['link6'] = link6
        item['link6_text'] = link6_text
        item['image_urls'] = self.image_urls
        item['file_urls'] = self.file_urls
        print item
        return item


