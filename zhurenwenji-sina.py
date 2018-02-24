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
        html = urllib2.urlopen(request).read().decode('utf-8')
        print html
    except urllib2.URLError as e:
        print 'download error:',e.reason
        html = None
        if num_retrics > 0:
            if hasattr(e,'code') and 500<=e.code<600:
                #recursively retry 5xx HTTP errors
                return download(url,user_agent,num_retrics-1)
    return html
    
def craw_sitemap(user_agent,num_retrics):
    doc = Document()
    f = open('d:\exercise\zhuren_sina_urls.txt','r')
    str = f.read()
    links = re.findall('<a href="(.*?)"',str)
    f.close()
    print len(links)
    td = ''
    i = 0
    for link in links:
        try:
            html = download(link,user_agent,num_retrics)
            #contents = re.findall('<div class="detail">(.*?)</div>',html)
            tree = lxml.html.fromstring(html)
            td = tree.cssselect('div.WBA_content')[0].text_content()
            i+=1
            print i
        except:
            pass
        doc.add_paragraph(td)
    doc.save('d:\exercise\zhurenwenji.docx')
    
if __name__ == '__main__':
    craw_sitemap('Mozilla/5.0 (Windows NT 6.1; WOW64)',2)