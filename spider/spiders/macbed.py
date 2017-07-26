#coding=utf-8

from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.selector import Selector
from spider.items import SpiderItem
 
 
class MacbedSpider(CrawlSpider):
    name = "macbed"
    download_delay = 1
    allowed_domains = ["macbed.com","www.macbed.com"]

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
        
        self.screen_urls = None
        self.screens = None

    def parse(self, response):
        sel = Selector(response)
        last_page = int(sel.xpath('//a[contains(@class,"page-numbers")]//text()')[-2].extract())
 
        for url in range(1,3):
            next_url =  "https://www.macbed.com/page/%s/" % str(url)
            yield Request(next_url, callback=self.parse_results)


    def parse_results(self,response):
        sel = Selector(response)

        urls = sel.xpath('//div[contains(@class, "entry")]//h2//a/@href')
        for url in urls[:4]:
            yield Request(url.extract(), callback=self.parse_product, meta={
                'splash': {
                    'args': {'wait': 0.5}},
                'url': url.extract()
            })


    def parse_product(self,response):
        sel = Selector(response)
        
        item = SpiderItem()

        self.category = sel.xpath('//div[contains(@class, "entry")]//div[contains(@class,"desc")]//a/text()')[1:].extract()
        self.tag = sel.xpath('//div[contains(@class, "entry")]//div[contains(@class,"tag")]//a/text()').extract()
        self.content = sel.xpath('//div[contains(@class, "article")]//div[contains(@class,"text")]//p|//div[contains(@class, "article")]//div[contains(@class,"text")]//ul|//div[contains(@class, "article")]//div[contains(@class,"text")]//h5|//div[contains(@class, "article")]//div[contains(@class,"text")]//h3[position() < 2]|//div[contains(@class, "article")]//div[contains(@class,"text")]//br')[1:].extract()
        self.content = sel.xpath('//div[contains(@class, "article")]//div[contains(@class,"text")]/*[not(@id="div-gpt-ad-1462783699686-0" or @class="appdl"  or self::a or self::script or @class="alignright" or @id="appked_link_39590")]')[1:].extract()

        what_new = sel.xpath('//div[contains(@class, "article")]//div[contains(@class,"text")]//p|//div[contains(@class, "article")]//div[contains(@class,"text")]//ul|//div[contains(@class, "article")]//div[contains(@class,"text")]//h3')[1:].extract()

        requirements = sel.xpath('//div[contains(@class, "article")]//div[contains(@class,"text")]//p|//div[contains(@class, "article")]//div[contains(@class,"text")]//ul|//div[contains(@class, "article")]//div[contains(@class,"text")]//h3')[1:].extract()

        download_url = sel.xpath('//div[contains(@class, "appdl")]//a/@href')
        name = sel.xpath('//div[contains(@class, "entry")]//h2//a/text()').extract()
		
		
        self.unique_name = name[0].replace(u'\u2013', '-').split('-')[0].strip()
        self.full_name = name[0].replace(u'\u2013', '-')
        
        print self.full_name	

        self.image_urls = sel.xpath('//div[contains(@class, "article")]//div[contains(@class,"text")]//p//img/@src').extract()

        self.file_urls  = sel.xpath('//div[contains(@class, "article")]//div[contains(@class,"text")]//img[1]').extract()
        self.screen_urls = ['http:%s'  % sel.xpath('//div[contains(@class, "article")]//div[contains(@class,"text")]//img/@src')[-2].extract()]

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
        
        try:
            link6 = sel.xpath('//div[contains(@class, "downloadlink")]//a/@href')[5].extract()
            link6_text = sel.xpath('//div[contains(@class, "downloadlink")]//a/text()')[5].extract()
          
        except IndexError,e:
            link6 = ''
            link6_text = ''

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
        
        item['screen_urls'] =  self.screen_urls
        item['tag'] = self.tag
        return item


