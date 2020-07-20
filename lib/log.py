#! /usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from skstack.settings import BASE_DIR
import os

dic = {"debug": logging.DEBUG,
       "warning": logging.WARNING,
       "info": logging.INFO,
       "critical": logging.CRITICAL,
       "error": logging.ERROR,
       }


def log(log_name, level="info", path=None):

    if path:
        log_path = path+'/'
    else:
        log_path = BASE_DIR+'/logs/'

    logging.basicConfig(level=dic[level],
                # format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                format='%(asctime)s|%(levelname)s|%(pathname)s|%(funcName)s|%(lineno)d|[msg:%(message)s]',
                datefmt='%Y%m%d %H:%M:%S',
                filename=log_path+log_name,
                filemode='a+')
    return logging.basicConfig

def showLog(created_at, task_name_created, logPath, workorder_group):
    if workorder_group == 'DeployDocker':
        dockerLogPath = logPath + '/pl_deploy_docker.log.' + task_name_created
        dockerLogPathBak = logPath + 'bak' + '/pl_deploy_docker.log.' + task_name_created
        if os.path.exists(dockerLogPath):
            with open(dockerLogPath, 'r', encoding='UTF-8') as f:
                # print(f.read())
                tpl_WorkOrderFlow_form_log = f.read()
                # print(tpl_WorkOrderFlow_form_log)
        elif os.path.exists(dockerLogPathBak):
            with open(dockerLogPathBak, 'r', encoding='UTF-8') as f:
                tpl_WorkOrderFlow_form_log = f.read()
        else:
            tpl_WorkOrderFlow_form_log = "日志文件不存在！！！"
    else:
        tpl_WorkOrderFlow_form_log = "非 docker 类型暂时不支持查看日志功能"

    return tpl_WorkOrderFlow_form_log