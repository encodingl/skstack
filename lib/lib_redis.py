#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import redis
from lib.lib_config import get_redis_config

def redis_subscribe():
    rc = redis.Redis(host='127.0.0.1',password='redis0619')
    ps = rc.pubsub()
    ps.subscribe(['c1', 'c2'])
    for item in ps.listen():
        if item['type'] == 'message':
            print(item['data'])
            
class RedisLock():
    def __init__(self,channel_name):
        self.channel_name=channel_name
        redis_host,redis_port,redis_db,redis_password = get_redis_config()

        self.conn = redis.Redis(host=redis_host,db=redis_db,port=redis_port,password=redis_password)
            
    def lock(self):
        self.conn.set(self.channel_name,"1")
    def unlock(self):
        self.conn.set(self.channel_name,"0") 
    def get_channel_value(self):
        return self.conn.get(self.channel_name)
    def is_locked(self):
        try:
            if self.conn.get(self.channel_name) == b"1":
                return True
            else:
                return False
        except:
            return "redis.conn.get error"
        
    def test(self,tchn):
        return self.conn.get(tchn)
    
if __name__ == "__main__":
    r1=RedisLock(channel_name="dev_nginx01_DEV_4_taskcommit_lock")
    cv = r1.get_channel_value()
    print(cv)
    print(r1.is_locked())
  
   
  




  
