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
    def test(self,tchn):
        return self.conn.get(tchn)
    
if __name__ == "__main__":
    r1=RedisLock(channel_name="chn001")
    cv = r1.get_channel_value()
    print(cv)
    r1.lock()
    cv = r1.get_channel_value()
    print(cv)
    r1.unlock()
    cv = r1.get_channel_value()
    print(cv)
    tv = r1.test(tchn="chn001")
    print(tv)




  
