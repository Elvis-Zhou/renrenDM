#encoding=utf-8
from sgmllib import SGMLParser
import sys,urllib2,urllib,cookielib
class spider(SGMLParser):
    def __init__(self,email,password):
        SGMLParser.__init__(self)
        self.h3=False
        self.h3_is_ready=False
        self.div=False
        self.h3_and_div=False
        self.a=False
        self.depth=0
        self.names=""
        self.dic={}

        self.email=email
        self.password=password
        self.domain='renren.com'
        try:
            cookie=cookielib.CookieJar()
            cookieProc=urllib2.HTTPCookieProcessor(cookie)
        except:
            raise
        else:
            opener=urllib2.build_opener(cookieProc)
            urllib2.install_opener(opener)

    def login(self):
        url='http://www.renren.com/PLogin.do'
        postdata={
            'email':self.email,
            'password':self.password,
            'domain':self.domain
        }
        req=urllib2.Request(
            url,
            urllib.urlencode(postdata)
        )

        self.file=urllib2.urlopen(req).read()
        url="http://status.renren.com/GetHotDoing.do?word=%E4%BF%9D%E9%92%93%E4%BA%BA%E5%A3%AB%E7%99%BB%E5%B2%9B%E6%88%90%E5%8A%9F"
        htmlfile=urllib2.urlopen(url).read()
        print htmlfile
        #url2="http://status.renren.com/GetHotDoing.do?word=你最想看的价格战"
        #htmlfile2=urllib2.urlopen(url).read()
        #print htmlfile2
#print self.file
    def start_h3(self,attrs):
        self.h3 = True
    def end_h3(self):
        self.h3=False

    def start_a(self,attrs):
        if self.h3 or self.div:
            self.a=True
    def end_a(self):
        self.a=False

    def start_div(self,attrs):
        if self.h3_is_ready == False:
            return
        if self.div==True:
            self.depth += 1

        for k,v in attrs:
            if k == 'class' and v == 'content':
                self.div=True;
                self.h3_and_div=True   #h3 and div is connected
    def end_div(self):
        if self.depth == 0:
            self.div=False
            self.h3_and_div=False
            self.h3_is_ready=False
            self.names=""
        if self.div == True:
            self.depth-=1
    def handle_data(self,text):
        #record the name
        if self.h3 and self.a:
            self.names+=text
            #record says
        if self.h3 and (self.a==False):
            if not text:pass
            else: self.dic.setdefault(self.names,[]).append(text)
            return
        if self.h3_and_div:
            self.dic.setdefault(self.names,[]).append(text)

    def show(self):
        #type = sys.getfilesystemencoding()
        type="utf-8"
        for key in self.dic:
            print ( (''.join(key)).replace(' ','')).decode('utf-8').encode(type),\
            ( (''.join(self.dic[key])).replace(' ','')).decode('utf-8').encode(type)
        #htmlfile=urllib2.urlopen(url).read()



renrenspider=spider('zhouxz007@gmail.com','whu@1234')
renrenspider.login()
renrenspider.feed(renrenspider.file)
renrenspider.show()

url2="http://status.renren.com/GetHotDoing.do?word=你最想看的价格战"
htmlfile2=urllib2.urlopen(url2).read()
print htmlfile2