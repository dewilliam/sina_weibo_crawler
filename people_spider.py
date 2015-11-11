#-*- coding: utf-8 -*-
#encoding=utf-8

import urllib
import urllib2
import requests
from bs4 import BeautifulSoup
from collections import deque
import re
import os
import random
import time
import MySQLdb

url_list=deque()
visited=set()
proxy_ip=[]
url='http://weibo.cn/2464043951'
cookie='_T_WM=cc5f39ceb170315e5f2d858046a3c28b; gsid_CTandWM=4uae3cf01KdIPmjGzUr0aal0Dfl; SUB=_2A254v331DeTxGeRK7VYR9C3Fzj2IHXVYQAO9rDV6PUJbvNANLXjNkW0hSksbJ42gQgzHP1SeILTkhfTpyA..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5c3wY9vCnrbYKbHWVGCzE.5JpX5K-t; SUHB=0OMl2W7hOMtU42; SSOLoginState=1438322085'
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
def getpage(url):
    header=random.choice(headers)
    form_url=url.split('cn',1)[1]
    page_list=[]
    req=urllib2.Request(url,headers=header)
    try:
        html=urllib2.urlopen(req).read()
    except urllib2.URLError,e:
        print e.code
    soup=BeautifulSoup(html,'html.parser')
    try:
        form=soup.find('form',attrs={'action':form_url})
        total_page=form.find('input',attrs={'type':'hidden'})
    except:
        page_list.append(url)
        return page_list
    total_page_num=int(total_page.get('value'))
    page_list.append(url)
    if total_page_num>1:
        for i in range(2,(total_page_num+1)):
            page_list.append(url+'?page='+str(i))
    return page_list
    
def geturl(url,header):
    req=urllib2.Request(url,headers=header)
    html=urllib2.urlopen(req).read()
    soup=BeautifulSoup(html,'html.parser')
    tr_list=soup.findAll('tr')
    for tr in tr_list:
        td=tr.findAll('td')[1]    
        a=td.findAll('a')[0]
        href=a.get('href')
        sub_sleep=random.randint(3,6)
        time.sleep(sub_sleep)
        getfans(href,header)

def getinfo(url):
    header=random.choice(headers)
    req=urllib2.Request(url,headers=header)
    response=urllib2.urlopen(req)
    html=response.read()
    sub_sleep=random.randint(0,3)
    time.sleep(sub_sleep)
    soup=BeautifulSoup(html,'html.parser')
    try:
        info_url='http://weibo.cn'+soup.find('table').findAll('td')[1].find('a',attrs={'href':re.compile(r'/[0-9]+/info(.*)')}).get('href').split('?',1)[0]
    except:
        wrong=open('d:/Python27/wrong_urls.txt','a')
        wrong.writelines(url)
        wrong.write('\n')
        wrong.close()
        return
    print info_url
    info_req=urllib2.Request(info_url,headers=header)
    try:
        info_html=urllib2.urlopen(info_req).read()
    except:
        wrong=open('d:/Python27/wrong_urls.txt','a')
        wrong.writelines(url)
        wrong.write('\n')
        wrong.close()
        return
    info_soup=BeautifulSoup(info_html,'html.parser')
    try:
        info_class=info_soup.findAll('div',attrs={'class':'c'})[2]
    except:
        wrong=open('d:/Python27/wrong_urls.txt','a')
        wrong.writelines(url)
        wrong.write('\n')
        wrong.close()
        return
    info=str(info_class).split('<br/>')
    print 'done_1'
    user_sex=user_nike_name=user_birth_date=user_place=user_intro=user_mark=''
    for str_ in info:
        new_info=BeautifulSoup(str_,'html.parser').get_text()
        if u'性别' in new_info:
            user_sex=new_info.split(':')[1]
        if u'昵称' in new_info:
            user_nike_name=new_info.split(':')[1]
        if u'生日' in new_info:
            user_birth_date=new_info.split(':')[1]
        if u'地区' in new_info:
            user_place=new_info.split(':')[1]
        if u'简介' in new_info:
            user_intro=new_info.split(':')[1]
        if u'标签' in new_info:
            user_mark=new_info.split(':')[1]
    print 'done_2'
    try:
        conn=MySQLdb.connect(user='root',passwd='musicpower',host='localhost',db='weibo',charset='utf8')
    except:
        print 'connection wrong'
        wrong=open('d:/Python27/wrong_urls.txt','a')
        wrong.writelines(url)
        wrong.write('\n')
        wrong.close()
        return
    cursor=conn.cursor()
    cursor.execute('insert into user_info(url,nike_name,sex,birth_date,place,intro,mark) values(%s,%s,%s,%s,%s,%s,%s)',(url,user_nike_name,user_sex,user_birth_date,user_place,user_intro,user_mark))
    conn.commit()
    print 'done_3'
    cursor.close()
    conn.close()

def first_step(init_url):
    header=random.choice(headers)
    getfans(init_url,header)
    while len(url_list):
        url=url_list.popleft()
        header=random.choice(headers)
        try:
            page_list=getpage(url,header)
        except:
            continue
        for page in page_list:
            geturl(page,header)
            main_sleep=random.randint(3,9)
            time.sleep(main_sleep)
                

def getfans(url,header):
    req=urllib2.Request(url,headers=header)
    html=urllib2.urlopen(req).read()
    soup=BeautifulSoup(html,'html.parser')
    fans_url='http://weibo.cn'+soup.find('a',attrs={'href':re.compile(r'/[0-9]+/fans')}).get('href').split('?',1)[0]
    if url not in visited or len(visited)==0:
        url_list.append(fans_url)
        visited.add(url)
        weibo_urls=open('d:/Python27/weibo_urls.txt','a')
        weibo_urls.writelines(url)
        weibo_urls.write('\n')
        weibo_urls.close()
    sub_sleep=random.randint(3,6)
    time.sleep(sub_sleep)
    print len(visited)

def init():
    weibo_urls=open('d:/Python27/weibo_urls.txt','r')
    urls=weibo_urls.readlines()
    for i in range(1,len(urls)):
        url=urls[i].strip()
        visited.add(url)
    weibo_urls.close()
    

if __name__ == '__main__':
    #init()
    #first_step('http://weibo.cn/u/1859612392')
    f=open('d:/Python27/wrong_urls.txt','r')
    #f.readline()
    urls=f.readlines()
    for url in urls:
        print url.strip()
        sub_sleep=random.randint(3,9)
        time.sleep(sub_sleep)
        getinfo(url.strip())
        sub_sleep_2=random.randint(0,3)
        time.sleep(sub_sleep_2)
    
