#! /usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE, STDOUT, call
from skcmdb.models import Host, HostGroup
from django.shortcuts import render
from django.http import HttpResponse
import os
from skconfig.views import get_dir
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
import logging
from lib.log import log
from lib.setup import get_playbook, get_roles
from .models import history
from datetime import datetime

# var info
ansible_dir = get_dir("a_path")
roles_dir = get_dir("r_path")
playbook_dir = get_dir("p_path")
level = get_dir("log_level")
log_path = get_dir("log_path")
log("setup.log", level, log_path)


@login_required()
@permission_verify()
def index(request):
    temp_name = "sktask/setup-header.html"
#     all_host = Host.objects.all()
#     all_dir = get_roles(roles_dir)
#     all_pbook = get_playbook(playbook_dir)
#     all_group = HostGroup.objects.all()
    
    return render(request, 'sktask/ansible.html', locals())


@login_required()
@permission_verify()
def playbook(request):
    ret = []
    temp_name = "sktask/setup-header.html"
    if os.path.exists(ansible_dir + '/gexec.yml'):
        os.remove(ansible_dir + '/gexec.yml')
    else:
        pass
    if request.method == 'POST':
        host = request.POST.getlist('mserver', [])
        group = request.POST.getlist('mgroup', [])
        pbook = request.POST.getlist('splaybook', [])
        roles = request.POST.getlist('mplaybook', [])
 
    if host:
        if roles:
            for h in host:
                logging.info("==========ansible tasks start==========")
                logging.info("User:"+request.user.username)
                logging.info("host:"+h)
                f = open(ansible_dir + '/gexec.yml', 'w+')
                flist = ['- hosts: '+h+'\n', '  remote_user: root\n', '  gather_facts: false\n', '  roles:\n']
                for r in roles:
                    rs = '    - ' + r + '\n'
                    flist.append(rs)
                    logging.info("Role:"+r)
                f.writelines(flist)
                f.close()
                cmd = "ansible-playbook"+" " + ansible_dir+'/gexec.yml'
                p = Popen(cmd, stderr=PIPE, stdout=PIPE, shell=True)
                data = p.communicate()
                print("data:%s" % data)
                ret.append(data)
                for d in data:
                    logging.info(d)
                logging.info("==========ansible tasks end============")
        else:
            for h in host:
                for p in pbook:
                    f = open(playbook_dir + p, 'r+')
                    flist = f.readlines()
                    flist[0] = '- hosts: '+h+'\n'
                    f = open(playbook_dir + p, 'w+')
                    f.writelines(flist)
                    f.close()
                    cmd = "ansible-playbook"+" " + playbook_dir + p
                    pcmd = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
                    data = pcmd.communicate()
                    ret.append(data)
                    print(data)
                    print(ret)
                    logging.info("==========ansible tasks start==========")
                    logging.info("User:"+request.user.username)
                    logging.info("host:"+h)
                    logging.info("Playbook:"+p)
                    for d in data:
                        logging.info(d)
                    logging.info("==========ansible tasks end============")
        return render(request, 'sktask/result.html', locals())
 
    if group:
        if roles:
            for g in group:
                logging.info("==========ansible tasks start==========")
                logging.info("User:"+request.user.username)
                logging.info("group:"+g)
                f = open(ansible_dir + '/gexec.yml', 'w+')
                flist = ['- hosts: '+g+'\n', '  remote_user: root\n', '  gather_facts: false\n', '  roles:\n']
                for r in roles:
                    rs = '    - ' + r + '\n'
                    flist.append(rs)
                    logging.info("Role:"+r)
                f.writelines(flist)
                f.close()
                cmd = "ansible-playbook"+" " + ansible_dir+'/gexec.yml'
                p = Popen(cmd, stderr=PIPE, stdout=PIPE, shell=True)
                data = p.communicate()
                ret.append(data)
                for d in data:
                    logging.info(d)
                logging.info("==========ansible tasks end============")
        else:
            for g in group:
                for p in pbook:
                    f = open(playbook_dir + p, 'r+')
                    flist = f.readlines()
                    flist[0] = '- hosts: '+g+'\n'
                    f = open(playbook_dir + p, 'w+')
                    f.writelines(flist)
                    f.close()
                    cmd = "ansible-playbook"+" " + playbook_dir + p
                    pcmd = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
                    data = pcmd.communicate()
                    ret.append(data)
                    logging.info("==========ansible tasks start==========")
                    logging.info("User:"+request.user.username)
                    logging.info("Group:"+g)
                    logging.info("Playbook:"+p)
                    for d in data:
                        logging.info(d)
                    logging.info("==========ansible tasks end============")
        return render(request, 'sktask/result.html', locals())


@login_required()
@permission_verify()
def ansible_command(request):
    command_list = []
    ret = []
    count = 1
    temp_name = "sktask/setup-header.html"
    if request.method == 'POST':
        mcommand = request.POST.get('mcommand')
        print('mcm_request %s'% mcommand)
        command_list = mcommand.split('\n')
        print('cm_list %s'% command_list)
        user=request.user
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
    
        for command in command_list:
            if command.startswith("ansible"):
                time_start= datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                p = Popen(command, stdout=PIPE, stderr=PIPE,shell=True)
                data = p.communicate()
                retcode=p.poll()
                
                
                ret.append(data)
            else:
                data = "your command " + str(count) + "  is invalid!"
                retcode=1
                ret.append(data)
            count += 1
            logging.info("==========ansible tasks start==========")
            logging.info("User:"+request.user.username)
            logging.info("command:"+command)
            for d in data:
                logging.info(d)
            logging.info("==========ansible tasks end============")
        # return render(request,'sktask/result.html', locals())
        print('ret value: %s' % ret)
        cmd_hosts =  ret[0][0].split('|')[0]
        task_name="ansible"
        if retcode==0:
            retcode="success"
        else:
            retcode="failed"
        dic_his={'login_user':user,
                 'src_ip':ip,
                 'cmd_object':cmd_hosts,
                 'cmd':mcommand,
                 'cmd_result':retcode,
                 'cmd_detail':ret,                
                 'time_task_start':time_start,
#                  'time_task_finished':time_finished,
                 'task_name':task_name}
        history.objects.create(**dic_his)
        return render(request, 'sktask/result.html', locals())


@login_required()
@permission_verify()
def host_sync(request):
 
    group = HostGroup.objects.all()
    ansible_file = open(ansible_dir+"/hosts", "wb")
    all_host = Host.objects.all()
    for host in all_host:
        #gitlab ansible_host=10.100.1.76 host_name=gitlab
        host_item = host.hostname+" "+"ansible_host="+host.ip+" "+"host_name="+host.hostname+"\n"
        ansible_file.write(host_item)
    for g in group:
        group_name = "["+g.name+"]"+"\n"
        ansible_file.write(group_name)
        members = Host.objects.filter(group__name=g)
        for m in members:
            group_item = m.hostname+"\n"
            ansible_file.write(group_item)
    ansible_file.close()
    logging.info("==========ansible tasks start==========")
    logging.info("User:"+request.user.username)
    logging.info("Task: sync cmdb info to ansible hosts")
    logging.info("==========ansible tasks end============")
    return HttpResponse("ok")
