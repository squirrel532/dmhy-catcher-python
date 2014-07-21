import urllib3
from bs4 import BeautifulSoup
import re

#before you send the keyword into the function, Search(), please decode the keyword.
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

#Full url ( including http://... )
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
