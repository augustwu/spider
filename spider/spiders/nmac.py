#coding=utf-8

from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.selector import Selector
from spider.items import SpiderItem
 
ip = "http://192.168.1.9"
 
class NmacSpider(CrawlSpider):
    name = "nmac"
    download_delay = 1
    allowed_domains = ["nmac.to","www.nmac.to"]

    start_urls = [
        "https://www.nmac.to/"
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
        last_page = int(sel.xpath('//div[contains(@class,"sort-buttons")]//a/@data-paginated')[-1].extract())
 
        for index,url in enumerate(range(1,402)):
            next_url =  "https://nmac.to/page/%s/" % str(url)
            yield Request(next_url, callback=self.parse_results,priority=index)


    def parse_results(self,response):
        sel = Selector(response)

        urls = sel.xpath('//div[contains(@class, "article-excerpt")]//h2//a/@href')
        for index,url in enumerate(urls):
            yield Request(url.extract(), callback=self.parse_product,priority=index, meta={
                'splash': {
                    'args': {'wait': 0.5}},
                'url': url.extract()
            })


    def parse_product(self,response):
        sel = Selector(response)
        
        item = SpiderItem()

        category = sel.xpath('//div[contains(@class, "category-list")]//a/text()')[-1].extract()
        tag = sel.xpath('//div[contains(@class,"post-tags-wrapper")]//div[contains(@class,"post-tags")]//a/text()').extract()

        content = sel.xpath('//div[contains(@class, "the-content")]/*[not(@class="nmac-before-content"  or self::a or self::script or @class="nmac-after-content" or @class="adsbygoogle" or @id="aswift_2_expand" or class="alert fade in alert-error" or class="wp-image-3333" or @style="text-align: center; width: 40%; margin-left: 30%;" or @style="text-align: center" or @style="text-align: center;" or  @class="alert fade in alert-error" or @style="text-align: left;" or @class="alert fade in alert-error " or @style="text-align: center; width: 100%;" or @class="size-full")]').extract()



        download_url = sel.xpath('//div[contains(@class, "the-content")]//a[contains(@class,"btn-block")]/@href').extract()
        name = sel.xpath('//div[contains(@class, "main-content")]//h1/text()').extract()
		
        unique_name = name[0].replace(u'\u2013', '-').split('-')[0].strip()
        full_name = name[0].replace(u'\u2013', '-').strip()
        post_time = sel.xpath('//div[contains(@class,"meta-data")]//span[contains(@class,"date")]/text()')[-1].extract().split('\n')[-1].strip()
        

        image_urls = sel.xpath('//div[contains(@class, "the-content")]//img[contains(@class,"alignright")]/@src').extract()
        
        item['unique_name'] = unique_name
        item['full_name'] = full_name
        item['content'] = content 
        item['category'] = [category]

        item['image_urls'] =image_urls
        
        item['tag'] = tag
        item['post_time'] = post_time
        
        for index,d_url in enumerate(download_url):
            if index == 0:
                request =  Request(d_url, callback=self.parse_download_link_1, meta={
                    "download_url":download_url,'item':item
                })
                yield request
            
                
        
       # print item.get('link1')
       # print '======='
       # if item['link1']:
       #     content_added = '%s<a class="btn btn-small  btn-block"  href="%s" target="_blank">%s</a><br> ' % (content_added,link1,link1_text)
       # if item['link2']:
       #     content_added = '%s<a class="btn btn-small  btn-block" href="%s" target="_blank">%s</a><br> ' % (content_added,link2,link2_text)
       #     
       # if item['link3']:
       #     content_added = '%s<a class="btn btn-small  btn-block"  href="%s" target="_blank">%s</a><br>' % (content_added,link3,link3_text)
       # if item['link4']:
       #     content_added = '%s<a class="btn btn-small  btn-block"  href="%s" target="_blank">%s</a><br>' % (content_added,link4,link4_text)

       # if item['link5']:
       #     content_added = '%s<a class="btn btn-small  btn-block"  href="%s" target="_blank">%s</a><br>' % (content_added,link5,link5_text)

        
       # content_added = '%s%s' % (content_added,'</div>')
     #   item['unique_name'] = unique_name
     #   item['full_name'] = full_name
     #   item['content'] = content 
     #   item['category'] = category
#
     #   item['image_urls'] =image_urls
     #   
     #   item['tag'] = tag
     #   item['post_time'] = post_time
     #   return item
         


    def parse_download_link_1(self,response):
        sel = Selector(response)
        download_url = sel.xpath('//div[contains(@style,"text-align: center; width: 40%; margin-left: 30%;")]//a/@href')[0].extract()
        download_text = download_url.split('//')[-1].split('/')[0]
        
        item = response.meta['item']
        item['link1'] = download_url
        item['link1_text'] = download_text
        print download_url,download_text
        download_url = response.meta['download_url']
        request =  Request(download_url[1], callback=self.parse_download_link_2, meta={'item':item,'download_url':download_url})
        yield request
        
        
        
        

    def parse_download_link_2(self,response):
        sel = Selector(response)
        download_url = sel.xpath('//div[contains(@style,"text-align: center; width: 40%; margin-left: 30%;")]//a/@href')[0].extract()
        download_text = download_url.split('//')[-1].split('/')[0]
        
        item = response.meta['item']
        item['link2'] = download_url
        item['link2_text'] = download_text
        download_url = response.meta['download_url']
        request =  Request(download_url[2], callback=self.parse_download_link_3, meta={'item':item,'download_url':download_url})
        yield request

    def parse_download_link_3(self,response):
        sel = Selector(response)
        download_url = sel.xpath('//div[contains(@style,"text-align: center; width: 40%; margin-left: 30%;")]//a/@href')[0].extract()
        download_text = download_url.split('//')[-1].split('/')[0]
        
        item = response.meta['item']
        item['link3'] = download_url
        item['link3_text'] = download_text
        download_url = response.meta['download_url']
        request =  Request(download_url[3], callback=self.parse_download_link_4, meta={'item':item,'download_url':download_url})
        yield request

    def parse_download_link_4(self,response):
        sel = Selector(response)
        download_url = sel.xpath('//div[contains(@style,"text-align: center; width: 40%; margin-left: 30%;")]//a/@href')[0].extract()
        download_text = download_url.split('//')[-1].split('/')[0]
        
        item = response.meta['item']
        item['link4'] = download_url
        item['link4_text'] = download_text
        download_url = response.meta['download_url']
        request =  Request(download_url[4], callback=self.parse_download_link_5, meta={'item':item,'download_url':download_url})
        yield request
      
       
    def parse_download_link_5(self,response):
        sel = Selector(response)
        download_url = sel.xpath('//div[contains(@style,"text-align: center; width: 40%; margin-left: 30%;")]//a/@href')[0].extract()
        download_text = download_url.split('//')[-1].split('/')[0]
        
        item = response.meta['item']
        item['link5'] = download_url
        item['link5_text'] = download_text
        download_url = response.meta['download_url']
        print '444444444444'

        link1 = item.get('link1')
        link1_text = item.get('link1_text')        
 
        link2 = item.get('link2')
        link2_text = item.get('link2_text')        

        link3 = item.get('link3')
        link3_text = item.get('link3_text')        

        link4 = item.get('link4')
        link4_text = item.get('link4_text')        

        link5 = item.get('link5')
        link5_text = item.get('link5_text')        
        
        image_url = item.get('image_urls')
        
        import re
        content = item.get('content')
        content_added = '''%s<br><h3>%s</h3><br><div>
        '''  % (''.join(content),'Download Now From FreeMac')
        
        #content_added = re.sub(r'https://nmac.to(\S+).png',image_url[0],content_added)

        if link1:
            content_added = '%s<a class="btn btn-small  btn-block"  href="%s" target="_blank">%s</a><br> ' % (content_added,link1,link1_text)
        if link2:
            content_added = '%s<a class="btn btn-small  btn-block" href="%s" target="_blank">%s</a><br> ' % (content_added,link2,link2_text)
            
        if link3:
            content_added = '%s<a class="btn btn-small  btn-block"  href="%s" target="_blank">%s</a><br>' % (content_added,link3,link3_text)
        if link4:
            content_added = '%s<a class="btn btn-small  btn-block"  href="%s" target="_blank">%s</a><br>' % (content_added,link4,link4_text)

        if link5:
            content_added = '%s<a class="btn btn-small  btn-block"  href="%s" target="_blank">%s</a><br>' % (content_added,link5,link5_text)

        item['content'] = content_added 
        return item


