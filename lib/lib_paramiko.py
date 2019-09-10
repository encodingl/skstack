#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2018年8月9日 @author: encodingl
'''

import paramiko
import logging
log = logging.getLogger('skworkorders')


def ssh_cmd(host,port,username,password,cmd,rsa_key,request):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if rsa_key:
            key_file = paramiko.RSAKey.from_private_key_file(rsa_key)
            client.connect(host, port, username=username, pkey=key_file, timeout=20)
        elif  password:
            client.connect(host, port, username=username, password=password, timeout=20)
        else:
            request.websocket.send("没有配置密码或者秘钥")
        stdin, stdout,stderr = client.exec_command(cmd,get_pty=True)
        while 1:
            result = stdout.readline().encode('utf-8')
            if len(result) == 0:
                break
            request.websocket.send(result)
        channel = stdout.channel
        retcode = channel.recv_exit_status()  
        log.info("ssh_cmd_result2:%s" % stdout) 
    except Exception as e:
        log.error("ssh_cmd_result2:%s" % e)
        request.websocket.send(e)
       
    finally:
        client.close()
        return retcode
  

if __name__=="__main__":

   pass
 
