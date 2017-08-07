# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
import MySQLdb
from datetime import datetime
import time
#mysql_con  = MySQLdb.connect(host='localhost',user='hiveuser',passwd='123456',db='wp')
mysql_con  = MySQLdb.connect(host='localhost',user='root',passwd='1',db='wp_2')
ip = 'http://192.168.1.9'
username = 'wu'
passwd = '1'
from rpc_invoke import Custom_WP_XMLRPC

class SpiderPipeline(object):


    def exists_item(self,post_name):
        sql = u"select count(0) from wp_posts where post_name='%s'" % post_name
        self.cursor.execute(sql)
        item = self.cursor.fetchone()[0]
        return item 
    

    def get_max_id(self,table):
        sql  = "select id from %s order by id desc limit 1" % table
        self.cursor.execute(sql)
        try:
            item = self.cursor.fetchone()[0]
        except:return 0
        return item
        
      
    def insert_post_media(self,post_id,meta_value):
        date_meta_value = '%s/%s/%s' % (datetime.now().strftime('%Y'),datetime.now().strftime('%m'),meta_value)
        sql = "insert into wp_postmeta(post_id,meta_key,meta_value) values ('%s','%s','%s')" % (post_id,'_wp_attached_file',date_meta_value)
        print meta_value.split('/')[-1].split('.')[0]
        print meta_value,date_meta_value
        print '-========='
        self.cursor.execute(sql)
        self.db.commit()
        
        sql2 = '''insert into wp_postmeta(post_id,meta_key,meta_value) values ('%s','%s','a:5:{s:5:"width";i:1188;s:6:"height";i:776;s:4:"file";s:54:"%s";s:5:"sizes";a:6:{s:9:"thumbnail";a:4:{s:4:"file";s:54:"%s.jpg";s:5:"width";i:150;s:6:"height";i:150;s:9:"mime-type";s:10:"image/jpeg";}s:6:"medium";a:4:{s:4:"file";s:54:"%s.jpg";s:5:"width";i:300;s:6:"height";i:196;s:9:"mime-type";s:10:"image/jpeg";}s:12:"medium_large";a:4:{s:4:"file";s:54:"%s.jpg";s:5:"width";i:768;s:6:"height";i:502;s:9:"mime-type";s:10:"image/jpeg";}s:5:"large";a:4:{s:4:"file";s:55:"%s.jpg";s:5:"width";i:1024;s:6:"height";i:669;s:9:"mime-type";s:10:"image/jpeg";}s:14:"post-thumbnail";a:4:{s:4:"file";s:54:"%s.jpg";s:5:"width";i:660;s:6:"height";i:431;s:9:"mime-type";s:10:"image/jpeg";}s:17:"excerpt-thumbnail";a:4:{s:4:"file";s:54:"%s.jpg";s:5:"width";i:200;s:6:"height";i:140;s:9:"mime-type";s:10:"image/jpeg";}}s:10:"image_meta";a:12:{s:8:"aperture";s:1:"0";s:6:"credit";s:0:"";s:6:"camera";s:0:"";s:7:"caption";s:0:"";s:17:"created_timestamp";s:1:"0";s:9:"copyright";s:0:"";s:12:"focal_length";s:1:"0";s:3:"iso";s:1:"0";s:13:"shutter_speed";s:1:"0";s:5:"title";s:0:"";s:11:"orientation";s:1:"0";s:8:"keywords";a:0:{}}}')''' % (post_id,'_wp_attachment_metadata',date_meta_value,meta_value.split('/')[-1].split('.')[0],meta_value.split('/')[-1].split('.')[0],meta_value.split('/')[-1].split('.')[0],meta_value.split('/')[-1].split('.')[0],meta_value.split('/')[-1].split('.')[0],meta_value.split('/')[-1].split('.')[0] )
        self.cursor.execute(sql2)
        self.db.commit()
        last_id =   int(self.cursor.lastrowid)
        return last_id

    def get_item(self,item):
        sql = u"select id from wp_posts where post_title='%s'" % item.get('full_name') 
        self.cursor.execute(sql)
        item = self.cursor.fetchone()[0]
        return item 

    def insert_item(self,item):
        new_id = self.get_max_id('wp_posts')

        guid = '%s/?p=%s' % (ip,new_id+1)
        sql = u'''insert into wp_posts(post_author,post_content,
            post_title,post_excerpt,post_name,
            post_type,to_ping,pinged,post_content_filtered,post_date,post_date_gmt,post_modified,post_modified_gmt,post_status) values 
            (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''


        content = ''.join(item.get('content')).replace(u'\u2013', '-').replace(u'\u2019',',').replace(u'\xae','@')
        post_title = item.get('full_name')
        post_excerpt = item.get('unique_name')[:200].split(']')[-1]
        post_name = item.get('unique_name').split(']')[-1].replace(' ','-').replace('.','-')

        post_time = item.get('post_time')
        print post_time
        print '~~~~~~~~~'

        self.cursor.execute(sql, (1,content,post_title, content[:200],post_name,'post','','','',post_time,post_time,post_time,post_time,'publish'))

        self.db.commit()
        last_id =   int(self.cursor.lastrowid)
        update_sql = "update wp_posts set guid = '%s' where id=%s" % (guid,last_id)

        self.cursor.execute(update_sql)
        self.db.commit()
        return last_id
        

    def exists_category_tag(self,category):
        print category
        print 'pppppppppppp'
        sql = 'select count(0) from wp_terms where name="%s"' % category
        self.cursor.execute(sql)
	
        return self.cursor.fetchone()[0]

    def insert_category_tag(self,category):
        sql = 'insert into wp_terms(name,slug) values("%s","%s")' % (category,category)
        self.cursor.execute(sql)
      	self.db.commit()

      	last_id =   int(self.cursor.lastrowid)
      	return last_id
         

    def __init__(self):
        self.db = mysql_con
        self.db.set_character_set('utf8')

        self.cursor = self.db.cursor()
        self.cursor.execute('SET NAMES utf8;')
        self.cursor.execute('SET CHARACTER SET utf8;')
        self.cursor.execute('SET character_set_connection=utf8;')

    
    def insert_term_taxonomy(self,term_id):
        sql = "insert into wp_term_taxonomy(term_id,taxonomy,count) values('%s','%s','%s')" % (term_id,'category',1)
        self.cursor.execute(sql)
        self.db.commit()

    def select_category_id(self,category):
        sql = "select term_id from wp_terms where name='%s'" % category
        self.cursor.execute(sql)
        return self.cursor.fetchone()[0]

    
    def insert_wp_term_relationships(self,object_id,term_taxonomy_id):
        sql = "insert into wp_term_relationships(object_id,term_taxonomy_id) values (%s,%s)" % (object_id,term_taxonomy_id)
        self.cursor.execute(sql)
        self.db.commit()

    
    def get_term_taxomomy_id(self,category,type):
        sql = "select * from wp_term_taxonomy where term_id=%s and taxonomy='%s'" % (category,type)
        self.cursor.execute(sql)
        return self.cursor.fetchone()[0]

    def process_item(self, item, spider):
        title = item.get('full_name')
        category_list = item.get('category')
        post_name = item.get('unique_name').split(']')[-1].replace(' ','-').replace('.','-')
        content = ''.join(item.get('content')).replace(u'\u2013', '-').replace(u'\u2019',',').replace(u'\xae','@')
        post_title = item.get('full_name')
        post_excerpt = item.get('unique_name')[:200].split(']')[-1]
        post_name = item.get('unique_name').split(']')[-1].replace(' ','-').replace('.','-')
        
        logo = item.get('image_urls')[0]    
        post_time = item.get('post_time')
        logo_name = logo.split('/')[-1]
        
        if_exist = self.exists_item(post_name)
        
        tag_list = item.get('tag')
        item_id = None
        xmlrpc_object   = Custom_WP_XMLRPC()

        if not if_exist:
            item_id = xmlrpc_object.post_article(ip+"/xmlrpc.php",username,passwd,title, category_list, content, tag_list,logo,post_time,logo_name,post_name)

      

    def insert_post_image(self,item_id,logo):
        full_logo = '%s/wp-content/uploads/%s/%s/%s' % (ip,datetime.now().strftime('%Y'),datetime.now().strftime('%m'),logo)
        logo_name = full_logo.split('/')[-1].split('.')[0]
        
        print full_logo 
        print '~~~~~~~~~~~'
        sql = '''insert into wp_posts(
            post_author,
            post_date,
            post_date_gmt,
            post_content,
            post_title,
            post_status,
            post_name,
            post_modified,
            post_modified_gmt,
            post_parent,
            guid,
            post_type,
            post_mime_type,post_excerpt,to_ping,pinged,post_content_filtered) 
            values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')''' % (1,datetime.now(),datetime.now(),'',logo_name,'inherit',logo_name,datetime.now(),datetime.now(),item_id, full_logo,'attachment','image/jpeg','','','','')
        self.cursor.execute(sql)
        print 'vvvvvvvvvvvvv'
        self.db.commit()
        last_id =   int(self.cursor.lastrowid)
        return last_id
            
    def insert_term_taxonomy_tag(self,term_id,type):
        sql = "insert into wp_term_taxonomy(term_id,taxonomy,count,description) values('%s','%s','%s','')" % (term_id,type,1)
        self.cursor.execute(sql)
        self.db.commit()
        last_id =   int(self.cursor.lastrowid)
        return last_id

    def select_category_tag_id(self,category):
        sql = "select term_id from wp_terms where name='%s'" % category
        self.cursor.execute(sql)
        return self.cursor.fetchone()[0]

    
    def insert_wp_term_relationships(self,object_id,term_taxonomy_id):
        try:        
          sql = "insert into wp_term_relationships(object_id,term_taxonomy_id) values (%s,%s)" % (object_id,term_taxonomy_id)
          self.cursor.execute(sql)
          self.db.commit()
        except MySQLdb.IntegrityError,e:
          print e

