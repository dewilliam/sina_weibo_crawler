#-*- coding: utf-8 -*-
#encoding=utf-8

import MySQLdb
import pygal
import os

time=[]
t_0=t_1=t_2=t_3=t_4=t_5=t_6=t_7=t_8=t_9=t_10=t_11=t_12=0
t_13=t_14=t_15=t_16=t_17=t_18=t_19=t_20=t_21=t_22=t_23=0
result=[0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0]

try:
    conn=MySQLdb.connect(host='localhost',user='root',passwd='musicpower',db='weibo',charset='utf8')
except:
    print 'wrong connection...'
    quit()
cur=conn.cursor(MySQLdb.cursors.DictCursor)
cur.execute('select weibo_time from weibo_list where weibo_time like "%:%"')
rows=cur.fetchall()
for row in rows:
    time.append(row['weibo_time'][:-2])

print len(rows)

for t in time:
    t_h=t.split(':')[0]
    t_m=t.split(':')[1]
    if int(t_h)==23 and int(t_m)<=30:
        result[23]+=1
    if int(t_h)==23 and int(t_m)>30:
        result[0]+=1
    if int(t_h)!=23 and int(t_m)<=30:
        index=int(t_h)
        result[index]+=1
    if int(t_h)!=23 and int(t_m)>30:
        index=int(t_h)+1
        result[index]+=1

for i in range(0,24):
    result[i]=1.0*result[i]/len(rows)
print result

chart=pygal.Line()
chart.x_labels=['0','1','2','3','4','5','6','7','8','9','10','11','12','13',
               '14','15','16','17','18','19','20','21','22','23']
chart.add('times',result)
chart.render()
f=open('d:/Python27/test.html','w')
f.write(chart.render())
f.close()
