#!/bin/bash
stdout_logfile=/opt/sklogs/skipper/skipper.log
python manage.py runserver 0.0.0.0:8000 > $stdout_logfile 2>&1 &