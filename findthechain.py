#!/usr/bin/env python
#encoding=utf-8
import urllib, urllib2, cookielib, re, sys,os

class  Renren(object):
    def __init__(self,email,password):
        self.email=email
        self.password=password
        self.origURL='http://www.renren.com/Home.do'
        self.domain='renren.com'
        # 如果有本地cookie，登录时无需验证。
        self.cj = cookielib.LWPCookieJar()
        try:
            self.cj.revert('renren,cookie')
        except:
            pass
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        urllib2.install_opener(self.opener)

    def login(self):
        params = {'email':self.email,'password':self.password,'origURL':self.origURL,'domain':self.domain}
        req = urllib2.Request(
            'http://www.renren.com/PLogin.do',
            urllib.urlencode(params)
        )
        r = self.opener.open(req)
        #print r.read()
    def friends(self):
        #好友目录地址
        req='http://friend.renren.com/myfriendlistx.do'
        print "Get my friends"
        r=self.opener.open(req)
        data=r.read()
        f=re.findall('"id":(\d{6,15}),',data)
        print "friends list"
        print f,len(f)
        #todo
        self.todolist=f
        self.donelist=[]
        #write data
        fdata=open('data0.txt','w')
        for item in f:
            fdata.write(item+' ')
        fdata.close()
        sernum=0
        while True:
            temp1w={}
            sernum=sernum+1
            print "data"+str(sernum)
            count=1000
            while count>0:
                count=count-1
                rrid=self.getone()        #从todo 里面取一个数据
                print count,rrid
                f=self.getfriends(rrid)
                self.savenews(f)    #保存该组数据到todo
                templst=''
                for eachid in f:
                    templst=eachid+' '+templst
                temp1w[rrid]=templst
            #将count 个结果写到文件
            filename="data_"+str(sernum)+".txt"
            fp=open(filename,'w')
            for each in temp1w:
                fp.write(each+'@'+temp1w[each])
                fp.write('\n')
    def getfriends(self,rrid):
        friends=[]
        count=0
        while True:
            req="http://friend.renren.com/GetFriendList.do?curpage="+str(count)+'&id='+rrid
            print 'Get',req
            r=self.opener.open(req)
            data=r.read()
            f=re.findall('profile.do\?id=(\d{7,15})"><img',data)
            friends=friends+f
            count=count+1
            if f==[]:
                exit()
        return friends

    def getone(self):
        if self.todolist==[]:
            print "Empty todo list"
        popup=self.todolist[1]        #选择第一个id
        self.donelist.append(popup)    #加入到done 列表
        del self.todolist[1]        #在todo 中删除
        return popup                #返回

    def savenews(self,newlist):
       for item in newlist:                    #删除出现在了done 列表中的id
           if item in self.donelist:
               newlist.remove(item)
       self.todolist=self.todolist+newlist        #添加到todo 列表中
       self.todolist=list(set(self.todolist))    #去掉重复元素


if __name__ == "__main__":
     semail='zhouxz007@gmail.com'
     spassword='whu@1234'
     #a=Renren(semail,spassword)
     print "your account and password are %s %s" % (semail, spassword)
     #os.system("cmd.exe")
     #print "\a"*10
     #a.login()
     #a.friends()
