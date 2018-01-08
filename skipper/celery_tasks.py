from celery_init import celery
from time  import sleep

@celery.task
def add(x, y):
    print "=======>"
    sleep(10)
    print "<================="
    result = x + y
    
    return result