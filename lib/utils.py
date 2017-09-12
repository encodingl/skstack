#!/url/bin/env python
#-*- coding: utf8  -*-

import MySQLdb

from skcmdb.models import DbSource

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



