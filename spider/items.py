# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    content = scrapy.Field()
    tag = scrapy.Field()

    category = scrapy.Field()
    
    logo_url = scrapy.Field()
    logos = scrapy.Field()


    what_new = scrapy.Field()
    requirements = scrapy.Field()

    screen = scrapy.Field()
    features = scrapy.Field()

    link1 = scrapy.Field()
    link2 = scrapy.Field()
    link3 = scrapy.Field()
    link4 = scrapy.Field()
    link5 = scrapy.Field()
    link6 = scrapy.Field()



