#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2018年6月19日 @author: encodingl
'''

import time
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
scheduler = BlockingScheduler()
# from lib_apscheduler import scheduler

# scheduler.remove_job('my_job_id')
# scheduler.remove_all_jobs()
scheduler.print_jobs()
# print scheduler.get_job('test_job2')
# apscheduler.job.Job.resume()