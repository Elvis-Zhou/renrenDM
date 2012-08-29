# -*- coding:utf-8 -*-
#encoding = utf-8
import urllib, urllib2, cookielib, re, sys
import chardet,string,time,random,os
from bs4 import BeautifulSoup
import threading
from Queue import Queue
reload(sys)
sys.setdefaultencoding('utf-8')

maxthreads=100
count=0
urllib2.socket.setdefaulttimeout(30)
#input=open("hotstatus.txt","r")
savepath="./hotpage/"
outputfilename1=savepath+"finance%s.txt" % time.strftime("%y-%m-%d ",time.localtime(time.time()))
outputfilename2=savepath+"rawfinance%s.txt" % time.strftime("%y-%m-%d",time.localtime(time.time()))
#out=open("hotstatus.txt","a")

out=open(outputfilename1,"a")
out2=open(outputfilename2,"a")
out3=open("comonpages.txt","a")
out4=open("pagelist.txt","r")


class renren():
    def __init__(self):
        self.soup=""
        self.names=""
        self.dic={}
        self.compages=[]
        self.pageurls=[]
        self.status=[]
        self.replys=[]
        self.question=""
        self.cururl=""
        self.url="http://www.renren.com/"
        #self.commonpageurl1='http://page.renren.com/assemble/portal/2'
        self.commonpageurl1='http://page.renren.com/friend/allpages'
        self.htmlfile=""
        self.requset=""
        self.queue=Queue()
        self.out_queue=Queue(maxthreads)
        #self.q="金融"

        self.content=set()
        #把content从list改成set以去重
        #self.keyword="保钓人士登岛成功"
        self.charset="utf-8"
        #self.cookie="anonymid=h2k3dem91ah9s0; _r01_=1; mop_uniq_ckid=127.0.0.1_1339338517_232586224; l4pager=0; XNESSESSIONID=4b366edd7d09; _urm_282566272=45; _urm_348398946=45; __utma=151146938.1806053947.1345432990.1345448438.1345558336.3; __utmc=151146938; __utmz=151146938.1345558336.3.3.utmcsr=guide.renren.com|utmccn=(referral)|utmcmd=referral|utmcct=/guide; jebecookies=db4be8c5-9059-4ba4-ad7e-6effba65d472|||||; ick_login=9c57e046-4539-42e6-93c6-834903ba822b; _de=F0FE108A947A3E6B27329D0BA75CD0BC34DF20B0B3AA6FF7; hp=601231122%2Chttp%3A%2F%2Fhdn.xnimg.cn%2Fphotos%2Fhdn221%2F20120609%2F0845%2Fh_tiny_kQSi_1b6b000005011375.jpg%2C%E6%AF%8F%E5%A4%A9%E9%98%85%E8%AF%BB%E4%B8%80%E5%B0%8F%E6%97%B6%3B601369283%2Chttp%3A%2F%2Fhdn.xnimg.cn%2Fphotos%2Fhdn221%2F20120427%2F2145%2Fh_tiny_lCs8_5f4c00069aa22f75.jpg%2C%E7%8E%8B%E6%9D%BE%E4%B9%89%3B600493224%2Chttp%3A%2F%2Fhdn.xnimg.cn%2Fphotos%2Fhdn321%2F20120705%2F1115%2Fh_tiny_Mcbq_673d0000083f1376.jpg%2C%E8%8C%83%E5%86%B0%E5%86%B0; transfer=2ad28691ca7d9b9770209fb86f6c48082; p=459069938a37652ee7fea3a291d7a6a02; ap=282566272; t=90ba99376ca249dbd286e5e46ded842a2; societyguester=90ba99376ca249dbd286e5e46ded842a2; id=282566272; xnsid=97f34a28; loginfrom=null; idc=tel; vip=1"
        try:
            cookie=cookielib.CookieJar()
            cookieProc=urllib2.HTTPCookieProcessor(cookie)
        except:
            raise
            #else:
        self.opener=urllib2.build_opener(cookieProc)
        urllib2.install_opener(self.opener)
    def generatepurl(self):


        self.htmlfile=urllib2.urlopen("http://page.renren.com/eason/fdoing").read()
        soup=BeautifulSoup(self.htmlfile,"lxml")
        rawurl="http://page.renren.com"
        self.status=soup.find_all("h3")

        for p in self.status:
            print p.text.strip()

        self.quesitonurls=soup.find_all("a",{"href":re.compile(r'^/\d*/.*',re.DOTALL)})

        for p in self.quesitonurls:
            self.pageurls.append(rawurl+p["href"])

        rawhtml=urllib2.urlopen(h).read()
        soup=BeautifulSoup(rawhtml,"lxml")
        allcomments=soup.find_all("p",{"class":"content"})

        for p in allcomments:
            print p.text.strip()

    def showurls(self,htmlfile=""):
        #testurl="http://www.zhihu.com/search/question?q=%E9%87%91%E8%9E%8D&type1=question&page=37"
        #self.htmlfile=self.getpage(testurl)
        if htmlfile:
            self.htmlfile=htmlfile
        #self.htmlfile=self.getpage("http://page.renren.com/friend/allpages")
        self.soup=BeautifulSoup(self.htmlfile,"lxml")
        url="http://page.renren.com"
        #print self.htmlfile
        #questions=self.soup.find
        pages=self.soup.find_all("a",{"target":"top","class":"owner"})
        #print pages
        for p in pages:
            t=p.text
            self.compages.append(t)
            tt=url+re.findall(r"/\d*",p["href"])[0]
            self.pageurls.append(tt)
            #写入文件
            out3.write(t+"\n"+tt+"\n")
            out4.write(tt+"\n")
            print t
            print tt
        #print self.quesitons
        return self.pageurls

    def getpage(self,url):
        #self.keyword=keyword
        if url:
            self.url=url
        self.requset=urllib2.Request(self.url)
        #self.requset.add_header("Cookie",self.cookie)
        #self.requset.add_header("Host","www.renren.com")
        #self.requset.add_header("Referer",self.cururl)
        self.requset.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.75 Safari/537.1")
        i=0
        t=0
        while t==0:
            try:
                self.htmlfile=urllib2.urlopen(self.requset).read()
                if  self.htmlfile:
                    t=1
                    break
                else:
                    i+=1
                    #continue
            except :
                i+=1
            if i>=5:break

        #print self.htmlfile
        return self.htmlfile

    def dealcontent(self,htmlfile="",answercount=3):
        if htmlfile:
            self.htmlfile=htmlfile
        self.htmlfile=urllib2.urlopen("http://page.renren.com/eason/fdoing").read()
        soup=BeautifulSoup(self.htmlfile,"lxml")
        rawurl="http://page.renren.com"
        self.status=soup.find_all("h3")

        for p in self.status:
           print p.text.strip()

        self.quesitonurls=soup.find_all("a",{"href":re.compile(r'^/\d*/.*',re.DOTALL)})

        for p in self.quesitonurls:
            self.pageurls.append(rawurl+p["href"])

        rawhtml=urllib2.urlopen(h).read()
        soup=BeautifulSoup(rawhtml,"lxml")
        allcomments=soup.find_all("p",{"class":"content"})

        for p in allcomments:
            print p.text.strip()
        """
        #print soup
        self.question=soup.title.text[:-4]
        #print self.question
        answers=soup.find_all("div",{"class":"xajw xod"})
        keywords=soup.find_all("a",{"class":"xyk"})
        self.keyword=""
        for k in keywords:
            self.keyword+=k.text.strip()+" "
        print "关键词是: "+self.keyword
        #print answers
        if answers:
            self.answer=answers[0].text
        else:
            self.answer=u"这个问题没有一个好的答案"
        if answers:
            i=0
            for ans in answers:
                self.answers.append(ans.text)
                i+=1
                if i>=answercount:break

        #print self.answer
        self.writetoaiml()
        self.writetorawfile()
        self.answers=[]
        time.sleep(random.randint(1,3))
        self.questionurls=[]
        self.answers=[]

        html=open("test.html")
        htmlfile=""
        for i in html:
            htmlfile+=i
        soup=BeautifulSoup(htmlfile,"lxml")
        question=soup.title.text[:-4]

        answers=soup.find("div",{"class":"xajw xod"})
        print question
        print answers.text
        """
        return 1

    def dealquestions(self,startpage=31,maxpage=38,keyword="金融",answercount=3):
        for page in range(startpage,maxpage+1):
            print "now at page:"+str(page)
            self.quesitonurls=[]
            self.quesitons=[]
            url=self.generatepurl(keyword,page)
            htmlfile=self.getpage(url)
            soup=BeautifulSoup(htmlfile,"lxml")
            while soup.find_all(text="请输入图中的数字："):
                print "\a"*10,
                print url+" 知乎要求输入验证码，请打开知乎输入"
                #os.system("cmd ./beep.bat")
                time.sleep(20)
                #这个是获取问题列表URL的时候
                htmlfile=self.getpage(url)
                soup=BeautifulSoup(htmlfile,"lxml")

            self.showurls(htmlfile)
            self.dealcontent(answercount=answercount)

            for q in self.quesitons:
                out3.write(q+"\n")
            out3.flush()
            self.quesitons=[]
            print "sleep half a minute~~~"
            time.sleep(random.randint(25,35))
            #if len(htmlfile)<=12200:
            #print "finish at page: "+str(page)
            #break




    def writetoaiml (self):
        global out,count
        out.write("  <category>\n")
        out.write("    <pattern>")
        words=self.question.encode("utf-8")
        if not words.strip():
            return
        words=words.replace("&","&amp;")
        words=words.replace("<","&lt;")
        words=words.replace(">","&gt;")
        words=words.replace("'","&apos;")
        words=words.replace('"',"&quot;")
        out.write(words)
        out.write("</pattern>\n")
        out.write("    <template>\n")
        print self.question
        if len(self.answers)>1:
            out.write("      <random>\n")
            for x in self.answers:
                print x
                out.write("        <li>")
                words=x.encode("utf-8").replace("&","&amp;")
                words=words.replace("<","&lt;")
                words=words.replace(">","&gt;")
                words=words.replace("'","&apos;")
                words=words.replace('"',"&quot;")
                out.write(words)
                out.write("</li>\n")
                #count += 1
                out.write("      </random>\n")
        else:
            x=self.answer.encode("utf-8")
            print x
            words=x.replace("&","&amp;")
            words=words.replace("<","&lt;")
            words=words.replace(">","&gt;")
            words=words.replace("'","&apos;")
            words=words.replace('"',"&quot;")
            #charset=chardet.detect(words)["encoding"]
            out.write(words+'\n')
        out.write("    </template>\n")
        out.write("  </category>\n")
        out.flush()
        count += 1
        print count
        #self.content=set()


    def writetorawfile(self):
        if not self.question.strip():
            return
        out2.write("问题:\n"+self.question.encode("utf-8")+"\n")
        out2.write("关键词:\n"+self.keyword.encode("utf-8")+"\n")
        out2.write("答案:\n")
        i=1
        for x in self.answers:
            out2.write("最佳答案Top"+str(i)+":\n"+x.encode("utf-8")+'\n')
            i+=1

        out2.write("引用链接:\n"+self.cururl.encode("utf-8")+"\n")
        out2.write("######################################\n")
        out2.flush()

    def findhtmlurls(self,filename="mosthot.html"):

        file=open(filename,"r")
        htmlfile=""
        for line in file:
            htmlfile+=line
        soup=BeautifulSoup(htmlfile,'lxml')
        x=soup.find_all("strong")
        #print x
        for aa in x:
            print >>out3,aa.text

            t=aa.find("a")["href"]
            try:
                t=re.findall(r"http://page.renren.com/\d*",t)[0]
                print >>out3,t
            except:
                pass
    """
    def findurls(self,nowurl):
        #nowurl=url%x
        self.out_queue.get()
        self.getpage(nowurl)
        print "now finding at :"+nowurl
        self.showurls()
        out3.flush()
        out4.flush()
        self.out_queue.task_done()
    def findCommonPageUrls(self,start=0,end=1000):
        url="http://page.renren.com/friend/allpages?curpage=%s&t=0"

        for x in range(start,end+1):
            nowurl=url%x
            #t=threading.Thread(target=self.findurls(nowurl))
            self.queue.put(nowurl)
        print "finish put urls"
        for x in range(start,end+1):
            url=self.queue.get()
            print url
            t=threading.Thread(target=self.findurls(url))
            #self.out_queue.put(t,1)
            #t.start()
            #self.out_queue.join()

        #self.out_queue.join()
        """
    def findCommonPageUrls(self,start=0,end=1000):
        url="http://page.renren.com/friend/allpages?curpage=%s&t=0"
        for x in range(start,end+1):
            nowurl=url%x
            self.getpage(nowurl)
            print "now finding at :"+nowurl
            self.showurls()
            out3.flush()
            out4.flush()

class downpage(threading.Thread):
    def __init__(self,queue,out_queue):
        threading.Thread.__init__(self)
        self.queue=queue
        self.out_queue=out_queue

    def run(self):
        while True:
            url=self.queue.get()
            i=0
            t=0
            while not t:
                try:
                    htmlfile=urllib2.urlopen(url).read()
                    if  htmlfile:
                        t=1
                        break
                    else:
                        i+=1
                        #continue
                except :
                    i+=1
                if i>=5:break
            self.out_queue.put(htmlfile)
            self.queue.task_done()

class dealpage(threading.Thread):
    def __init__(self,out_queue,renrendm):
        threading.Thread.__init__(self)
        self.out_queue=out_queue
        self.renrendm=renrendm

    def run(self):
        while True:
            htmlfile=self.out_queue.get()
            self.renrendm

            self.out_queue.task_done()

if __name__ == "__main__":
    renrendm=renren()
    startpage=18
    endpage=1000
    #renrendm.findCommonPageUrls(startpage,endpage)
    renrendm.dealcontent()
    #keyword="金融"
    #answercount=3
    #renrendm.dealquestions(startpage,endpage,keyword,answercount)
    #renrendm.showurls("")
