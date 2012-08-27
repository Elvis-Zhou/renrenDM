# -*- coding:utf-8 -*-
#encoding = utf-8
import urllib, urllib2, cookielib, re, sys,os
from sgmllib import SGMLParser
import chardet,string,time
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf-8')

#url="http://status.renren.com/status/hot/list?word=%E4%BF%9D%E9%92%93%E4%BA%BA%E5%A3%AB%E7%99%BB%E5%B2%9B%E6%88%90%E5%8A%9F"
#htmlfile=urllib2.urlopen(url).read()
#print htmlfile
count=0
urllib2.socket.setdefaulttimeout(30)
#input=open("hotstatus.txt","r")
savepath="./commonpage/"
outputfilename1=savepath+"status%s.txt" % time.strftime("%y-%m-%d-%H",time.localtime(time.time()))
outputfilename2=savepath+"rawstatus%s.txt" % time.strftime("%y-%m-%d-%H",time.localtime(time.time()))
#out=open("hotstatus.txt","a")

#out=open(outputfilename1,"a")
#out2=open("wordlist.txt","a")
#out3=open(outputfilename2,"a")
class renren():
    def __init__(self,email,password):
        self.soup=""
        self.names=""
        self.dic={}
        self.stauts=[]
        #self.url="http://status.renren.com/GetHotDoing.do?word=%E4%BF%9D%E9%92%93%E4%BA%BA%E5%A3%AB%E7%99%BB%E5%B2%9B%E6%88%90%E5%8A%9F"
        self.url='http://www.renren.com/PLogin.do'
        #self.url2="http://www.renren.com/282566272"
        self.url2="http://guide.renren.com/guide?reurl=%2F%2Fstatus%2Fstatus%3Fid%3D282566272#//status/status?id=282566272"
        self.url2="http://status.renren.com/GetSomeomeDoingList.do?userId=253810474&curpage=0"
        self.originurl="http://status.renren.com/GetSomeomeDoingList.do?userId=%s&curpage=%s"
        self.htmlfile=""
        self.requset=""
        self.pages=[]
        self.email=email
        self.password=password
        self.domain='renren.com'
        self.content=set()
        #把content从list改成set以去重
        #self.keyword="保钓人士登岛成功"
        self.charset="ascii"
        self.cookie="anonymid=h2k3dem91ah9s0; _r01_=1; mop_uniq_ckid=127.0.0.1_1339338517_232586224; l4pager=0; XNESSESSIONID=4b366edd7d09; _urm_282566272=45; _urm_348398946=45; depovince=JS; __utma=151146938.1806053947.1345432990.1345448438.1345558336.3; __utmc=151146938; __utmz=151146938.1345558336.3.3.utmcsr=guide.renren.com|utmccn=(referral)|utmcmd=referral|utmcct=/guide; transfer=2ad28691ca7d9b9770209fb86f6c48082; at=1; vip=1; jebecookies=db4be8c5-9059-4ba4-ad7e-6effba65d472|||||; ick_login=9c57e046-4539-42e6-93c6-834903ba822b; idc=tel; _de=F0FE108A947A3E6B27329D0BA75CD0BC34DF20B0B3AA6FF7; p=a9de570e422f9a65d4e1cb2911cf185c6; ap=348398946; t=8ea852e4d2f94b9a3118812288a42b5a6; societyguester=8ea852e4d2f94b9a3118812288a42b5a6; id=348398946; xnsid=ac9dc4c4; feedType=348398946_hot; loginfrom=null"
        try:
            cookie=cookielib.CookieJar()
            cookieProc=urllib2.HTTPCookieProcessor(cookie)
        except:
            raise
            #else:
        self.opener=urllib2.build_opener(cookieProc)
        urllib2.install_opener(self.opener)

    def login(self):
        #url='http://www.renren.com/PLogin.do'
        postdata={
            'email':self.email,
            'password':self.password,
            'domain':self.domain
        }
        req=urllib2.Request(
            self.url,
            urllib.urlencode(postdata)
        )
        req=urllib2.Request(self.url2)
        req.add_header("cookie",self.cookie)
        self.file=urllib2.urlopen(req).read()
        print self.file

    def show(self):
        #type = sys.getfilesystemencoding()
        type="utf-8"
        for key in self.dic:
            print ( (''.join(key)).replace(' ','')).decode('utf-8').encode(type),\
            ( (''.join(self.dic[key])).replace(' ','')).decode('utf-8').encode(type)
            #htmlfile=urllib2.urlopen(url).read()

    def getpage(self,id):
        self.url=self.originurl % (id,0)
        #self.url=self.url.replace("+","%20")
        print self.url
        self.requset=urllib2.Request(self.url)
        #self.requset.add_header("Accept-Charset","GBK,utf-8;q=0.7,*;q=0.3")
        #self.requset.add_header("Accept-Encoding","gzip,deflate,sdch")
        #self.requset.add_header("Accept-Language","zh-CN,zh;q=0.8")
        self.requset.add_header("Host","status.renren.com")
        self.requset.add_header("Cookie",self.cookie)
        #self.requset.add_header("Referer","http://status.renren.com/ajaxproxy.htm")
        self.requset.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.75 Safari/537.1")
        i=0
        t=0
        while t==0:
            try:
                self.htmlfile=urllib2.urlopen(self.requset).read()
                htmlfile2=urllib2.urlopen(self.requset).read()
                if  self.htmlfile[:200]==htmlfile2[:200]:
                    t=1
                else:
                    i+=1
                    #continue
            except :
                i+=1
            if i>=5:break
        self.charset=chardet.detect(self.htmlfile)["encoding"]
        print self.charset

        i=0
        while self.charset!='ascii':
            try:
                self.htmlfile=urllib2.urlopen(self.requset).read()
            except :
                pass
            self.charset=chardet.detect(self.htmlfile)["encoding"]
            i+=1
            if i>=5:break
        print self.htmlfile
        return self.htmlfile

    def dealcontent(self,id):
        """
        主要函数，用来输入热门词汇，就可以返回单个结果
        """
        t=0
        i=0
        content={}
        self.htmlfile=self.getpage(id)
        #print content

        for c in content:
            print c["content"]
        while t==0:
            try:
                start=self.htmlfile.find('"doingArray":')
                end=self.htmlfile.find('}],')
                content=self.htmlfile[start+13:end+2]
            except BaseException:
                return 0
            if content[-1]=="]":
                t=1
                content=eval(content)
                break
            else:
                try:
                    self.htmlfile=urllib2.urlopen(self.requset).read()
                except :
                    pass
                i+=1
            if i>5:
                break
        allct=""
        for text in content:
            ct=text["content"]
            ct=ct.replace(r'<span class="key">',"")
            ct=ct.replace(r'<\/span>',"")
            ct=ct.replace(r'http:\/\/',"http://")
            ct=ct.replace(r'.cn\/',".cn/")
            ct=ct.replace(r'.com\/',".com/")
            ct=ct.replace("#","")
            ct=re.sub(r'<a\b href=".*?>',"",ct,flags=re.M)
            ct=ct.replace(r"<\/a>","")
            if self.charset=="utf-8":
                pass
            else:
                ct=ct.decode("raw_unicode_escape")
                #imgs=re.findall(r"(?<=<img.*?alt=').*?(?=')",ct,re.DOTALL)
            #emotion=re.findall(r"(?<=<img.*?alt=').*?(?=')",ct,re.DOTALL)
            ct=re.sub(r"<img.*?alt='","[",ct,flags=re.DOTALL)
            ct=re.sub(r"'\s.*?\/>","]",ct,flags=re.DOTALL)
            if self.charset=="utf-8":
                pass
            else:
                ct=ct.encode("utf-8")
                #ct=ct.decode("gb18030").encode("utf-8")
            print ct
            allct+=ct+"\n"

            self.content.add(ct)
        charset=chardet.detect(allct)["encoding"]
        #print charset
        #out3.write(allct.decode(charset).encode("utf-8")+"\n")
        #out3.write("######################################################"+"\n")
        #print len(content)
        #self.htmlfile=""
        return 1
    def dealwordlist(self):
        wordlist=eval(self.htmlfile)["wordList"]
        out2.write("\n"+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+"\n")
        out2.write("######################################################"+"\n")
        for word in wordlist:
            t=word.decode('raw_unicode_escape')
            print t
            self.wordlist.append(t)
            out2.write(t.encode("utf-8")+"\n")
        out2.flush()

    def dealallwords(self,todaykeyword):
        self.getpage(todaykeyword)
        self.dealwordlist()
        print "######################################################"
        for words in self.wordlist:
            #self.getpage(words)
            t=words.encode("utf-8")
            #t=t.replace(" ","+")
            if self.dealcontent(t):
                #print words
                #self.writetoaiml()
                print "######################################################"

    def writetoaiml (self):
        global out,count
        out.write("  <category>\n")
        out.write("    <pattern>")
        words=self.keyword
        words=words.replace("&","&amp;")
        words=words.replace("<","&lt;")
        words=words.replace(">","&gt;")
        words=words.replace("'","&apos;")
        words=words.replace('"',"&quot;")
        out.write(words)
        out.write("</pattern>\n")
        out.write("    <template>\n")
        if len(self.content)>1:
            out.write("      <random>\n")
            for x in self.content:
                print self.keyword
                print x
                out.write("        <li>")
                words=x.replace("&","&amp;")
                words=words.replace("<","&lt;")
                words=words.replace(">","&gt;")
                words=words.replace("'","&apos;")
                words=words.replace('"',"&quot;")
                charset=chardet.detect(words)["encoding"]
                try:
                    out.write(words.decode(charset).encode("utf-8"))
                except UnicodeDecodeError:
                    out.write(words.decode("gb18030").encode("utf-8"))
                except BaseException:
                    out.write(words.encode("utf-8"))
                out.write("</li>\n")
                #count += 1
            out.write("      </random>\n")
        else:
            print self.keyword
            x=self.content.pop()
            print x
            words=x.replace("&","&amp;")
            words=words.replace("<","&lt;")
            words=words.replace(">","&gt;")
            words=words.replace("'","&apos;")
            words=words.replace('"',"&quot;")
            charset=chardet.detect(words)["encoding"]
            out.write(words.decode(charset).encode("utf-8")+'\n')
            count += 1
        out.write("    </template>\n")
        out.write("  </category>\n")
        out.flush()
        count += 1
        print count
        self.content=set()
    def findlack(self):
        global out
        input=open("hotstatus.txt","r")
        out=open("hotstatus.txt","a")
        self.getpage()
        self.dealwordlist()
        text=""
        while 1:
            thisline=input.readline()
            text+=thisline
            if not thisline:
                break
        texts=re.findall(r'(?<=<pattern>).*?(?=</pattern>)',text,re.M)
        #print texts
        text2=[]
        #print self.wordlist
        for theword in texts:
            t=theword.decode("utf-8")
            #print t
            text2.append(t)
        texts= set(self.wordlist)-set(text2)
        print texts
        for word in texts:
            #t=word.replace(" ","+")
            if self.dealcontent(word):
                #print words
                self.writetoaiml()
            print "######################################################"

if __name__ == "__main__":
    semail='zhouxz007@gmail.com'
    spassword='whu@1234'
    renrendm=renren(semail,spassword)
    #renrendm.login()
    #renrendm.show()
    #todaykeyword="过你妹的七夕"
    #url="http://status.renren.com/GetHotDoing.do?word="+todaykeyword
    #url2="http://status.renren.com/GetSomeomeDoingList.do?userId=253810474&curpage=0"
    id="253810474"
    #renrendm.dealallwords(todaykeyword)
    #renrendm.getpage(todaykeyword)
    #renrendm.dealwordlist()
    renrendm.dealcontent(id)

    #renrendm.getpage("printfabcd")
    #renrendm.dealcontent("GALA")
    #renrendm.findlack()