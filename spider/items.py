# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    unique_name = scrapy.Field()
    full_name= scrapy.Field()
    content = scrapy.Field()
    tag = scrapy.Field()
    post_time = scrapy.Field()

    category = scrapy.Field()
    
    image_urls = scrapy.Field()
    images = scrapy.Field()
    
    screen_urls = scrapy.Field()
    screens = scrapy.Field()
    
    file_urls = scrapy.Field()
    files = scrapy.Field()

    what_new = scrapy.Field()
    requirements = scrapy.Field()

    screen = scrapy.Field()
    features = scrapy.Field()

    link1 = scrapy.Field()
    link1_text = scrapy.Field()

    link2 = scrapy.Field()
    link2_text = scrapy.Field()

    link3 = scrapy.Field()
    link3_text = scrapy.Field()

    link4 = scrapy.Field()
    link4_text = scrapy.Field()

    link5 = scrapy.Field()
    link5_text = scrapy.Field()

    link6 = scrapy.Field()
    link6_text = scrapy.Field()



