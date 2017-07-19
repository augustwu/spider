# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
import MySQLdb
from datetime import datetime

#mysql_con  = MySQLdb.connect(host='localhost',user='hiveuser',passwd='123456',db='wp')
mysql_con  = MySQLdb.connect(host='localhost',user='root',passwd='1',db='wp')


class SpiderPipeline(object):

    

    def exists_item(self,title):
	
        sql = u"select count(0) from wp_posts where post_title='%s'" % title
        self.cursor.execute(sql)
        return self.cursor.fetchone()[0]

    
    def insert_item(self,item):
        sql = '''insert into wp_posts(post_author,post_date,post_date_gmt,post_content,
            post_title,post_excerpt,post_name,post_modified,
            post_modified_gmt,post_type,to_ping,pinged,post_content_filtered) values 
            ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')''' % (1,datetime.now(),datetime.now(),'<br>'.join(item.get('content')),item.get('full_name'),item.get('unique_name'),item.get('full_name'),datetime.now(),datetime.now(),'post','','','')

	print sql
        self.cursor.execute(sql)
	print int(self.db.insert_id())
	print '=============='
	last_id =   int(self.db.insert_id())
	self.db.commit()
	return last_id
        

    def exists_category(self,category):
        sql = "select count(0) from wp_terms where name='%s'" % category
        self.cursor.execute(sql)
	
        return self.cursor.fetchone()[0]

    def insert_category(self,item):
        sql = "insert into wp_terms(name,slug) values('%s','%s')" % (item.get('category'),item.get('category'))
        self.cursor.execute(sql)
	last_id =   int(self.db.insert_id())
	self.db.commit()
	return last_id
        
        
    def exists_term_rel(self):
	pass

    def __init__(self):
        self.db = mysql_con
	self.db.set_character_set('utf8')

        self.cursor = self.db.cursor()
	self.cursor.execute('SET NAMES utf8;')
	self.cursor.execute('SET CHARACTER SET utf8;')
	self.cursor.execute('SET character_set_connection=utf8;')

    def process_item(self, item, spider):
        title = item.get('full_name')
        category = item.get('category')
        if not self.exists_item(title):
            self.insert_item(item)
            
      	if not self.exists_category(category):
            self.insert_category(item)


      




  
