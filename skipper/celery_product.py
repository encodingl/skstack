from celery_tasks import add
from time  import sleep

def notify(a, b):
    
    result = add.apply_async((a, b), queue='queue_task')
  
    return result

if __name__ == '__main__':
    haha = notify(7, 7)
    print haha.get(timeout=1)
    print haha.status
    print "haha.id: %s" % haha.id
