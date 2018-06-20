#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2018年6月19日 @author: skipper
'''

import time
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
 
def job1(f):
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), f
 
def job2(args1, args2, f):
    print f, args1, args2
 
def job3(**args):
    print args
 
'''
APScheduler支持以下三种定时任务：
cron: crontab类型任务
interval: 固定时间间隔任务
date: 基于日期时间的一次性任务
'''

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    #循环任务示例
    scheduler.add_job(job1, 'interval', seconds=3, args=('循环',), id='test_job1')
    #定时任务示例
    scheduler.add_job(job1, 'cron', second='*/4', args=('定时',), id='test_job2')
    #一次性任务示例
    scheduler.add_job(job1, next_run_time=(datetime.datetime.now() + datetime.timedelta(seconds=5)), args=('一次',), id='test_job3')
    '''
    传递参数的方式有元组(tuple)、列表(list)、字典(dict)
    注意：不过需要注意采用元组传递参数时后边需要多加一个逗号
    '''
    # #基于list
    # scheduler.add_job(job2, 'interval', seconds=5, args=['a','b','list'], id='test_job4')
    # #基于tuple
    # scheduler.add_job(job2, 'interval', seconds=5, args=('a','b','tuple',), id='test_job5')
    # #基于dict
    # scheduler.add_job(job3, 'interval', seconds=5, kwargs={'f':'dict', 'a':1,'b':2}, id='test_job6')
    
     
    #带有参数的示例
    # scheduler.add_job(job2, 'interval', seconds=5, args=['a','b'], id='test_job7')
    # scheduler.add_job(job2, 'interval', seconds=5, args=('a','b',), id='test_job8')
    # scheduler.add_job(job3, 'interval', seconds=5, kwargs={'a':1,'b':2}, id='test_job9')
    print scheduler.get_jobs()
    scheduler.start()




