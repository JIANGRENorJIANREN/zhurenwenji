import urllib2
import re
import lxml.html
from docx import Document
import os.path

def download(url,user_agent,num_retrics):
    print 'downloading the html '
    headers = {'User-agent':user_agent}
    request = urllib2.Request(url,headers=headers)
    try:
        html = urllib2.urlopen(request).read()
    except urllib2.URLError as e:
        print 'download error:',e.reason
        html = None
        if num_retrics > 0:
            if hasattr(e,'code') and 500<=e.code<600:
                #recursively retry 5xx HTTP errors
                return download(url,user_agent,num_retrics-1)
    return html
    
def craw_sitemap(url,user_agent,num_retrics):
    #download the sitemap file
    sitemap = download(url,user_agent,num_retrics)
    #f = open(r'D:\exercise\zhurenwenji.txt','w')
    doc = Document()
    
    #extract the sitemap links
    links = re.findall('<a href="http:(.*?)" title="http',sitemap)
    #print links
    i = 0
    print len(links)
    for link in links:
        link =  'http:' + link
        try:
            html = download(link,user_agent,num_retrics)
            #contents = re.findall('<div class="detail">(.*?)</div>',html)
            tree = lxml.html.fromstring(html.decode('utf-8'))
            td = tree.cssselect('div.detail')[0].text_content()
            i+=1
            print i
        except:
            pass
        #doc.save(contents)
        doc.add_paragraph(td)
    doc.save('d:\exercise\zhurenwenji.docx')
    
if __name__ == '__main__':
    craw_sitemap('http://weibo.com/ttarticle/p/show?id=2309403992433556850854','Mozilla/5.0 (Windows NT 6.1; WOW64)',2)