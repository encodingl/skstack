#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2018年8月17日 @author: skipper
'''

from fabric import Connection

def ssh_cmd_back(host,port,username,password,cmd,rsa_key):
    ret = [host]

    if rsa_key:
        c1 = Connection(host, port=port, user=username, connect_kwargs={'key_filename':rsa_key,})
    elif  password:
        c1 = Connection(host, port=port, user=username, connect_kwargs={'password':password,})
    else:
        ret.append("没有配置密码或者秘钥")

    result = c1.run(cmd)
    ret.append(result.stdout)

    retcode = result.exited



    return ret,retcode

if __name__ == "__main__":
    c1 = Connection('172.28.28.127', port=22, user='root', connect_kwargs={'password':'rft420e',})
    c2 = Connection('172.28.28.127', port=22, user='root', connect_kwargs={'key_filename':'/root/.ssh/id_rsa',})
    r = c2.run("ansible gtest -f 1 -a 'date'")
    print r.exited
    
#     print r.stdout
