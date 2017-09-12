#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import redis

def redis_subscribe():
    rc = redis.Redis(host='127.0.0.1',password='redis0619')
    ps = rc.pubsub()
    ps.subscribe(['c1', 'c2'])
    for item in ps.listen():
        if item['type'] == 'message':
            print item['data']
    
if __name__ == "__main__":
    



  