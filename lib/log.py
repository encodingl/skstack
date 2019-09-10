#! /usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from skstack.settings import BASE_DIR

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
                filemode='ab+')
    return logging.basicConfig
