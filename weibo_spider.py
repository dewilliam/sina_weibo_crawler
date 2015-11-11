#-*- coding: utf-8 -*-
#encoding=utf-8

import urllib2
import requests
import random
from bs4 import BeautifulSoup
from collections import deque
import MySQLdb
import test_spider
import time

cookie='_T_WM=bfe9a82723014e83f27c2980fef82185; SUB=_2A254u04sDeTxGeRK7VYR9C3Fzj2IHXVYRFJkrDV6PUJbrdANLVTlkW0gaBO4vmKNp9Lz0P4XmSXPySMueg..; gsid_CTandWM=4uae3cf01KdIPmjGzUr0aal0Dfl'
user_agent_1='Mozilla/5.0 (Windows NT 6.3; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'
user_agent_2='Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30'
user_agent_3='Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)'
user_agent_4='Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)'
user_agent_5='Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727) '
user_agent_6='Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)'
user_agent_7='Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50'
user_agent_8='Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)'
user_agent_9='Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)'
user_agent_10='Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1'
user_agent_11='Mozilla/5.0 (Windows; U; Windows NT 5.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12'
user_agent_12='Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; TheWorld)'
accept='text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
Host='weibo.cn'

headers=[{'Cookie':cookie,'User-Agent':user_agent_1,'Accept':accept,'Connection':'keep-alive','Host':Host},{'Cookie':cookie,'User-Agent':user_agent_2,'Accept':accept,'Connection':'keep-alive','Host':Host},{'Cookie':cookie,'User-Agent':user_agent_3,'Accept':accept,'Connection':'keep-alive','Host':Host},{'Cookie':cookie,'User-Agent':user_agent_4,'Accept':accept,'Connection':'keep-alive','Host':Host},{'Cookie':cookie,'User-Agent':user_agent_5,'Accept':accept,'Connection':'keep-alive','Host':Host},{'Cookie':cookie,'User-Agent':user_agent_6,'Accept':accept,'Connection':'keep-alive','Host':Host},{'Cookie':cookie,'User-Agent':user_agent_7,'Accept':accept,'Connection':'keep-alive','Host':Host},{'Cookie':cookie,'User-Agent':user_agent_8,'Accept':accept,'Connection':'keep-alive','Host':Host},{'Cookie':cookie,'User-Agent':user_agent_9,'Accept':accept,'Connection':'keep-alive','Host':Host},{'Cookie':cookie,'User-Agent':user_agent_10,'Accept':accept,'Connection':'keep-alive','Host':Host},{'Cookie':cookie,'User-Agent':user_agent_11,'Accept':accept,'Connection':'keep-alive','Host':Host},{'Cookie':cookie,'User-Agent':user_agent_12,'Accept':accept,'Connection':'keep-alive','Host':Host}]

urls_list=deque()
id_list=deque()

def getweibo(user_id,url):
    print user_id
    print url
    header=random.choice(headers)
    req=urllib2.Request(url,headers=header)
    response=urllib2.urlopen(req)
    html=response.read()
    soup=BeautifulSoup(html,'html.parser')
    weibo_set=soup.findAll('div',attrs={'class':'c'})
    for weibo in weibo_set[:-2]:
        try:
            weibo_info=weibo.find('span',attrs={'class':'ctt'}).get_text()
            weibo_attr=weibo.find('span',attrs={'class':'ct'}).get_text().split(u'来自')
        except:
            f=open('d:/Python27/wrong_urls.txt','a')
            s=url+','+str(user_id)
            f.writelines(s)
            f.write('\n')
            f.close()
            return
        date_time=weibo_attr[0].split(' ')
        if len(date_time)==2:
            weibo_date=weibo_attr[0].split(' ')[0]
            weibo_time=weibo_attr[0].split(' ')[1]
        else:
            weibo_date=''
            weibo_time=date_time[0]
        if len(weibo_attr)==2:
            weibo_from=weibo_attr[1]
        try:
            conn=MySQLdb.connect(host='localhost',user='root',passwd='musicpower',db='weibo',charset='utf8')
        except:
            print 'wrong connectino...'
            return
        cur=conn.cursor()
        cur.execute('insert into weibo_list(user_id,weibo_info,weibo_date,weibo_time,weibo_from) values(%s,%s,%s,%s,%s)',(user_id,weibo_info,weibo_date,weibo_time,weibo_from))
        conn.commit()
        cur.close()
        conn.close()
        
        

def geturls():
    try:
        conn=MySQLdb.connect(host='localhost',user='root',passwd='musicpower',db='weibo',charset='utf8')
    except:
        print 'wrong connection...'
        return
    sql='select id,url from user_info'
    cursor=conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(sql)
    rows=cursor.fetchall()
    for row in rows:
        urls_list.append(row['url'])
        id_list.append(row['id'])
    cursor.close()
    conn.close()
    



if __name__ == '__main__':
    geturls()
    while len(urls_list):
        url=urls_list.popleft()
        user_id=id_list.popleft()
        print url
        pages=test_spider.getpage(url)
        quit()
        if len(pages)>20:
            pages=pages[:20]
        if len(pages)==1:
            main_sleep=random.randint(3,9)
            time.sleep(main_sleep)
            getweibo(user_id,pages[0])
            continue
        for page in pages:
            getweibo(user_id,page)
            sub_sleep=random.randint(2,6)
            time.sleep(sub_sleep)
        main_sleep=random.randint(3,9)
        time.sleep(main_sleep)
