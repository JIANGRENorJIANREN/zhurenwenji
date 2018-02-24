#-*-coding:utf-8 -*-
import lxml.html
import urllib2
import pandas as pd


url_links = ['http://cd.lianjia.com/ershoufang/rs/']
for i in range(1,101):
    url_links.append('http://cd.lianjia.com/ershoufang/pg'+str(i))

columns = ['title','where','other','chanquan','price','price-pre','square']

#读取每页的html文件    
def scrapt_datas(url_page,user_agent,num_retrics):
    headers = {'User_agent':user_agent}
    request = urllib2.Request(url_page,headers=headers)
    try:
        html = urllib2.urlopen(request).read()
    except urllib2.URLError as e:
        print 'error'
        html = None
        if num_retrics > 0:
            if hasattr(e,'code') and 500<=e.code<600:
                return scrapt_datas(url_page,user_agent,num_retrics-1)
    tree = lxml.html.fromstring(html)
     
    td = pd.DataFrame(columns = ['title','where','other','chanquan','price','price-pre','square'])
     
    td['title'] = [tree.cssselect('ul#house-lst > li > .info-panel > h2')[index].text_content() for index in range(30)]
    td['where'] = [tree.cssselect('ul#house-lst > li > .info-panel > .col-1 > .where')[index].text_content() for index in range(30)]
    td['other'] = [tree.cssselect('ul#house-lst > li > .info-panel > .col-1 > .other')[index].text_content()  for index in range(30)]
    td['chanquan'] = [tree.cssselect('ul#house-lst > li > .info-panel > .col-1 > .chanquan')[index].text_content()  for index in range(30)]
    td['price'] = [tree.cssselect('ul#house-lst > li > .info-panel > .col-3 > .price')[index].text_content()  for index in range(30)]
    td['price-pre'] = [tree.cssselect('ul#house-lst > li > .info-panel > .col-3 > .price-pre')[index].text_content()  for index in range(30)]
    td['square'] = [tree.cssselect('ul#house-lst > li > .info-panel > .col-2 > .square')[index].text_content()  for index in range(30)]

    td.to_csv('d:/exercise/lianjia.csv',encoding = 'utf-8',mode = 'a')
    #title = td.text_content()
     
if __name__ == '__main__':
    print '下载链家房屋信息： '
    for url_mem in url_links:
        scrapt_datas(url_mem,'Mozilla/5.0',3)
