#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2018年4月17日 @author: skipper
'''

from django.shortcuts import render

from dwebsocket.decorators import accept_websocket, require_websocket

from django.http import HttpResponse
import paramiko



from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
import subprocess

from django.shortcuts import render_to_response, RequestContext


@login_required()
@permission_verify()
def websocket_index(request):
    temp_name = "skworkorders/skworkorders-header.html"    
 

    return render_to_response('skworkorders/websocket.html', locals(), RequestContext(request))

def exec_command(comm):
    hostname = '172.28.28.127'
    username = 'root'
    password = 'rft420e'

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, username=username, password=password)
    stdin, stdout, stderr = ssh.exec_command(comm)
    result = stdout.read()
    ssh.close()
    return result


@accept_websocket
def echo(request):
    temp_name = "skworkorders/skworkorders-header.html" 
    if not request.is_websocket():#判断是不是websocket连接
       
        try:#如果是普通的http方法
            message = request.GET['message']
            return HttpResponse(message)
        except:
            return render_to_response('skworkorders/websocket.html', locals(), RequestContext(request))
    else:
        for message in request.websocket:
            cmd = message
            print cmd
       
#             request.websocket.send(exec_command(cmd))
            pcmd = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
            while True: 
                 line = pcmd.stdout.readline().strip()  #获取内容
                 print line
                 if line:
                      request.websocket.send(line)
                 else:
                     
                     break
            retcode=pcmd.wait()
            if retcode==0:
                ret_message="执行成功"
            else:
                ret_message="执行失败"
            request.websocket.send(ret_message)
#             request.websocket.send(exec_command(cmd))#发送消息到客户端