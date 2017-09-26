#!/url/bin/env python
#-*- coding: utf8  -*-

from django.conf import settings
import MySQLdb
from skcmdb.models import DbSource
import ConfigParser


ASSET_TYPE = (
    (1, u"物理机"),
    (2, u"虚拟机"),
    (3, u"交换机"),
    (4, u"路由器"),
    (5, u"防火墙"),
    (6, u"Docker"),
    (7, u"其他")
    )



def mysql_execute(dbsource,sql):
    db = DbSource.objects.get(id=int(dbsource))
    config = {'host': db.host, 'user': db.user, 'passwd': db.password, 'port': db.port, 'db': db.db,'charset':'utf8'}
    db = MySQLdb.connect(**config)
    cursor  = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data

#
# class config:
#     def __init__(self,):
#         pass
#
#     config = ConfigParser.ConfigParser()
#     with open(dirs + '/skipper.conf', 'r') as cfgfile:
#         config.readfp(cfgfile)
#         a_path = config.get('config', 'ansible_path')
#         pro_path = config.get('config', 'project_base_path')
#         git_path = config.get('config', 'git_base_path')
#
#         #         r_path = config.get('config', 'roles_path')
#         #         p_path = config.get('config', 'playbook_path')
#         #         s_path = config.get('config', 'scripts_path')
#         engine = config.get('db', 'engine')
#         host = config.get('db', 'host')
#         port = config.get('db', 'port')
#         user = config.get('db', 'user')
#         password = config.get('db', 'password')
#         database = config.get('db', 'database')
#         token = config.get('token', 'token')
#         log_path = config.get('log', 'log_path')
#         log_level = config.get('log', 'log_level')



