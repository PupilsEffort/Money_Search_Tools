import requests
import threading
from bs4 import BeautifulSoup
import re
import time

url = input( 'url(如baidu.com): ' )

head={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'}
ip = 'http://site.ip138.com/{}'.format( url )
# domain_url = url.split('.')
# domain_url = domain_url[1]+'.'+domain_url[2]
domain_url = url
domain = 'http://site.ip138.com/{}/domain.htm'.format( domain_url )
t = time.strftime("%Y-%m-%d"+'_', time.localtime())
html_file = open( url+'_'+t+'.html','w' )
html_file.write( '''
	
<head>

<title>%s的扫描结果</title>
<link rel="stylesheet" href="https://cdn.staticfile.org/twitter-bootstrap/3.3.7/css/bootstrap.min.css">
<script src="https://cdn.staticfile.org/jquery/2.1.1/jquery.min.js"></script>
<script src="https://cdn.staticfile.org/twitter-bootstrap/3.3.7/js/bootstrap.min.js"></script>
<style>

pre{

margin: 0 0 0px;

}

</style>
</head>

<ul id="myTab" class="nav nav-tabs navbar-fixed-top navbar navbar-default">
    <li class="active">
        <a href="#ip" data-toggle="tab">
             IP历史解析
        </a>
    </li>
    <li><a href="#cms" data-toggle="tab">CMS识别</a></li>
    <li><a href="#domain" data-toggle="tab">子域名信息</a></li>
</ul>
<br>
<br>
<br>
<br>
<div id="myTabContent" class="tab-content">
'''%url )

class IP( threading.Thread ):
    def __init__(self, ip):
        threading.Thread.__init__(self)
        self.ip = ip
    def run(self):
        r = requests.get( self.ip,headers = head )
        html = r.text
        bs = BeautifulSoup(html, "html.parser")
        html_file.write('<div class="tab-pane fade in active" id="ip">')
        for i in bs.find_all('p'):
            ipc = i.get_text()
            ip_html = '<pre>{}</pre>'.format( ipc )
            html_file.write( ip_html )
        html_file.write('</div>')

class CMS( threading.Thread ):
    def __init__(self, cms):
        threading.Thread.__init__(self)
        self.cms = cms
    def run(self):
        cms = requests.post('http://whatweb.bugscaner.com/what/', data={'url': self.cms}, headers = head)
        text = cms.text
        Web_Frameworks = re.search('"Web Frameworks": "(.*?)"]', text)
        Programming_Languages = re.search('"Programming Languages":(.*?)"]', text)
        JavaScript_Frameworks = re.search('"JavaScript Frameworks": (.*?)"]', text)
        CMS = re.search('"CMS": (.*?)"]', text)
        Web_Server = re.search('"Web Servers": (.*?)"]', text)
        if CMS:
            CMS = CMS.group(1)+'"]'
        if Programming_Languages:
            Programming_Languages = Programming_Languages.group(1)+'"]'
        if JavaScript_Frameworks:
            JavaScript_Frameworks = JavaScript_Frameworks.group(1)+'"]'
        if Web_Frameworks:
            Web_Frameworks = Web_Frameworks.group(1)+'"]'
        if Web_Server:
            Web_Server = Web_Server.group(1)+'"]'
        html = '''
        <div class="tab-pane fade" id="cms">
        <div class="table-responsive">
        <table class="table table-condensed">
           <tr>
            <th>web框架</th>
            <th>脚本版本</th>
            <th>JavaScript框架</th>
            <th>CMS框架</th>
            <th>web服务器</th>
          </tr>
          <tr>
            <td>{0}</td>
            <td>{1}</td>
            <td>{2}</td>
            <td>{3}</td>
            <td>{4}</td>
          </tr>
        </table>
        </div>
        </div>
        '''.format(Web_Frameworks,Programming_Languages,JavaScript_Frameworks,CMS,Web_Server)
        html_file.write( html )

class DOMAIN( threading.Thread ):
    def __init__(self, domain):
        threading.Thread.__init__(self)
        self.domain = domain
    def run(self):
        r = requests.get( self.domain,headers = head )
        html = r.text
        bs = BeautifulSoup(html, "html.parser")
        html_file.write('<div class="tab-pane fade in active" id="domain"')
        num = 0
        for i in bs.find_all('p'):
            num += 1
            html_file.write( '<br>' )
            domainc = i.get_text()
            domain_html = '<pre>[{}]： {}</pre>'.format( num,domainc )
            html_file.write( domain_html )
            print( domain_html )
        html_file.write('</div>')

ip_cls = IP(ip)
ip_html = ip_cls.run()

cms_cls = CMS(url)
cms_html = cms_cls.run()

domain_cls = DOMAIN( domain )
domain_html = domain_cls.run()