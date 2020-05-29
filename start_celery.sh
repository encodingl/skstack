#!/bin/bash
export C_FORCE_ROOT="true"
logfile=/opt/sklogs/skstack/celery.log
celery -A skstack worker -c 16 --loglevel=info >> $logfile 2>&1 &
celery -A skstack flower --loglevel=info  >> $logfile 2>&1 &
celery -A skstack beat --loglevel=info  >> $logfile 2>&1 &


