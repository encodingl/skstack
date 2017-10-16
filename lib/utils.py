#!/url/bin/env python
# -*- coding: utf8  -*-

from django.conf import settings
import MySQLdb
from skcmdb.models import DbSource
import ConfigParser, os
from django.conf import settings

ASSET_TYPE = (
    (1, u"物理机"),
    (2, u"虚拟机"),
    (3, u"交换机"),
    (4, u"路由器"),
    (5, u"防火墙"),
    (6, u"Docker"),
    (7, u"其他")
)


def mysql_execute(dbsource, sql):
    db = DbSource.objects.get(id=int(dbsource))
    config = {'host': db.host, 'user': db.user, 'passwd': db.password, 'port': db.port, 'db': db.db, 'charset': 'utf8'}
    db = MySQLdb.connect(**config)
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data


def get_object(model, **kwargs):
    """
    use this function for query
    使用改封装函数查询数据库
    """
    for value in kwargs.values():
        if not value:
            return None

    the_object = model.objects.filter(**kwargs)
    if len(the_object) == 1:
        the_object = the_object[0]
    else:
        the_object = None
    return the_object


def config(path=os.path.join(settings.BASE_DIR, 'skipper.conf')):
    obj = ConfigParser.ConfigParser()
    obj.read(path)
    return obj
