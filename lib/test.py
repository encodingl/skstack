#! /usr/bin/env python
# -*- coding: utf-8 -*-

from lib.lib_config import get_redis_config
import redis

if __name__ == "__main__":
    redis_host,redis_port,redis_db,redis_password = get_redis_config()
    conn = redis.Redis(host=redis_host,db=redis_db,port=redis_port,password=redis_password)
    redis_chanel_pid_lock = "yyappgwprod11"
    redis_chanel_message = "yyappgwprod"
    conn.delete("yyappgwprod11")
    
    if conn.get(redis_chanel_pid_lock == "1") :
        conn.set(redis_chanel_message,"You have already submitted, or someone else is submitting the same project.If you have any other problems, please contact the administrator")     
               
        ret=conn.get(redis_chanel_message)
        print ret
        
        
    else:
        
        print conn.get(redis_chanel_pid_lock)