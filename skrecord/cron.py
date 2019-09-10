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


sql1='''select * from skrecord_memo;'''

config = {
	'host':'127.0.0.1',
	'user':'ser_skstack',
	'passwd':'9FNdRf1',
	'port':3306,
	'db':'skstack',
	'charset':'utf8'
}



try:
  db = MySQLdb.connect(**config)
  cursor = db.cursor()
  Date = datetime.date.today().strftime("%Y-%m-%d")
  endDate = datetime.date.today()
  try:
    cursor.execute(sql1)
  except:
    pass
  results = cursor.fetchall()
  for row in results:
     noticetime = row[3]
     startDate = noticetime
     datediff = (endDate - startDate).days

     if datediff >= 0:
       receiver_list = [row[5]]
       title = (row[1])

       content = (row[2])
       for receiver in receiver_list:
           args = [receiver,title,content,25]
           sendMail(args)
  cursor.close()
  db.close()

except :
  print "Error!!!!"
