#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2018年7月9日 @author: skipper
'''
from skipper.celery import app as celery_app
from datetime import datetime,timedelta
import pytz
import sys



def format_celery_eta_time(time_str):
    try:
        time01 = datetime.strptime(time_str, "%Y-%m-%d-%H:%M:%S")
    except ValueError:
        time01 = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")   
    local_tz = pytz.timezone(celery_app.conf['CELERY_TIMEZONE'])
    format_eta_time = local_tz.localize(datetime.strptime(str(time01).strip(), '%Y-%m-%d %H:%M:%S'))
    return format_eta_time

if __name__ == "__main__":
    time_str = "2017-07-11 12:11:23"
    print format_celery_eta_time(time_str)