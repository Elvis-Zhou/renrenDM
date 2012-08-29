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
outputfilename1=savepath+"renren%s.txt" % time.strftime("%y-%m-%d ",time.localtime(time.time()))
outputfilename2=savepath+"renrenstatus%s.txt" % time.strftime("%y-%m-%d",time.localtime(time.time()))
#out=open("hotstatus.txt","a")

out=open(outputfilename1,"a")
out2=open(outputfilename2,"a")
out3=open("comonpages.txt","a")
in1=open("pagelist.txt","r")

lock1=threading.Lock()
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
        self.out_queue=Queue()
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
    def generatepUrl(self,max=1000):
        i=0
        for line in in1:
            self.queue.put(line)
            i+=1
            if i>max:
                break

    def showUrlpage(self):
        url=self.queue.get().strip()+"/fdoing"
        print url
        htmlfile=self.getpage(url)
        return htmlfile

    def tempgeturls(self,htmlfile=""):
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
            #out4.write(tt+"\n")
            print t
            print tt
        #print self.quesitons
        return self.pageurls

    def getpage(self,url):
        if url:
            self.url=url
        self.requset=urllib2.Request(self.url)
        self.requset.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.75 Safari/537.1")
        i=0
        t=0
        while not t:
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

    def dealcontent(self):
        #if htmlfile:
            #self.htmlfile=htmlfile
        while 1:
            htmlfile=self.showUrlpage()
            #self.htmlfile=urllib2.urlopen("http://page.renren.com/eason/fdoing").read()
            soup=BeautifulSoup(htmlfile,"lxml")
            rawurl="http://page.renren.com"
            #self.status=soup.find_all("h3")
            #for p in self.status:
               #print p.text.strip()
            quesitonurls=soup.find_all("a",{"href":re.compile(r'^/\d*/.*',re.DOTALL)})
            for p in quesitonurls:
                self.out_queue.put(rawurl+p["href"])
            self.queue.task_done()
        #return 1

    def dealcomments(self):
        while 1:
            url=self.out_queue.get()
            print url
            htmlfile=self.getpage(url)
            soup=BeautifulSoup(htmlfile,"lxml")
            allcomments=soup.find_all("p",{"class":"content"})
            try:
                status=soup.find("h3").text.strip()
            except AttributeError:
                status=soup.find("span",{"class":"status-content"}).text.strip()
            except BaseException:
                status="状态丢失"
            commentlist=[]
            for comment in allcomments:
                x=comment.text.strip()
                commentlist.append(x)
                #print x
            lock1.acquire()
            self.writetoxml(status,commentlist)
            lock1.release()
            self.out_queue.task_done()

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

    def writetoxml (self,status,list):
        if not list:
            return
        global out,count
        out.write("  <category>\n")
        out.write("    <text>")
        words=status
        if not words.strip():
            return
        words=words.replace("&","&amp;")
        words=words.replace("<","&lt;")
        words=words.replace(">","&gt;")
        words=words.replace("'","&apos;")
        words=words.replace('"',"&quot;")
        out.write(words)
        out.write("</text>\n")
        out.write("    <commments>\n")
        print status
        for comment in list:
            out.write("      <comment1>")
            print comment.strip()
            #out.write("        <li>")
            words=comment.strip().replace("&","&amp;")
            words=words.replace("<","&lt;")
            words=words.replace(">","&gt;")
            words=words.replace("'","&apos;")
            words=words.replace('"',"&quot;")
            out.write(words)
            out.write("</comment1>\n")
            #count += 1
            #out.write("      </random>\n")
        out.write("    </text>\n")
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

    def findCommonPageUrls(self,start=0,end=1000):
        url="http://page.renren.com/friend/allpages?curpage=%s&t=0"
        for x in range(start,end+1):
            nowurl=url%x
            self.getpage(nowurl)
            print "now finding at :"+nowurl
            self.showurls()
            out3.flush()
            #out4.flush()
    def p(self):
        print "1"

    def main(self):
        #初始化要抓取的页面列表
        url=self.generatepUrl(50000)
        print "begin"
        #self.dealcontent()
        #做100个线程，用来处理放在out_queue里面的状态队列，并获得状态和回复，写入文件。
        for j in range(0,50):
            t=threading.Thread(target=self.dealcomments)
            t.setDaemon(True)
            t.start()

        #做10个线程池，用来做打开状态主页，获取状态链接放入out_queue中
        for i in range(0,10):
            t=threading.Thread(target=self.dealcontent())
            t.setDaemon(True)
            t.start()


        self.queue.join()
        self.out_queue.join()

        print "finish all"


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
    renrendm.main()
    #renrendm.dealcontent()
    #keyword="金融"
    #answercount=3
    #renrendm.dealquestions(startpage,endpage,keyword,answercount)
    #renrendm.showurls("")
