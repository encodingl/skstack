#!/bin/bash
stdout_logfile=/opt/sklogs/skstack/skstack.log
python manage.py runserver 0.0.0.0:18002 > $stdout_logfile 2>&1 &


