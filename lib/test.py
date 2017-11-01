#! /usr/bin/env python
# -*- coding: utf-8 -*-


from lib.lib_config import get_redis_config
import redis
from skdeploy.models import TaskStatus
import django
django.setup()

if __name__ == "__main__":
    obj = TaskStatus.objects.filter(id = 42)
    obj_hosts = obj.hosts_cus
    print obj_hosts
    print type(obj_hosts)