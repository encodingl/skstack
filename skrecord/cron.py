#! /usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import time
import MySQLdb
from sendinfo import *
from warnings import filterwarnings
filterwarnings('error', category = MySQLdb.Warning)
import smtplib
from email.mime.text import MIMEText
from email.header import Header
#def sendmail():
#    send_mail('Subject here hahaha', 'Here is the message.', 'monitor.sz@mljr.com', ['yanjun.wang@mljr.com'], fail_silently=False)
#print("ok")

sql1='''select * from skrecord_memo;'''

config = {
	'host':'10.8.105.195',
	'user':'ser_skipper',
	'passwd':'9FNdRf1/GyPwFrRd8Oempw==',
	'port':3306,
	'db':'skipper',
	'charset':'utf8'
}

#receiver_list = ['yanjun.wang@mljr.com']

try:
  db = MySQLdb.connect(**config)
  cursor = db.cursor()
  Date = datetime.date.today().strftime("%Y-%m-%d")
  endDate = datetime.date.today()
  #startDate = endDate - datetime.timedelta(days=21)
  #datediff = (endDate - startDate).days
  try:
    cursor.execute(sql1)
  except:
    pass
  results = cursor.fetchall()
  for row in results:
     noticetime = row[3]
     startDate = noticetime
     datediff = (endDate - startDate).days
     #print "test : %s " % row[2]
     #print(row[2])
     #print(noticetime)
     #print(row[3])
     #print(endDate)
     #print(startDate)
     #print(datediff)
     if datediff >= 0:
       receiver_list = [row[5]]
       title = (row[1])
       #content = u'''test'''  % (row[1],row[2])
       #content = 'test'
       content = (row[2])
       for receiver in receiver_list:
           args = [receiver,title,content,25]
           sendMail(args)
           #send_mail('Subject here hahaha', 'Here is the message.', 'monitor.sz@mljr.com', ['yanjun.wang@mljr.com'], fail_silently=False)
  #print "ok"
  cursor.close()
  db.close()
  #print(row[2])
except :
  print "Error!!!!"
