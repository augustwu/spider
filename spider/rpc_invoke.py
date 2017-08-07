import urllib
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts
import xmlrpclib
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
import os
import datetime
import requests
########################### Read Me First ###############################
'''
------------------------------------------In DETAIL--------------------------------
Description
===========
Add new posts to WordPress remotely using Python using XMLRPC library provided by the WordPress.

Installation Requirement
************************
Verify you meet the following requirements
==========================================
Install Python 2.7 (Don't download 3+, as most libraries dont yet support version 3). 
Install from PyPI using easy_install python-wordpress-xmlrpc 
Easy_Install Link: https://pypi.python.org/pypi/setuptools
==========================================

Windows Installation Guide
==========================
-Download and Install Easy_Install from above Link -Extract Downloaded File and from CMD go to the extracted directory and run 'python setup.py install'. This will install easy_install. -Go to %/python27/script and run following command easy_install python-wordpress-xmlrpc

Ubuntu Installation Guide
=========================
sudo apt-get install python-setuptools 
sudo easy_install python-wordpress-xmlrpc

Note: Script has its dummy data to work initially which you can change or integrate with your code easily for making it more dynamic.

****************************************
For Bugs/Suggestions
contact@waqasjamal.com
****************************************
------------------------------------------In DETAIL--------------------------------		
'''
class Custom_WP_XMLRPC:
    def post_article(self,wpUrl,wpUserName,wpPassword,articleTitle, articleCategories, articleContent, articleTags,PhotoUrl,date,logo_name,post_name):
        self.path=os.path.join(os.getcwd(),"00000001.jpg")
        self.articlePhotoUrl=PhotoUrl
        self.wpUrl=wpUrl
        self.wpUserName=wpUserName
        self.wpPassword=wpPassword
        #Download File
        print self.articlePhotoUrl
        r = requests.get(self.articlePhotoUrl,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:16.0) Gecko/20100101 Firefox/16.0,gzip(gfe)'})
        #with open('test.jpg', "wb") as f:
        #    f.write(r.content)
        from PIL import Image
        from StringIO import StringIO
        content = r.content
        im = Image.open(StringIO(content))
        rgb_im = im.convert('RGB')
        self.path = os.path.join(os.getcwd(),'image',logo_name)
        print self.path
        rgb_im.save(self.path)

        #Upload to WordPress
        client = Client(self.wpUrl,self.wpUserName,self.wpPassword)
        filename = self.path
        

        # prepare metadata
        data = {'name': logo_name,'type': 'image/jpeg'}
        
        # read the binary file and let the XMLRPC library encode it into base64
        print filename
        with open(filename, 'rb') as img:
        	data['bits'] = xmlrpc_client.Binary(img.read())
        response = client.call(media.UploadFile(data))
        print 'aaaaaaaaaaaa'
        attachment_id = response['id']
        #Post
        post = WordPressPost()
        post.title = articleTitle

        try:
            post.date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
            post.date_modified = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
        except:
            post.date = datetime.datetime.strptime(date, "%Y-%m-%d")
            post.date_modified = datetime.datetime.strptime(date, "%Y-%m-%d")
        post.slug = post_name 
        post.comment_status ="open"
        
        post.content = articleContent
        post.terms_names = { 'post_tag': articleTags,'category': articleCategories}
        post.post_status = 'publish'
        post.thumbnail = attachment_id
        post.id = client.call(posts.NewPost(post))
        print 'Post Successfully posted. Its Id is: ',post.id


        if post.content.find('https://nmac.to') != -1:
            image = client.call(media.GetMediaItem(attachment_id))
            import re 
            post.content = re.sub(r'https://nmac.to(\S+).png',image.link,post.content) 
            client.call(posts.EditPost(post.id, post))
            print 'Post Successfully updated. Its Id is: ',post.id
            

        


#########################################
# POST & Wp Credentials Detail #
#########################################

#Url of Image on the internet
ariclePhotoUrl='http://i1.tribune.com.pk/wp-content/uploads/2013/07/584065-twitter-1375197036-960-640x480.jpg' 
# Dont forget the /xmlrpc.php cause thats your posting adress for XML Server
wpUrl='http://192.168.1.9/xmlrpc.php' 
#WordPress Username
wpUserName='wu'
#WordPress Password
wpPassword='1'
#Post Title
articleTitle='Testing Python Script version 3'
#Post Body/Description
articleContent='Final .... Testing Fully Automated'
#list of tags
articleTags=['code','python'] 
#list of Categories
articleCategories=['language','art'] 

#########################################
# Creating Class object & calling the xml rpc custom post Function
#########################################
#xmlrpc_object	=	Custom_WP_XMLRPC()
#On Post submission this function will print the post id
#xmlrpc_object.post_article(wpUrl,wpUserName,wpPassword,articleTitle, articleCategories, articleContent, articleTags,ariclePhotoUrl)
