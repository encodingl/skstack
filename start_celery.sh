#!/bin/bash
logfile=/opt/data/logs/skipper/celery.log
celery -A skipper worker -c 16 --loglevel=info >> $logfile 2>&1 &
#celery -A skipper flower --loglevel=info  >> $logfile 2>&1 &
celery -A skipper beat --loglevel=info  >> $logfile 2>&1 &


