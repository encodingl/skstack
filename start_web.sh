#!/bin/bash
#daphne -b 0.0.0.0 -p 8001 skstack.asgi:application
stdout_logfile=/opt/sklogs/skstack/skstack.log
python manage.py runserver 0.0.0.0:18001 > $stdout_logfile 2>&1 &


