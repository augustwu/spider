# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
import MySQLdb
from datetime import datetime

mysql_con  = MySQLdb.connect(host='localhost',user='hiveuser',passwd='123456',db='wp')


class SpiderPipeline(object):

    

    def exists_item(self,title):
        sql = 'select count(0) from wp_posts where post_title=%s' % title 
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    
    def insert_item(self,item):
        sql = 'insert into wp_posts(post_author,post_date,post_date_gmt,post_content,
            post_title,post_excerpt,post_name,post_modified,
            post_modified_gmt,post_type) values 
            (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)' % (1,datetime.now(),datetime.now(),item.get('content'),item.get('full_name'),item.get('unique_name'),item.get('full_name'),datetime.now(),datetime.now(),'post')

        self.cursor.execute(sql)
        return self.cursor.fetchone()
        

    def exists_category(self,category):
        sql = 'select count(0) from wp_terms wher name=%s' % category
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def insert_category(self,item):
        sql = 'insert into wp_terms(name,slug) values(%s,%s)' % (item.get('category'),item.get('category'))
        self.cursor.execute(sql)
        return self.cursor.fetchone()
        
        

    def __init__(self):
        self.db = mysql_con
        self.cursor = db.cursor()

    def process_item(self, item, spider):
        title = item.get('full_name')
        category = item.get('category')
        if self.exists_item(title):
            pass
        else:
            self.insert_item(item)
            
      if not self.exists_category(category):
          self.insert_category(item)

      




  
