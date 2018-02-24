import urllib2
import re
from docx import Document

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
    f = open(r'D:\exercise\zhurenwenji.txt','ab')
    #doc = Document()
    #extract the sitemap links
    links = re.findall('<a href="http:(.*?)" title="http',sitemap)
    #print links
    
    for link in links:
        link =  'http:' + link
        html = download(link,user_agent,num_retrics)
        contents = re.findall('<div class="detail">(.*?)</div>',html)
        #print contents
        #doc.add_paragraph(contents[0])
    #doc.save('d:\exercise\zhurenwenji.docx')
        f.write(contents[0])
    f.close()
    
if __name__ == '__main__':
    craw_sitemap('https://xueqiu.com/2054435398/32283614','wasp',2)