#coding=utf-8

from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.selector import Selector
from spider.items import SpiderItem
 

 
class MacbedSpider(CrawlSpider):
    name = "macbed"
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
 
        for index,url in enumerate(range(1,2)):
            next_url =  "https://nmac.to/page/%s/" % str(url)
            yield Request(next_url, callback=self.parse_results,priority=index)


    def parse_results(self,response):
        sel = Selector(response)

        urls = sel.xpath('//div[contains(@class, "article-excerpt")]//h2//a/@href')
        for index,url in enumerate(urls[:2]):
            yield Request(url.extract(), callback=self.parse_product,priority=index, meta={
                'splash': {
                    'args': {'wait': 0.5}},
                'url': url.extract()
            })


    def parse_product(self,response):
        sel = Selector(response)
        
        item = SpiderItem()

        category = sel.xpath('//div[contains(@class, "category-list")]//a/text()')[-1].extract()
        tag = sel.xpath('div[contains(@class,"post-tags")]//a/text()').extract()

        content = sel.xpath('//div[contains(@class, "the-content")]/*[not(@class="nmac-before-content"  or self::a or self::script or @class="nmac-after-content" or @class="adsbygoogle" or @id="aswift_2_expand" or class="alert fade in alert-error" or class="wp-image-3333" or @style="text-align: center; width: 40%; margin-left: 30%;" or @style="text-align: center" or @style="text-align: center;" or  @class="alert fade in alert-error" or @style="text-align: left;" or @class="alert fade in alert-error " or @style="text-align: center; width: 100%;")]')[1:].extract()



        download_url = sel.xpath('//div[contains(@class, "the-content")]//a[contains(@class,"btn-block")]/@href').extract()
        name = sel.xpath('//div[contains(@class, "main-content")]//h1/text()').extract()
		
        print name	
        unique_name = name[0].replace(u'\u2013', '-').split('-')[0].strip()
        full_name = name[0].replace(u'\u2013', '-')
        post_time = sel.xpath('//div[contains(@class,"meta-data")]//span[contains(@class,"date")]/text()')[-1].extract().strip()[6:]
        print post_time
        print '======='
        print full_name,unique_name,name,category
        print content
        

        image_urls = sel.xpath('//div[contains(@class, "the-content")]//img[contains(@class,"size-full")]/@src')[0].extract()
        print image_urls
        print download_url
        #file_urls  = sel.xpath('//div[contains(@class, "article")]//div[contains(@class,"text")]//img[1]').extract()
        #screen_urls = sel.xpath('//div[contains(@class, "article")]//div[contains(@class,"text")]//img/@src')[-2].extract()
        #if screen_urls.startswith('http'):
        #    screen_urls = ['%s' % screen_urls]
        #else:
        #    screen_urls = ['http:%s' % screen_urls]
        
        #for d_url in download_url:
        #    request =  Request(d_url, callback=self.parse_link, meta={
        #        'splash': {
        #            'args': {'wait': 0.5}},
        #    })
        #
        #request.meta['category'] = category
        #request.meta['content'] = ''.join(content)
        #request.meta['tag'] = tag 
        #request.meta['unique_name'] = unique_name
        #request.meta['full_name'] = full_name
        #request.meta['image_urls'] = image_urls
        ##request.meta['file_urls'] = file_urls

        ##request.meta['screen_urls'] =screen_urls
        #request.meta['post_time'] = post_time

        return request

    def parse_link(self,response):

        item = SpiderItem()

        unique_name = response.meta['unique_name']
        full_name = response.meta['full_name']
        content = response.meta['content']
        category = response.meta['category']
        
        post_time = response.meta['post_time']
        #file_urls = response.meta['file_urls']
        #screen_urls = response.meta['screen_urls']
        image_urls = response.meta['image_urls']
        tag = response.meta['tag']

        print unique_name
        print '------'
        sel = Selector(response)

        try:
            link1 = sel.xpath('//div[contains(@class, "downloadlink")]//a/@href')[0].extract()
            link1_text = sel.xpath('//div[contains(@class, "downloadlink")]//a/text()')[0].extract()
        except IndexError,e:
            link1 = ''
            link1_text = ''
            f = open('no_link.html','a')
            f.write('%s\n' % full_name)
            f.close()
        
        try:
            link2 = sel.xpath('//div[contains(@class, "downloadlink")]//a/@href')[1].extract()
            link2_text = sel.xpath('//div[contains(@class, "downloadlink")]//a/text()')[1].extract()
        except:
            link2 = ''
            link2_text = ''
        try:
            link3 = sel.xpath('//div[contains(@class, "downloadlink")]//a/@href')[2].extract()
            link3_text = sel.xpath('//div[contains(@class, "downloadlink")]//a/text()')[2].extract()
        except:
            link3 = ''
            link3_text = ''

        try:
            link4 = sel.xpath('//div[contains(@class, "downloadlink")]//a/@href')[3].extract()
            link4_text = sel.xpath('//div[contains(@class, "downloadlink")]//a/text()')[3].extract()

        except:
            link4 = ''
            link4_text = ''
        try:
            link5 = sel.xpath('//div[contains(@class, "downloadlink")]//a/@href')[4].extract()
            link5_text = sel.xpath('//div[contains(@class, "downloadlink")]//a/text()')[4].extract()
        except IndexError,e:

            link5 = ''
            link5_text = ''
        
        try:
            link6 = sel.xpath('//div[contains(@class, "downloadlink")]//a/@href')[5].extract()
            link6_text = sel.xpath('//div[contains(@class, "downloadlink")]//a/text()')[5].extract()
          
        except IndexError,e:
            link6 = ''
            link6_text = ''

        content_added = '''%s<br><h3>%s</h3><br><div>
        '''  % (content,'Download Now From FreeMac')

        if link2:
            content_added = '%s<a class="btn btn-small  btn-block" href="%s" target="_blank">%s</a><br> ' % (content_added,link2,link2_text)
            
        if link3:
            content_added = '%s<a class="btn btn-small  btn-block"  href="%s" target="_blank">%s</a><br>' % (content_added,link3,link3_text)
        if link4:
            content_added = '%s<a class="btn btn-small  btn-block"  href="%s" target="_blank">%s</a><br>' % (content_added,link4,link4_text)

        if link5:
            content_added = '%s<a class="btn btn-small  btn-block"  href="%s" target="_blank">%s</a><br>' % (content_added,link5,link5_text)
        if link6:
            content_added = '%s<a class="btn btn-small  btn-block"  href="%s" target="_blank">%s</a><br>' % (content_added,link6,link6_text)
        if link1:
            content_added = '%s<a class="btn btn-small  btn-block"  href="%s" target="_blank">%s</a><br> ' % (content_added,link1,link1_text)

        
        content_added = '%s%s' % (content_added,'</div>')
            
        if (link1 == '' and link2 =='' and link3 =='' and link4 =='' and link5 =='' and link6 ==''):
            return None 
        for cat in category:
            if cat.find('LIMIT') != -1: 
                return None
        else:
            item['unique_name'] = unique_name
            item['full_name'] = full_name
            item['content'] = content_added
            item['category'] = category

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
            item['image_urls'] =image_urls
            item['file_urls'] = file_urls
            
            item['screen_urls'] =  screen_urls
            item['tag'] = tag
            item['post_time'] = post_time
            return item


