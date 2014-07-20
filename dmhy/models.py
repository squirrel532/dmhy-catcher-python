from django.db import models
import sys
import urllib3
from bs4 import BeautifulSoup
import re

#return an array of dictionary which contains two attributes, title & url.
#The attribute which names url is a relativity route. 
def Search( keywords ):
    page = urllib3.PoolManager()
    keywords = u"http://share.dmhy.org/topics/list?keyword={keyword}".format( keyword=keywords.replace( ' ', '+') )
    res = page.request( 'GET', keywords.encode('utf-8') )
    if res.status != 200 :
        return None

    parser = BeautifulSoup( res.data )
    table = parser.find( id='topic_list').tbody.find_all('tr')
    download_list = []
    
    for topic in table:
        date = topic.find(style="display: none;").get_text().encode("utf-8")
        source = topic.find( target="_blank" )
        while source.find('span') != None :
            source.span.unwrap()
        title = re.findall( r"\S+.*", source.get_text().encode('utf-8') )[0].decode("utf-8")
        download_list.append({ 'title':title, 'url':source['href'], 'date':date })
    return download_list

def GetMagnetLink( url ):
    page = urllib3.PoolManager()
    res = page.request( 'GET', url.encode('utf-8') )
    if res.status != 200:
        return None
    magnet = re.findall( r"magnet:[^\"\s<>]*", res.data )
    if len(magnet) != 0:
        return magnet[0]
    else:
        return None
        
class TransmissionAccount(models.Model):
    username = models.CharField( max_length=25)
    password = models.CharField( max_length=25)
    host     = models.CharField( max_length=25)
    port     = models.IntegerField( )
    
#Source
import transmissionrpc
class Source( models.Model ):
    id = models.AutoField( primary_key = True )
    tid = models.IntegerField( default = 0 )
    title = models.CharField( max_length = 255)
    uri = models.CharField( max_length = 255)
    magnet = models.CharField( max_length = 255)
    date = models.DateTimeField( auto_now = True, auto_now_add = True)
    status = models.IntegerField( default = 0 )# 0 means success
    def __str__(self):
        return self.title.encode('utf-8')
    def isExist( self ):
        return Source.objects.filter( uri=self.uri ).count( ) != 0
        
    def getMagnet( self ):
        m = GetMagnetLink( u'http://share.dmhy.org' + self.uri )
        if( m != None ):
            self.magnet = m
        return m
        
    def add( self):
        if( self.isExist() ):
            print "Ign: {title}".format( title = self.title )
            return 1
        else:
            self.getMagnet()
            print "Get: {title}".format( title = self.title )
            
            alias = Task.objects.get(tid=self.tid).alias
            try:
                t_account = TransmissionAccount.objects.get( id = 1 )            
            except:
                self.status = 1
                self.save()
                return 3
            try:
                t_rpc = transmissionrpc.Client( address=t_account.host, port=t_account.port, user=t_account.username, password=t_account.password )
            except transmissionrpc.error.TransmissionError:
                self.status = 1
                self.save()
                return 2
            else:
                directory = "/home/pydio/fileserver/BT/{alias}".format( alias = alias )
                res = t_rpc.add_torrent( self.magnet, download_dir = directory.encode("utf-8")  )
                self.save()
                return 0
            
#Task
import datetime
class Task( models.Model):
    tid = models.AutoField( primary_key = True)
    alias = models.CharField( max_length = 255)
    keywords = models.CharField( max_length = 255)
    first_topic = models.CharField( max_length = 255, default = "", blank = True )
    status = models.BooleanField( default = True)
    last_update = models.DateTimeField( auto_now_add = True)

    def executeTask( self ):
        print "Start to process task \"{alias}\"".format( alias = self.alias )
        topic_list = Search( self.keywords )
        print "We had found {num} topic(s)".format( num = str(len(topic_list)) )
        isupdate = False
        update_first_topic = ( self.first_topic == "" )
        for topic in topic_list:
            target = Source( tid=self.tid, uri=topic['url'], title=topic['title'] )
            if target.add() == 0:
                isupdate = True
            if topic['url'] == self.first_topic: break
            if update_first_topic: self.first_topic = topic['url']
        self.save()
        if isupdate :
            self.last_update = self.last_update.now()
            self.save()
