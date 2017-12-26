# file_name=init_celery.py
# coding: utf-8
from celery import Celery,platforms


BROKER_URL = 'redis://:redis0619@localhost:6379/0'
BACKEND_URL = 'redis://:redis0619@localhost:6379/1'
platforms.C_FORCE_ROOT = True

# Add tasks here
CELERY_IMPORTS = (
    'celery_init',
)


celery = Celery('celery',
    broker=BROKER_URL,
    backend=BACKEND_URL,
    include=CELERY_IMPORTS,)

celery.conf.update(
    CELERY_ACKS_LATE=True,
    CELERY_ACCEPT_CONTENT=['pickle', 'json'],
    CELERYD_FORCE_EXECV=True,
    CELERYD_MAX_TASKS_PER_CHILD=500,
    BROKER_HEARTBEAT=0,
)

