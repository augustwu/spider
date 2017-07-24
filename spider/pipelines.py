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
ip = 'http://192.168.3.50'

class SpiderPipeline(object):


    def exists_item(self,post_name):
	
        sql = u"select count(0) from wp_posts where post_name='%s'" % post_name
        self.cursor.execute(sql)
        item = self.cursor.fetchone()[0]
        return item 
    
    def exists_tag(self,tag):
        sql = "select count(0) from "

    def insert_item(self,item):
        new_id = self.cursor.lastrowid
        guid = '%s/?p=%s' % (ip,new_id+1)
        sql = u'''insert into wp_posts(post_author,post_content,
            post_title,post_excerpt,post_name,
            post_type,to_ping,pinged,post_content_filtered) values 
            (%s,%s,%s,%s,%s,%s,%s,%s,%s)'''

        #sql2 = u'''insert into wp_posts(post_author,post_date,post_date_gmt,post_content,
        #    post_title,post_excerpt,post_name,post_modified,
        #    post_modified_gmt,post_type,to_ping,pinged,post_content_filtered) values 
        #    ('%s','%s','%s',u"%s",'%s','%s','%s','%s','%s','%s','%s','%s','%s')''' % (1,datetime.now(),datetime.now(),MySQLdb.escape_string(''.join(item.get('content')).replace(u'\u2013', '-').replace(u'\u2019',',')) ,item.get('full_name').replace(u'\u2013', '-'),
        #    item.get('unique_name')[:50],item.get('unique_name').replace(' ','-').replace('.','-').replace(u'\u2013', '-'),datetime.now(),datetime.now(),'post','','','')
      

        content = MySQLdb.escape_string(''.join(item.get('content')).replace(u'\u2013', '-').replace(u'\u2019',','))
        post_title = MySQLdb.escape_string(item.get('full_name'))
        post_excerpt = MySQLdb.escape_string(item.get('unique_name')[:50])
        post_name = MySQLdb.escape_string(item.get('unique_name').replace(' ','-').replace('.','-'))

        self.cursor.execute(sql, (1,content,post_title, post_excerpt,post_name,'post','','','' ))

        last_id =   int(self.db.insert_id())
        update_sql = "update wp_posts set guid = '%s' where id=%s" % (guid,last_id)

        self.cursor.execute(update_sql)
        self.db.commit()
        return last_id
        

    def exists_category_tag(self,category):
        sql = "select count(0) from wp_terms where name='%s'" % category
        self.cursor.execute(sql)
	
        return self.cursor.fetchone()[0]

    def insert_category_tag(self,category):
        sql = "insert into wp_terms(name,slug) values('%s','%s')" % (category,category)
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

    
    def insert_term_taxonomy(self,term_id):
        sql = "insert into wp_term_taxonomy(term_id,taxonomy) values('%s','%s')" % (term_id,'category')
        self.cursor.execute(sql)
        self.db.commit()

    def select_category_id(self,category):
        sql = "select term_id from wp_terms where name='%s'" % category
        self.cursor.execute(sql)
        return self.cursor.fetchone()[0]

    
    def insert_wp_term_relationships(self,object_id,term_taxonomy_id):
        sql = "insert into wp_term_relationships(object_id,term_taxonomy_id) values (%s,%s)" % (object_id,term_taxonomy_id)
        print sql
        self.cursor.execute(sql)
        self.db.commit()

    def process_item(self, item, spider):
        title = item.get('full_name')
        print title
        category_list = item.get('category')
        post_name = item.get('unique_name').replace(' ','-').replace('.','-')
        
        if_exist = self.exists_item(post_name)
        
        tag_list = item.get('tag')
        item_id = None
        print item
        print '============'
        if not if_exist:
            item_id = self.insert_item(item)
            
        for category in category_list:
      	    if not self.exists_category_tag(category):
                self.insert_category_tag(category)
        for tag in tag_list:
            if not self.exists_category_tag(tag):
                self.insert_category_tag(tag)
      
        

        if not if_exist:
            for category in category_list: 
                print category
                category_id = self.select_category_tag_id(category)
                if category_id:
                    try:
                        self.insert_term_taxonomy_tag(category_id,'category')
                    except MySQLdb.IntegrityError:
                        pass
                    
                    self.insert_wp_term_relationships(item_id,category_id)

            for tag in tag_list:
                print tag
                tag_id = self.select_category_tag_id(tag)
                if tag_id:
                    try:
                        self.insert_term_taxonomy_tag(tag_id,'tag')
                    except MySQLdb.IntegrityError:
                        pass
                    
                    self.insert_wp_term_relationships(item_id,tag_id)
                    

            
    def insert_term_taxonomy_tag(self,term_id,type):
        sql = "insert into wp_term_taxonomy(term_id,taxonomy) values('%s','%s')" % (term_id,type)
        self.cursor.execute(sql)
        self.db.commit()

    def select_category_tag_id(self,category):
        sql = "select term_id from wp_terms where name='%s'" % category
        self.cursor.execute(sql)
        return self.cursor.fetchone()[0]

    
    def insert_wp_term_relationships(self,object_id,term_taxonomy_id):
        sql = "insert into wp_term_relationships(object_id,term_taxonomy_id) values (%s,%s)" % (object_id,term_taxonomy_id)
        self.cursor.execute(sql)
        self.db.commit()

  
